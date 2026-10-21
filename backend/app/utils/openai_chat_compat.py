"""
OpenAI Chat Completions compatibility helpers.

This module keeps existing behavior for legacy models/providers while
gracefully adapting request parameters for GPT-5 family models.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def is_gpt5_family(model: Optional[str]) -> bool:
    """Return True when model belongs to GPT-5 family aliases/snapshots."""
    if not model:
        return False
    return model.strip().lower().startswith("gpt-5")


def create_chat_completion(
    client: Any,
    *,
    model: str,
    messages: List[Dict[str, Any]],
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    response_format: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Create a chat completion with model-specific request parameters.

    Compatibility strategy:
    - For GPT-5 family, avoid sending temperature by default.
    - For token limit, use `max_completion_tokens` on GPT-5, `max_tokens` otherwise.
    - Preserve the legacy request shape for every non-GPT-5 model/provider.
    - Propagate provider errors unchanged instead of guessing from message text.
    """
    kwargs: Dict[str, Any] = {
        "model": model,
        "messages": messages,
    }

    if response_format is not None:
        kwargs["response_format"] = response_format
    else:
        # Provide fallback tool schemas so providers like Groq accept
        # model-emitted tool calls without throwing "Tool choice is none" or "tool not in request.tools"
        kwargs["tools"] = [
            {
                "type": "function",
                "function": {
                    "name": "insight_forge",
                    "description": "Deep insight search and question decomposition analysis",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "report_context": {"type": "string"},
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "panorama_search",
                    "description": "Wide-angle event timeline and overview search",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "quick_search",
                    "description": "Quick search for specific facts",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "interview_agents",
                    "description": "Interview simulated agents for firsthand opinions",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "agent_names": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": ["question"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "tool_call",
                    "description": "Generic tool invocation",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "parameters": {"type": "object"},
                        },
                    },
                },
            },
        ]

    gpt5_family = is_gpt5_family(model)

    if temperature is not None and not gpt5_family:
        kwargs["temperature"] = temperature

    if max_tokens is not None:
        if gpt5_family:
            kwargs["max_completion_tokens"] = max_tokens
        else:
            kwargs["max_tokens"] = max_tokens

    return client.chat.completions.create(**kwargs)


def extract_chat_completion_text(response: Any) -> str:
    """Extract plain text from chat completion response across SDK content shapes."""
    import json

    choices = getattr(response, "choices", None) or []
    if not choices:
        return ""

    message = getattr(choices[0], "message", None)
    if message is None:
        return ""

    content = getattr(message, "content", "")

    # Check if native tool_calls were emitted by the model
    tool_calls = getattr(message, "tool_calls", None)
    if tool_calls:
        tool_call_strs: List[str] = []
        for tc in tool_calls:
            func = getattr(tc, "function", None)
            name = getattr(func, "name", "unknown")
            args_str = getattr(func, "arguments", "{}")
            try:
                args_dict = json.loads(args_str)
            except Exception:
                args_dict = {"query": str(args_str)}

            if name == "tool_call" and "name" in args_dict and "parameters" in args_dict:
                call_data = args_dict
            else:
                call_data = {"name": name, "parameters": args_dict}

            call_json = json.dumps(call_data, ensure_ascii=False)
            tool_call_strs.append(f"<tool_call>\n{call_json}\n</tool_call>")
        if tool_call_strs:
            existing = content if isinstance(content, str) else ""
            return f"{existing}\n" + "\n".join(tool_call_strs)

    # Fallback to reasoning / reasoning_content if content is empty
    if not content:
        reasoning = getattr(message, "reasoning", None) or getattr(message, "reasoning_content", None)
        if reasoning:
            return str(reasoning)

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        chunks: List[str] = []
        for item in content:
            if isinstance(item, dict):
                text_obj = item.get("text")
                if isinstance(text_obj, dict):
                    text_obj = text_obj.get("value")
                if isinstance(text_obj, str):
                    chunks.append(text_obj)
                elif isinstance(item.get("content"), str):
                    chunks.append(item["content"])
                continue

            text_obj = getattr(item, "text", None)
            if isinstance(text_obj, dict):
                text_obj = text_obj.get("value")
            if isinstance(text_obj, str):
                chunks.append(text_obj)
                continue

            content_obj = getattr(item, "content", None)
            if isinstance(content_obj, str):
                chunks.append(content_obj)

        return "".join(chunks).strip()

    return str(content or "")
