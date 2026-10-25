"""
本体生成服务
接口1：分析文本内容，生成适合社会模拟的实体和关系类型定义
"""

import json
import logging
import re
from typing import Dict, Any, List, Optional
from ..utils.llm_client import LLMClient
from ..utils.locale import get_language_instruction
from ..utils.file_parser import split_text_into_chunks
from ..config import Config
from ..utils.ontology import (
    MAX_ONTOLOGY_TYPES,
    normalize_ontology_attributes,
    normalize_ontology_source_targets,
)

logger = logging.getLogger(__name__)


def _to_pascal_case(name: str) -> str:
    """将任意格式的名称转换为 PascalCase（如 'works_for' -> 'WorksFor', 'person' -> 'Person'）"""
    # 按非字母数字字符分割
    parts = re.split(r'[^a-zA-Z0-9]+', name)
    # 再按 camelCase 边界分割（如 'camelCase' -> ['camel', 'Case']）
    words = []
    for part in parts:
        words.extend(re.sub(r'([a-z])([A-Z])', r'\1_\2', part).split('_'))
    # 每个词首字母大写，过滤空串
    result = ''.join(word.capitalize() for word in words if word)
    return result if result else 'Unknown'


def _to_upper_snake_case(name: str) -> str:
    """Convert free-form or camelCase names to SCREAMING_SNAKE_CASE."""

    separated = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name.strip())
    normalized = re.sub(r'[^a-zA-Z0-9]+', '_', separated).strip('_').upper()
    if not normalized:
        return "UNKNOWN"
    if normalized[0].isdigit():
        normalized = f"REL_{normalized}"
    return normalized


# Ontology Generation System Prompt
ONTOLOGY_SYSTEM_PROMPT = """You are an expert knowledge graph ontology designer. Your task is to analyze the provided text content and simulation requirements, and design entity types and relationship types suitable for social media simulation.

**IMPORTANT: You must output valid JSON data only. Do not output any markdown or surrounding explanation.**

## Core Task Background
We are building a social media simulation system where:
- Each entity is an account or agent that can speak, interact, and disseminate information on social media.
- Entities influence, repost, comment on, and respond to each other.
- We simulate reactions and information propagation paths across all involved parties.

Therefore, entities must be real-world entities that can speak and interact on social media:
CAN BE: Specific individuals (public figures, spokespersons, key opinion leaders, experts, citizens), companies/corporations, organizations/institutions (universities, associations, NGOs), government agencies, media outlets, or community group representatives.
CANNOT BE: Abstract concepts (e.g. "Public Opinion", "Emotion", "Trend"), topics (e.g. "Academic Integrity"), or viewpoints (e.g. "Supporters", "Opponents").

## Output Format
Output JSON with the following structure:
```json
{
    "entity_types": [
        {
            "name": "PascalCaseEntityName",
            "description": "Short description in English (under 100 characters)",
            "attributes": [
                {
                    "name": "attribute_name_snake_case",
                    "type": "text",
                    "description": "Attribute description in English"
                }
            ],
            "examples": ["Example 1", "Example 2"]
        }
    ],
    "edge_types": [
        {
            "name": "UPPER_SNAKE_CASE_RELATION",
            "description": "Short description in English (under 100 characters)",
            "source_targets": [
                {"source": "SourceEntityType", "target": "TargetEntityType"}
            ],
            "attributes": []
        }
    ],
    "analysis_summary": "Brief summary of text content in English"
}
```

## Design Guidelines:
1. 5 to 7 specific domain entity types relevant to the text. (Do NOT output generic Person or Organization; the system automatically adds them as fallbacks).
2. 4 to 8 relationship types that reflect real connections in the text (e.g., WORKS_FOR, AFFILIATED_WITH, CRITICIZES, SUPPORTS, INVESTIGATES, COLLABORATES_WITH).
3. 1-2 attributes per entity type (do not use reserved words: name, uuid, group_id, graph_id, created_at, summary).
4. Keep descriptions under 15 words and examples to 1-2 items per entity.
5. All entity names, relationship names, attribute names, descriptions, examples, and analysis_summary MUST be written in English.
"""


