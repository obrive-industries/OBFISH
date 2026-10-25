"""
LLM客户端封装
统一使用OpenAI格式调用
"""

import json
import logging
import re
from typing import Optional, Dict, Any, List
from openai import OpenAI

from ..config import Config
from .openai_chat_compat import create_chat_completion, extract_chat_completion_text


logger = logging.getLogger(__name__)


class LLMResponseError(ValueError):
    """A safe, structured error for unusable model responses."""

    def __init__(self, message: str, *, finish_reason: Optional[str] = None):
        super().__init__(message)
        self.finish_reason = finish_reason


def _extract_error_details(error: Exception) -> Optional[Dict[str, Any]]:
    """Safely extract provider error detail payload from SDK or response exceptions."""
    body = getattr(error, "body", None)
    if isinstance(body, dict):
        return body.get("error", body) if isinstance(body.get("error"), dict) else body
    response = getattr(error, "response", None)
    if response is not None:
        try:
            data = response.json()
            if isinstance(data, dict):
                return data.get("error", data) if isinstance(data.get("error"), dict) else data
        except Exception:
            pass
    return None


def _is_response_format_unsupported(error: Exception) -> bool:
    """Detect an explicit provider rejection of JSON response_format."""

    if getattr(error, "status_code", None) not in {400, 422}:
        return False

    details = _extract_error_details(error)
    if not isinstance(details, dict):
        return False

    param = str(details.get("param") or "").strip().lower()
    if param == "response_format" or param.startswith("response_format."):
        return True

    code = str(details.get("code") or "").lower()
    if code in {"json_validate_failed", "json_format_error"}:
        return True

    message = str(details.get("message") or "").lower()
    if "failed to generate json" in message:
        return True

    if "response_format" not in message:
        return False

    unsupported_codes = {
        "unsupported_parameter",
        "unsupported_value",
        "unknown_parameter",
        "invalid_parameter",
    }
    unsupported_phrases = (
        "not support",
        "unsupported",
        "unknown parameter",
        "unrecognized parameter",
    )
    return code in unsupported_codes or any(
        phrase in message for phrase in unsupported_phrases
    )