class OntologyGenerator:
    """
    本体生成器
    分析文本内容，生成实体和关系类型定义
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()
    
    def generate(
        self,
        document_texts: List[str],
        simulation_requirement: str,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        生成本体定义
        
        Args:
            document_texts: 文档文本列表
            simulation_requirement: 模拟需求描述
            additional_context: 额外上下文
            
        Returns:
            本体定义（entity_types, edge_types等）
        """
        # 构建用户消息
        user_message = self._build_user_message(
            document_texts, 
            simulation_requirement,
            additional_context
        )
        
        lang_instruction = get_language_instruction()
        system_prompt = (
            f"{ONTOLOGY_SYSTEM_PROMPT}\n\n{lang_instruction}\n"
            "IMPORTANT: Entity type names MUST be in English PascalCase (e.g., 'PersonEntity', 'MediaOrganization'). "
            "Relationship type names MUST be in English UPPER_SNAKE_CASE (e.g., 'WORKS_FOR'). "
            "Attribute names MUST be in English snake_case. Only description fields and analysis_summary should use the specified language above.\n"
            "CRITICAL TOKEN LIMIT RULE: Keep all entity and relationship descriptions concise (under 15 words). "
            "Provide at most 2 attributes and 2 examples per entity type. Keep analysis_summary under 40 words. "
            "This ensures the JSON output is compact and never truncated at provider token limits."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Structured ontology responses can exceed 4096 completion tokens.
        # Allow natural model limit via max_tokens=None and 2 attempts with auto-repair.
        result = None
        try:
            result = self.llm_client.chat_json(
                messages=messages,
                temperature=0.3,
                max_tokens=None,
                max_attempts=2,
                allow_repair=True,
            )
        except Exception as err:
            logger.warning(
                "Ontology chat_json failed: %s. Attempting extraction / fallback recovery...",
                err,
            )
            raw_text = getattr(err, "raw_content", None)
            if raw_text:
                result = self._extract_partial_ontology(raw_text)

            if not result or len(result.get("entity_types", [])) < 2:
                # Emergency compact extraction prompt
                try:
                    compact_messages = [
                        {
                            "role": "system",
                            "content": (
                                "You are a knowledge graph ontology generator. Output ONLY a valid JSON object with "
                                "'entity_types' (5 domain types, PascalCase name, short description) and "
                                "'edge_types' (4 relations). Keep descriptions under 8 words. No markdown."
                            ),
                        },
                        {
                            "role": "user",
                            "content": f"Extract 5 domain entity types and 4 relations for social simulation from:\n{simulation_requirement[:1200]}",
                        },
                    ]
                    result = self.llm_client.chat_json(
                        messages=compact_messages,
                        temperature=0.2,
                        max_tokens=2048,
                        max_attempts=2,
                        allow_repair=True,
                    )
                except Exception as fallback_err:
                    logger.warning(
                        "Emergency compact ontology prompt failed: %s. Generating heuristic ontology.",
                        fallback_err,
                    )
                    result = self._generate_heuristic_ontology(simulation_requirement, document_texts)

        # 验证和后处理
        result = self._validate_and_process(result or {})
        
        return result

    def _extract_partial_ontology(self, raw_text: str) -> Optional[Dict[str, Any]]:
        """Extract valid entity_types and edge_types from truncated or malformed LLM output."""
        from ..utils.llm_client import repair_json_string
        repaired = repair_json_string(raw_text)
        if isinstance(repaired, dict) and (repaired.get("entity_types") or repaired.get("edge_types")):
            return repaired

        # Fallback: scan for individual entity objects in the raw text
        entities = []
        entity_matches = re.finditer(
            r'\{\s*"name"\s*:\s*"([A-Za-z0-9_]+)"[^}]*\}',
            raw_text,
        )
        for m in entity_matches:
            try:
                obj = json.loads(m.group(0))
                if isinstance(obj, dict) and obj.get("name"):
                    entities.append(obj)
            except Exception:
                continue

        summary_match = re.search(r'"analysis_summary"\s*:\s*"([^"]*)', raw_text)
        summary = summary_match.group(1) if summary_match else "Extracted scenario ontology."

        if entities:
            return {
                "entity_types": entities,
                "edge_types": [],
                "analysis_summary": summary,
            }
        return None

    def _generate_heuristic_ontology(
        self,
        simulation_requirement: str,
        document_texts: List[str],
    ) -> Dict[str, Any]:
        """Generate high-quality domain entities when LLM API is unavailable or exhausted."""
        text_preview = (simulation_requirement + " " + " ".join(document_texts[:2]))[:2000].lower()

        entities = []
        if any(w in text_preview for w in ("military", "defense", "war", "combat", "weapon", "army", "security")):
            entities.extend([
                {"name": "DefenseContractor", "description": "Corporations developing defense and strategic technologies.", "attributes": [{"name": "company_name", "type": "text", "description": "Name"}]},
                {"name": "MilitaryOfficial", "description": "Commanders and strategic defense personnel.", "attributes": [{"name": "rank_role", "type": "text", "description": "Rank and role"}]},
                {"name": "GovernmentAgency", "description": "National security and regulatory bodies.", "attributes": [{"name": "agency_name", "type": "text", "description": "Agency name"}]},
            ])
        elif any(w in text_preview for w in ("finance", "stock", "bank", "crypto", "market", "economy", "investment")):
            entities.extend([
                {"name": "FinancialInstitution", "description": "Banks, investment firms, and market makers.", "attributes": [{"name": "institution_name", "type": "text", "description": "Name"}]},
                {"name": "RegulatoryAuthority", "description": "Financial and market compliance regulators.", "attributes": [{"name": "jurisdiction", "type": "text", "description": "Jurisdiction"}]},
                {"name": "MarketAnalyst", "description": "Economic forecasters and industry analysts.", "attributes": [{"name": "firm_affiliation", "type": "text", "description": "Affiliation"}]},
            ])
        else:
            entities.extend([
                {"name": "OfficialSpokesperson", "description": "Institutional and governmental representatives.", "attributes": [{"name": "institution", "type": "text", "description": "Institution"}]},
                {"name": "IndustryExpert", "description": "Domain specialists and analysts.", "attributes": [{"name": "specialization", "type": "text", "description": "Field of expertise"}]},
                {"name": "MediaOutlet", "description": "Journalistic and news broadcast entities.", "attributes": [{"name": "reach", "type": "text", "description": "Audience reach"}]},
            ])

        entities.extend([
            {"name": "PublicAudience", "description": "Engaged citizens and digital commentators.", "attributes": [{"name": "demographic", "type": "text", "description": "Demographic group"}]},
            {"name": "CivilSocietyGroup", "description": "NGOs and advocacy groups.", "attributes": [{"name": "cause", "type": "text", "description": "Mission"}]},
        ])

        return {
            "entity_types": entities,
            "edge_types": [],
            "analysis_summary": "Heuristic domain ontology configured for scenario simulation.",
        }
    
    # 传给 LLM 的文本最大长度（5万字）
    MAX_TEXT_LENGTH_FOR_LLM = Config.ONTOLOGY_MAX_TEXT_LENGTH
    LONG_TEXT_CHUNK_SIZE = 8000
    LONG_TEXT_CHUNK_OVERLAP = 200
    MAX_LONG_TEXT_CHUNKS = 60
    MIN_LONG_TEXT_EXCERPT = 400
    
    def _build_user_message(
        self,
        document_texts: List[str],
        simulation_requirement: str,
        additional_context: Optional[str]
    ) -> str:
        """构建用户消息"""
        
        combined_text = self._build_document_context(document_texts)
        
        message = f"""## 模拟需求

{simulation_requirement}

## 文档内容

{combined_text}
"""
        
        if additional_context:
            message += f"""
## 额外说明

{additional_context}
"""
        
        message += """
请根据以上内容，设计适合社会舆论模拟的实体类型和关系类型。

**必须遵守的规则**：
1. 输出 5 到 7 个具体领域实体类型（无需输出通用的 Person 和 Organization，系统会自动补充）
2. 每个实体类型包含 1-2 个核心属性和 1-2 个代表性示例，描述精炼控制在 15 个词以内
3. 输出 4 到 8 个核心关系类型
4. 属性名不能使用 name、uuid、group_id、graph_id 等保留字，用 full_name、org_name 等替代
"""
        
        return message

    def _build_document_context(self, document_texts: List[str]) -> str:
        """构建用于本体分析的文档上下文，长文本按全局分块抽样而不是只截取开头。"""

        combined_text = "\n\n---\n\n".join(document_texts)
        original_length = len(combined_text)

        if original_length <= self.MAX_TEXT_LENGTH_FOR_LLM:
            return combined_text

        chunks = self._collect_document_chunks(document_texts)
        if not chunks:
            return ""

        selected_chunks = self._select_representative_chunks(chunks)
        excerpt_budget = self._calculate_excerpt_budget(len(selected_chunks))
        context = self._render_chunked_context(
            selected_chunks=selected_chunks,
            original_length=original_length,
            total_chunks=len(chunks),
            excerpt_limit=excerpt_budget,
        )

        while len(context) > self.MAX_TEXT_LENGTH_FOR_LLM and excerpt_budget > self.MIN_LONG_TEXT_EXCERPT:
            excerpt_budget = max(self.MIN_LONG_TEXT_EXCERPT, int(excerpt_budget * 0.85))
            context = self._render_chunked_context(
                selected_chunks=selected_chunks,
                original_length=original_length,
                total_chunks=len(chunks),
                excerpt_limit=excerpt_budget,
            )

        if len(context) > self.MAX_TEXT_LENGTH_FOR_LLM:
            marker = "\n\n...(分块上下文已压缩到本体分析长度限制内)..."
            context = context[:self.MAX_TEXT_LENGTH_FOR_LLM - len(marker)] + marker

        return context

    def _collect_document_chunks(self, document_texts: List[str]) -> List[Dict[str, Any]]:
        """按文档收集分块，保留文档和分块编号方便提示词定位。"""

        all_chunks: List[Dict[str, Any]] = []
        for doc_index, text in enumerate(document_texts, 1):
            doc_chunks = split_text_into_chunks(
                text,
                chunk_size=self.LONG_TEXT_CHUNK_SIZE,
                overlap=self.LONG_TEXT_CHUNK_OVERLAP,
            )
            total_doc_chunks = len(doc_chunks)
            for chunk_index, chunk in enumerate(doc_chunks, 1):
                all_chunks.append({
                    "document_index": doc_index,
                    "chunk_index": chunk_index,
                    "total_document_chunks": total_doc_chunks,
                    "text": chunk,
                })

        return all_chunks

    def _select_representative_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """从全部分块中等距抽样，覆盖长文开头、中段和结尾。"""

        if len(chunks) <= self.MAX_LONG_TEXT_CHUNKS:
            return chunks

        if self.MAX_LONG_TEXT_CHUNKS <= 1:
            return [chunks[0]]

        last_index = len(chunks) - 1
        selected_indexes = {
            round(i * last_index / (self.MAX_LONG_TEXT_CHUNKS - 1))
            for i in range(self.MAX_LONG_TEXT_CHUNKS)
        }
        return [chunks[i] for i in sorted(selected_indexes)]

    def _calculate_excerpt_budget(self, selected_count: int) -> int:
        """根据选中的分块数量为每块分配字符预算。"""

        header_budget = 600
        chunk_header_budget = 120 * selected_count
        available = max(
            self.MIN_LONG_TEXT_EXCERPT * selected_count,
            self.MAX_TEXT_LENGTH_FOR_LLM - header_budget - chunk_header_budget,
        )
        return max(self.MIN_LONG_TEXT_EXCERPT, available // max(selected_count, 1))

    def _render_chunked_context(
        self,
        selected_chunks: List[Dict[str, Any]],
        original_length: int,
        total_chunks: int,
        excerpt_limit: int,
    ) -> str:
        """渲染长文本分块上下文。"""

        lines = [
            (
                f"【长文本自动分块摘要】原文共{original_length}字，"
                f"已分为{total_chunks}个文本块用于全局覆盖分析。"
            ),
            (
                f"以下展示其中{len(selected_chunks)}个代表性文本块的摘录，"
                "覆盖开头、中段和结尾；请基于这些跨全文线索设计本体，不要只依赖第一段内容。"
            ),
        ]

        for chunk in selected_chunks:
            excerpt = self._excerpt_text(chunk["text"], excerpt_limit)
            lines.append(
                "\n".join([
                    (
                        f"--- 文档 {chunk['document_index']} / "
                        f"分块 {chunk['chunk_index']}/{chunk['total_document_chunks']} ---"
                    ),
                    excerpt,
                ])
            )

        return "\n\n".join(lines)

    @staticmethod
    def _excerpt_text(text: str, char_limit: int) -> str:
        """长分块保留首尾，避免每个分块内部再次变成只看开头。"""

        text = text.strip()
        if len(text) <= char_limit:
            return text

        marker = "\n...(本分块中间内容省略)...\n"
        if char_limit <= len(marker) + 20:
            return text[:char_limit]

        remaining = char_limit - len(marker)
        head_len = remaining // 2
        tail_len = remaining - head_len
        return f"{text[:head_len].rstrip()}{marker}{text[-tail_len:].lstrip()}"
    
    def _validate_and_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """验证和后处理结果"""
        if not isinstance(result, dict):
            raise ValueError("Ontology result must be an object")

        raw_entities = result.get("entity_types")
        raw_edges = result.get("edge_types")
        if not isinstance(raw_entities, list):
            raw_entities = []
        if not isinstance(raw_edges, list):
            raw_edges = []
        if not isinstance(result.get("analysis_summary"), str):
            result["analysis_summary"] = ""

        # Normalize entity entries before touching their fields. LLMs
        # occasionally emit a bare string, null, or another scalar.
        entity_name_map: Dict[str, str] = {}
        processed_entities: List[Dict[str, Any]] = []
        seen_entity_names = set()
        for raw_entity in raw_entities:
            if isinstance(raw_entity, str):
                entity = {"name": raw_entity}
            elif isinstance(raw_entity, dict):
                entity = dict(raw_entity)
            else:
                logger.warning("Ignoring non-object ontology entity entry")
                continue

            original_name = entity.get("name")
            if not isinstance(original_name, str) or not original_name.strip():
                logger.warning("Ignoring ontology entity without a usable name")
                continue
            original_name = original_name.strip()
            normalized_name = _to_pascal_case(original_name)
            if normalized_name == "Unknown":
                continue
            if normalized_name in seen_entity_names:
                logger.warning(f"Duplicate entity type '{normalized_name}' removed during validation")
                entity_name_map[original_name] = normalized_name
                entity_name_map[original_name.lower()] = normalized_name
                continue

            if normalized_name != original_name:
                logger.warning(
                    f"Entity type name '{original_name}' auto-converted to '{normalized_name}'"
                )
            entity["name"] = normalized_name
            entity["attributes"] = normalize_ontology_attributes(
                entity.get("attributes", [])
            )
            if not isinstance(entity.get("examples"), list):
                entity["examples"] = []
            description = entity.get("description")
            if not isinstance(description, str) or not description:
                description = f"A {normalized_name} entity."
            entity["description"] = (
                description[:97] + "..." if len(description) > 100 else description
            )

            seen_entity_names.add(normalized_name)
            processed_entities.append(entity)
            entity_name_map[original_name] = normalized_name
            entity_name_map[original_name.lower()] = normalized_name
            entity_name_map[normalized_name] = normalized_name
            entity_name_map[normalized_name.lower()] = normalized_name

        result["entity_types"] = processed_entities

        # 兜底类型定义
        person_fallback = {
            "name": "Person",
            "description": "Any individual person not fitting other specific person types.",
            "attributes": [
                {"name": "full_name", "type": "text", "description": "Full name of the person"},
                {"name": "role", "type": "text", "description": "Role or occupation"}
            ],
            "examples": ["ordinary citizen", "anonymous netizen"]
        }
        
        organization_fallback = {
            "name": "Organization",
            "description": "Any organization not fitting other specific organization types.",
            "attributes": [
                {"name": "org_name", "type": "text", "description": "Name of the organization"},
                {"name": "org_type", "type": "text", "description": "Type of organization"}
            ],
            "examples": ["small business", "community group"]
        }
        
        # 检查是否已有兜底类型
        entity_names = {e["name"] for e in result["entity_types"]}
        has_person = "Person" in entity_names
        has_organization = "Organization" in entity_names
        
        # 需要添加的兜底类型
        fallbacks_to_add = []
        if not has_person:
            fallbacks_to_add.append(person_fallback)
        if not has_organization:
            fallbacks_to_add.append(organization_fallback)
        
        if fallbacks_to_add:
            current_count = len(result["entity_types"])
            needed_slots = len(fallbacks_to_add)
            
            # 如果添加后会超过 10 个，需要移除一些现有类型
            if current_count + needed_slots > MAX_ONTOLOGY_TYPES:
                # 计算需要移除多少个
                to_remove = current_count + needed_slots - MAX_ONTOLOGY_TYPES
                # 从末尾移除（保留前面更重要的具体类型）
                result["entity_types"] = result["entity_types"][:-to_remove]
            
            # 添加兜底类型
            result["entity_types"].extend(fallbacks_to_add)
        
        # 最终确保不超过限制（防御性编程）
        result["entity_types"] = result["entity_types"][:MAX_ONTOLOGY_TYPES]

        # Resolve edge endpoints only after entity fallback/capping, so an edge
        # cannot refer to a type that was removed to satisfy Zep's limits.
        valid_entity_names = {entity["name"] for entity in result["entity_types"]}
        for name in valid_entity_names:
            entity_name_map[name] = name
            entity_name_map[name.lower()] = name

        def resolve_entity_name(value: str) -> Optional[str]:
            stripped = value.strip()
            if stripped == "Entity":
                return stripped
            mapped = entity_name_map.get(stripped) or entity_name_map.get(stripped.lower())
            if mapped in valid_entity_names:
                return mapped
            pascal_name = _to_pascal_case(stripped)
            return pascal_name if pascal_name in valid_entity_names else None

        processed_edges: List[Dict[str, Any]] = []
        seen_edge_names = set()
        for raw_edge in raw_edges:
            if isinstance(raw_edge, str):
                # A bare edge name has no endpoints and cannot be installed in
                # Zep safely. Ignore it instead of inventing a relationship.
                logger.warning(f"Ignoring ontology edge without source_targets: {raw_edge}")
                continue
            elif isinstance(raw_edge, dict):
                edge = dict(raw_edge)
            else:
                logger.warning("Ignoring non-object ontology edge entry")
                continue

            original_name = edge.get("name")
            if not isinstance(original_name, str) or not original_name.strip():
                logger.warning("Ignoring ontology edge without a usable name")
                continue
            normalized_name = _to_upper_snake_case(original_name)
            if normalized_name == "UNKNOWN" or normalized_name in seen_edge_names:
                if normalized_name in seen_edge_names:
                    logger.warning(f"Duplicate edge type '{normalized_name}' removed during validation")
                continue
            if normalized_name != original_name:
                logger.warning(
                    f"Edge type name '{original_name}' auto-converted to '{normalized_name}'"
                )
            edge["name"] = normalized_name

            normalized_targets = []
            for source_target in normalize_ontology_source_targets(
                edge.get("source_targets", []),
                limit=None,
            ):
                source = resolve_entity_name(source_target["source"])
                target = resolve_entity_name(source_target["target"])
                if source and target:
                    normalized_targets.append({"source": source, "target": target})
            edge["source_targets"] = normalize_ontology_source_targets(
                normalized_targets
            )
            edge["attributes"] = normalize_ontology_attributes(
                edge.get("attributes", [])
            )
            description = edge.get("description")
            if not isinstance(description, str) or not description:
                description = f"A {normalized_name} relationship."
            edge["description"] = (
                description[:97] + "..." if len(description) > 100 else description
            )

            seen_edge_names.add(normalized_name)
            processed_edges.append(edge)
            if len(processed_edges) == MAX_ONTOLOGY_TYPES:
                break

        if not processed_edges:
            standard_relations = [
                ("WORKS_FOR", "Employment or official affiliation", "Person", "Organization"),
                ("AFFILIATED_WITH", "Associated with an institution or group", "Person", "Organization"),
                ("CRITICIZES", "Public criticism, opposition, or dissent", "Person", "Organization"),
                ("SUPPORTS", "Public endorsement or alignment", "Person", "Organization"),
                ("COMMUNICATES_WITH", "Direct communication, dialogue, or response", "Person", "Person"),
                ("INFLUENCES", "Informational influence or opinion shaping", "Organization", "Person"),
            ]
            for rel_name, rel_desc, src_default, tgt_default in standard_relations:
                src = src_default if src_default in valid_entity_names else (list(valid_entity_names)[0] if valid_entity_names else "Entity")
                tgt = tgt_default if tgt_default in valid_entity_names else (list(valid_entity_names)[-1] if valid_entity_names else "Entity")
                processed_edges.append({
                    "name": rel_name,
                    "description": rel_desc,
                    "source_targets": [{"source": src, "target": tgt}],
                    "attributes": []
                })

        result["edge_types"] = processed_edges
        
        return result
    
    def generate_python_code(self, ontology: Dict[str, Any]) -> str:
        """
        将本体定义转换为Python代码（类似ontology.py）
        
        Args:
            ontology: 本体定义
            
        Returns:
            Python代码字符串
        """
        code_lines = [
            '"""',
            '自定义实体类型定义',
            'Auto-generated by Brain for social opinion simulation',
            '"""',
            '',
            'from pydantic import Field',
            'from zep_cloud.external_clients.ontology import EntityModel, EntityText, EdgeModel',
            '',
            '',
            '# ============== 实体类型定义 ==============',
            '',
        ]
        
        # 生成实体类型
        for entity in ontology.get("entity_types", []):
            name = entity["name"]
            desc = entity.get("description", f"A {name} entity.")
            
            code_lines.append(f'class {name}(EntityModel):')
            code_lines.append(f'    """{desc}"""')
            
            attrs = entity.get("attributes", [])
            if attrs:
                for attr in attrs:
                    attr_name = attr["name"]
                    attr_desc = attr.get("description", attr_name)
                    code_lines.append(f'    {attr_name}: EntityText = Field(')
                    code_lines.append(f'        description="{attr_desc}",')
                    code_lines.append(f'        default=None')
                    code_lines.append(f'    )')
            else:
                code_lines.append('    pass')
            
            code_lines.append('')
            code_lines.append('')
        
        code_lines.append('# ============== 关系类型定义 ==============')
        code_lines.append('')
        
        # 生成关系类型
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            # 转换为PascalCase类名
            class_name = ''.join(word.capitalize() for word in name.split('_'))
            desc = edge.get("description", f"A {name} relationship.")
            
            code_lines.append(f'class {class_name}(EdgeModel):')
            code_lines.append(f'    """{desc}"""')
            
            attrs = edge.get("attributes", [])
            if attrs:
                for attr in attrs:
                    attr_name = attr["name"]
                    attr_desc = attr.get("description", attr_name)
                    code_lines.append(f'    {attr_name}: EntityText = Field(')
                    code_lines.append(f'        description="{attr_desc}",')
                    code_lines.append(f'        default=None')
                    code_lines.append(f'    )')
            else:
                code_lines.append('    pass')
            
            code_lines.append('')
            code_lines.append('')
        
        # 生成类型字典
        code_lines.append('# ============== 类型配置 ==============')
        code_lines.append('')
        code_lines.append('ENTITY_TYPES = {')
        for entity in ontology.get("entity_types", []):
            name = entity["name"]
            code_lines.append(f'    "{name}": {name},')
        code_lines.append('}')
        code_lines.append('')
        code_lines.append('EDGE_TYPES = {')
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            class_name = ''.join(word.capitalize() for word in name.split('_'))
            code_lines.append(f'    "{name}": {class_name},')
        code_lines.append('}')
        code_lines.append('')
        
        # 生成边的source_targets映射
        code_lines.append('EDGE_SOURCE_TARGETS = {')
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            source_targets = edge.get("source_targets", [])
            if source_targets:
                st_list = ', '.join([
                    f'{{"source": "{st.get("source", "Entity")}", "target": "{st.get("target", "Entity")}"}}'
                    for st in source_targets
                ])
                code_lines.append(f'    "{name}": [{st_list}],')
        code_lines.append('}')
        
        return '\n'.join(code_lines)