def _clean_chat_text(content: str) -> str:
    """Remove common reasoning wrappers and an outer Markdown JSON fence."""

    cleaned = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
    cleaned = cleaned.lstrip("\ufeff")
    cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\n?```\s*$', '', cleaned)
    return cleaned.strip()


def _contains_additional_json_container(content: str) -> bool:
    """Return True when trailing text embeds another JSON object or array."""

    decoder = json.JSONDecoder()
    for match in re.finditer(r"[\[{]", content):
        try:
            value, _ = decoder.raw_decode(content[match.start():])
        except json.JSONDecodeError:
            continue
        if isinstance(value, (dict, list)):
            return True
    return False


def is_retryable_llm_error(err: Exception) -> bool:
    """Return True if an error from an LLM provider warrants failover/retry."""
    status = getattr(err, "status_code", None)
    err_str = str(err).lower()
    err_type = type(err).__name__.lower()

    # HTTP status codes: rate limits, timeouts, server errors, quota exceeded
    if status in {403, 408, 429, 500, 502, 503, 504}:
        return True

    # Connection and timeout errors (status_code is often None in OpenAI SDK)
    if any(k in err_type for k in ("connection", "timeout", "remotedisconnected", "apiconnectionerror", "apitimeouterror")):
        return True

    # Text indicators in message or error body
    retry_keywords = (
        "rate", "limit", "quota", "timeout", "timed out", "connect", "overloaded",
        "capacity", "exhausted", "temporarily unavailable", "try again",
        "credit", "resource has been exhausted", "service unavailable"
    )
    return any(k in err_str for k in retry_keywords)


def resolve_default_model(base_url: Optional[str], model: Optional[str]) -> str:
    """Return the configured platform model, allowing an explicit override."""

    return (model or "").strip() or Config.LLM_MODEL_NAME


from dataclasses import dataclass

@dataclass
class LLMTarget:
    client: OpenAI
    model: str
    base_url: str
    name: str


class LLMClient:
    """LLM客户端，支持多 Provider 负载均衡与自动跨 Provider 故障转移"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = api_key or Config.LLM_API_KEY
        self.base_url = base_url or Config.LLM_BASE_URL
        self.model = resolve_default_model(self.base_url, model)
        
        if not self.api_key:
            raise ValueError("LLM_API_KEY 未配置")
        
        self.api_keys = [k.strip() for k in self.api_key.split(",") if k.strip()]
        if not self.api_keys:
            raise ValueError("LLM_API_KEY 未配置有效密钥")

        default_headers = {}
        if self.base_url and "openrouter.ai" in self.base_url.lower():
            default_headers = {
                "HTTP-Referer": "https://brain.obrive.com",
                "X-Title": "Brain"
            }
            
        self.clients = [
            OpenAI(api_key=k, base_url=self.base_url, default_headers=default_headers or None)
            for k in self.api_keys
        ]
        self._key_index = 0
        self.client = self.clients[0]

        # 注册多 Provider 目标池（支持通用 LLM、加速 LLM、备份 LLM 组合）
        self.targets: List[LLMTarget] = []
        for idx, client in enumerate(self.clients):
            self.targets.append(LLMTarget(
                client=client,
                model=self.model,
                base_url=self.base_url or "",
                name=f"Primary-{idx+1}"
            ))

        # 仅在使用全局系统配置时挂载 Boost 和 Backup Provider
        if api_key is None:
            boost_key = getattr(Config, "LLM_BOOST_API_KEY", None)
            if boost_key:
                boost_base = getattr(Config, "LLM_BOOST_BASE_URL", None) or "https://api.mistral.ai/v1"
                boost_model = (
                    getattr(Config, "LLM_BOOST_MODEL_NAME", None)
                    or ("open-mistral-nemo" if "mistral" in boost_base.lower() else self.model)
                )
                for b_idx, bk in enumerate([k.strip() for k in boost_key.split(",") if k.strip()]):
                    self.targets.append(LLMTarget(
                        client=OpenAI(api_key=bk, base_url=boost_base),
                        model=boost_model,
                        base_url=boost_base,
                        name=f"Boost-{b_idx+1}"
                    ))
            
            backup_key = getattr(Config, "LLM_BACKUP_API_KEY", None)
            if backup_key:
                backup_base = getattr(Config, "LLM_BACKUP_BASE_URL", None) or "https://integrate.api.nvidia.com/v1"
                backup_model = (
                    getattr(Config, "LLM_BACKUP_MODEL_NAME", None)
                    or ("minimaxai/minimax-m3.1-flash" if "nvidia" in backup_base.lower() else self.model)
                )
                for bk_idx, bkk in enumerate([k.strip() for k in backup_key.split(",") if k.strip()]):
                    self.targets.append(LLMTarget(
                        client=OpenAI(api_key=bkk, base_url=backup_base),
                        model=backup_model,
                        base_url=backup_base,
                        name=f"Backup-{bk_idx+1}"
                    ))

            fallback_key = getattr(Config, "LLM_FALLBACK_API_KEY", None)
            if fallback_key:
                fallback_base = getattr(Config, "LLM_FALLBACK_BASE_URL", None) or "https://openrouter.ai/api/v1"
                fallback_model = getattr(Config, "LLM_FALLBACK_MODEL_NAME", None) or "nvidia/nemotron-3.5-lightning:free"
                fb_headers = {}
                if "openrouter.ai" in fallback_base.lower():
                    fb_headers = {
                        "HTTP-Referer": "https://brain.obrive.com",
                        "X-Title": "Brain"
                    }
                for fb_idx, fbk in enumerate([k.strip() for k in fallback_key.split(",") if k.strip()]):
                    self.targets.append(LLMTarget(
                        client=OpenAI(api_key=fbk, base_url=fallback_base, default_headers=fb_headers or None),
                        model=fallback_model,
                        base_url=fallback_base,
                        name=f"Fallback-{fb_idx+1}"
                    ))

    def _create_completion(
        self,
        *,
        messages: List[Dict[str, str]],
        temperature: Optional[float],
        max_tokens: Optional[int],
        response_format: Optional[Dict[str, Any]],
    ) -> Any:
        base_url = getattr(self, "base_url", None)
        fallback_model = resolve_default_model(base_url, None)
        
        # 优先使用多 Provider Target 池
        targets = getattr(self, "targets", None)
        if targets and len(targets) > 1:
            num_targets = len(targets)
            max_attempts = num_targets * 2
            last_error = None
            for attempt in range(max_attempts):
                idx = (getattr(self, "_key_index", 0) + attempt) % num_targets
                target = targets[idx]
                try:
                    return create_chat_completion(
                        target.client,
                        model=target.model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        response_format=response_format,
                    )
                except Exception as err:
                    last_error = err
                    is_retryable = is_retryable_llm_error(err)
                    if is_retryable and attempt < max_attempts - 1:
                        import time
                        import random
                        backoff = min(2.0 ** (attempt % num_targets) + random.uniform(0.1, 0.4), 4.0)
                        next_target = targets[(idx + 1) % num_targets]
                        logger.warning(
                            "LLM Target '%s' (%s) transient or quota/rate error (%s: %s); failing over to '%s' (%s) in %.1fs...",
                            target.name,
                            target.model,
                            type(err).__name__,
                            str(err)[:100],
                            next_target.name,
                            next_target.model,
                            backoff,
                        )
                        time.sleep(backoff)
                        continue
                    raise
            if last_error:
                raise last_error

        clients = getattr(self, "clients", [self.client])
        num_clients = len(clients)
        if num_clients <= 1:
            try:
                return create_chat_completion(
                    self.client,
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format=response_format,
                )
            except Exception as e:
                err_str = str(e).lower()
                if ("model_not_found" in err_str or "does not exist" in err_str or "404" in err_str) and self.model != fallback_model:
                    logger.warning(f"Model '{self.model}' not found on provider ({base_url}). Auto-falling back to baseline model '{fallback_model}'.")
                    self.model = fallback_model
                    return create_chat_completion(
                        self.client,
                        model=self.model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        response_format=response_format,
                    )
                raise

        max_attempts = num_clients * 2
        last_error = None
        for attempt in range(max_attempts):
            idx = (getattr(self, "_key_index", 0) + attempt) % num_clients
            client = clients[idx]
            try:
                return create_chat_completion(
                    client,
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format=response_format,
                )
            except Exception as err:
                last_error = err
                is_retryable = is_retryable_llm_error(err)
                if is_retryable and attempt < max_attempts - 1:
                    import time
                    import random
                    backoff = min(2.0 ** attempt + random.uniform(0.1, 0.5), 5.0)
                    logger.warning(
                        "LLM Key #%d request failed with %s (%s); rotating and retrying in %.1fs...",
                        idx + 1,
                        type(err).__name__,
                        str(err)[:100],
                        backoff,
                    )
                    time.sleep(backoff)
                    continue
                raise
        if last_error:
            raise last_error
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = 4096,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            response_format: 响应格式（如JSON模式）
            
        Returns:
            模型响应文本
        """
        response = self._create_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format,
        )
        content = extract_chat_completion_text(response)
        return _clean_chat_text(content)
    
    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: Optional[int] = 4096,
        max_attempts: int = 1,
    ) -> Dict[str, Any]:
        """
        发送聊天请求并返回JSON
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            max_attempts: 内容生成尝试次数（不含一次明确的JSON模式能力降级）
            
        Returns:
            解析后的JSON对象
        """
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        response_format: Optional[Dict[str, str]] = {"type": "json_object"}
        request_max_tokens = max_tokens
        last_error: Optional[LLMResponseError] = None

        for attempt in range(1, max_attempts + 1):
            # JSON-mode capability negotiation is separate from content
            # regeneration. An explicit response_format rejection may add one
            # request, but it must not consume a content attempt.
            while True:
                try:
                    response = self._create_completion(
                        messages=messages,
                        temperature=temperature,
                        max_tokens=request_max_tokens,
                        response_format=response_format,
                    )
                except Exception as error:
                    details = _extract_error_details(error)
                    if isinstance(details, dict) and "failed_generation" in details:
                        raw = str(details.get("failed_generation") or "")
                        if raw:
                            try:
                                recovered, _ = json.JSONDecoder().raw_decode(_clean_chat_text(raw))
                                if isinstance(recovered, dict) and recovered:
                                    logger.info("Successfully recovered JSON from provider failed_generation payload")
                                    return recovered
                            except Exception:
                                pass

                    if (
                        response_format is not None
                        and _is_response_format_unsupported(error)
                    ):
                        logger.warning(
                            "LLM provider explicitly rejected or failed response_format; "
                            "retrying once with prompt-only JSON guidance"
                        )
                        response_format = None
                        continue
                    raise
                break

            try:
                return self._parse_json_response(response)
            except LLMResponseError as error:
                last_error = error
                if attempt >= max_attempts:
                    raise

                if error.finish_reason == "length":
                    request_max_tokens = None
                logger.warning(
                    "LLM returned unusable JSON (finish_reason=%s); "
                    "retrying content generation with max_tokens=%s",
                    error.finish_reason or "unknown",
                    request_max_tokens,
                )

        if last_error is not None:  # pragma: no cover - defensive loop guard
            raise last_error
        raise LLMResponseError("LLM did not produce a JSON response")

    @staticmethod
    def _parse_json_response(response: Any) -> Dict[str, Any]:
        choices = getattr(response, "choices", None) or []
        if not choices:
            raise LLMResponseError("LLM returned no choices")

        choice = choices[0]
        finish_reason = getattr(choice, "finish_reason", None)
        if finish_reason == "length":
            content = _clean_chat_text(extract_chat_completion_text(response))
            if content:
                try:
                    value, _ = json.JSONDecoder().raw_decode(content)
                    if isinstance(value, dict) and value:
                        return value
                except Exception:
                    pass
            raise LLMResponseError(
                "LLM JSON output was truncated at the token limit",
                finish_reason=finish_reason,
            )
        if finish_reason not in {None, "stop"}:
            raise LLMResponseError(
                f"LLM JSON generation stopped unexpectedly ({finish_reason})",
                finish_reason=finish_reason,
            )

        content = _clean_chat_text(extract_chat_completion_text(response))
        if not content:
            raise LLMResponseError(
                "LLM returned empty JSON content",
                finish_reason=finish_reason,
            )

        try:
            value = json.loads(content)
        except json.JSONDecodeError as strict_error:
            # Some compatible providers append a short explanation after an
            # otherwise complete JSON object. Accept only an object decoded
            # from the beginning; never repair or invent truncated JSON.
            try:
                value, end = json.JSONDecoder().raw_decode(content)
            except json.JSONDecodeError:
                raise LLMResponseError(
                    "LLM returned invalid JSON "
                    f"(line {strict_error.lineno}, column {strict_error.colno})",
                    finish_reason=finish_reason,
                ) from strict_error

            trailing = content[end:].strip()
            if trailing:
                if _contains_additional_json_container(trailing):
                    raise LLMResponseError(
                        "LLM returned multiple JSON values",
                        finish_reason=finish_reason,
                    )
                logger.warning("Ignoring text after a complete LLM JSON object")

        if not isinstance(value, dict):
            raise LLMResponseError(
                "LLM JSON response must be a top-level JSON object",
                finish_reason=finish_reason,
            )

        return value
