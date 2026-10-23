"""
Universal BYOK (Bring Your Own Key) Provider Detection & Probing Utility.
Supports: OpenRouter, NVIDIA NIM, Alibaba Cloud (DashScope), Groq, OpenAI,
Google Gemini, DeepSeek, Cerebras, Perplexity, Together AI, Mistral, and custom endpoints.
"""

import os
import re
from typing import Dict, Any, Optional, List
import requests
from ..config import Config
from .logger import get_logger

logger = get_logger('obmind.byok_detector')

PROVIDERS: Dict[str, Dict[str, Any]] = {
    "openrouter": {
        "name": "OpenRouter",
        "prefixes": ["sk-or-v1-", "sk-or-"],
        "base_url": "https://openrouter.ai/api/v1",
        "default_model": "openai/gpt-4o-mini",
        "candidate_models": [
            "google/gemma-4-26b-a4b-it:free",
            "openai/gpt-4o-mini",
            "google/gemini-2.0-flash-001",
            "meta-llama/llama-3.3-70b-instruct",
            "anthropic/claude-3.5-haiku"
        ],
        "headers": {
            "HTTP-Referer": "https://brain.obrive.com",
            "X-Title": "Brain"
        }
    },
    "nvidia": {
        "name": "NVIDIA NIM",
        "prefixes": ["nvapi-"],
        "base_url": "https://integrate.api.nvidia.com/v1",
        "default_model": "meta/llama-3.1-8b-instruct",
        "candidate_models": [
            "meta/llama-3.1-8b-instruct",
            "nvidia/llama-3.1-nemotron-70b-instruct",
            "meta/llama-3.3-70b-instruct"
        ],
        "headers": {}
    },
    "alibaba": {
        "name": "Alibaba Cloud (DashScope)",
        "prefixes": ["qwen-"],
        "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        "default_model": "qwen-plus",
        "candidate_models": [
            "qwen-plus",
            "qwen-turbo",
            "qwen-max"
        ],
        "headers": {}
    },
    "groq": {
        "name": "Groq",
        "prefixes": ["gsk_"],
        "base_url": "https://api.groq.com/openai/v1",
        "default_model": "openai/gpt-oss-20b",
        "candidate_models": [
            "openai/gpt-oss-20b",
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile"
        ],
        "headers": {}
    },
    "gemini": {
        "name": "Google Gemini",
        "prefixes": ["AIzaSy"],
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "default_model": "gemini-1.5-flash",
        "candidate_models": [
            "gemini-1.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-pro"
        ],
        "headers": {}
    },
    "perplexity": {
        "name": "Perplexity",
        "prefixes": ["pplx-"],
        "base_url": "https://api.perplexity.ai",
        "default_model": "sonar",
        "candidate_models": [
            "sonar",
            "sonar-pro"
        ],
        "headers": {}
    },
    "cerebras": {
        "name": "Cerebras",
        "prefixes": ["csk-"],
        "base_url": "https://api.cerebras.ai/v1",
        "default_model": "llama3.1-8b",
        "candidate_models": [
            "llama3.1-8b",
            "llama3.1-70b"
        ],
        "headers": {}
    },
    "together": {
        "name": "Together AI",
        "prefixes": ["together-"],
        "base_url": "https://api.together.xyz/v1",
        "default_model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "candidate_models": [
            "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "mistralai/Mixtral-8x7B-Instruct-v0.1"
        ],
        "headers": {}
    },
    "mistral": {
        "name": "Mistral AI",
        "prefixes": ["mistral-"],
        "base_url": "https://api.mistral.ai/v1",
        "default_model": "mistral-small-latest",
        "candidate_models": [
            "mistral-small-latest",
            "mistral-large-latest"
        ],
        "headers": {}
    },
    "deepseek": {
        "name": "DeepSeek",
        "prefixes": [],
        "base_url": "https://api.deepseek.com/v1",
        "default_model": "deepseek-chat",
        "candidate_models": [
            "deepseek-chat",
            "deepseek-reasoner"
        ],
        "headers": {}
    },
    "openai": {
        "name": "OpenAI",
        "prefixes": ["sk-proj-", "sk-admin-", "sk-"],
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o-mini",
        "candidate_models": [
            "gpt-4o-mini",
            "gpt-4o"
        ],
        "headers": {}
    }
}


def detect_provider_from_key(api_key: Optional[str], hint_provider: Optional[str] = None) -> Dict[str, Any]:
    """
    Detect provider, official Base URL, and optimal default model from an API key or explicit hint.
    """
    cleaned_key = (api_key or "").strip()
    hint = (hint_provider or "").strip().lower()

    # 1. If explicit hint matches a known provider, prioritize it
    if hint in PROVIDERS:
        cfg = PROVIDERS[hint]
        return {
            "provider": hint,
            "name": cfg["name"],
            "base_url": cfg["base_url"],
            "default_model": cfg["default_model"],
            "candidate_models": cfg["candidate_models"],
            "headers": cfg["headers"]
        }

    # 2. Match prefixes (order matters: check specific prefixes first before generic sk-)
    for provider_key, cfg in PROVIDERS.items():
        if provider_key == "openai":
            continue  # Check generic OpenAI last
        for prefix in cfg["prefixes"]:
            if cleaned_key.startswith(prefix):
                return {
                    "provider": provider_key,
                    "name": cfg["name"],
                    "base_url": cfg["base_url"],
                    "default_model": cfg["default_model"],
                    "candidate_models": cfg["candidate_models"],
                    "headers": cfg["headers"]
                }

    # 3. Check generic sk- prefixes
    if cleaned_key.startswith("sk-"):
        cfg = PROVIDERS["openai"]
        return {
            "provider": "openai",
            "name": cfg["name"],
            "base_url": cfg["base_url"],
            "default_model": cfg["default_model"],
            "candidate_models": cfg["candidate_models"],
            "headers": cfg["headers"]
        }

    # 4. Fallback for unrecognized keys
    return {
        "provider": "custom",
        "name": "Custom Provider",
        "base_url": Config.LLM_BASE_URL or "https://api.openai.com/v1",
        "default_model": Config.LLM_MODEL_NAME or "gpt-4o-mini",
        "candidate_models": [],
        "headers": {}
    }


def resolve_model_for_base_url(base_url: Optional[str], requested_model: Optional[str]) -> str:
    """Resolve default model for any given base_url."""
    if requested_model and str(requested_model).strip():
        return str(requested_model).strip()
    
    url = (base_url or "").lower()
    if "integrate.api.nvidia.com" in url or "nvidia.com" in url:
        return "meta/llama-3.1-8b-instruct"
    if "aliyuncs.com" in url or "dashscope" in url:
        return "qwen-plus"
    if "openrouter.ai" in url:
        return "openai/gpt-4o-mini"
    if "groq.com" in url:
        return Config.LLM_MODEL_NAME or "openai/gpt-oss-20b"
    if "generativelanguage.googleapis.com" in url:
        return "gemini-1.5-flash"
    if "deepseek.com" in url:
        return "deepseek-chat"
    if "perplexity.ai" in url:
        return "sonar"
    if "cerebras.ai" in url:
        return "llama3.1-8b"
    if "together.xyz" in url:
        return "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    if "mistral.ai" in url:
        return "mistral-small-latest"
    
    return Config.LLM_MODEL_NAME or "gpt-4o-mini"


def probe_llm_key(
    api_key: str,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
    hint_provider: Optional[str] = None,
    timeout: int = 8
) -> Dict[str, Any]:
    """
    Live probe an API key against provider.
    1. Resolves provider, base_url, and model.
    2. Probes provider's /models endpoint to inspect availability.
    3. Runs a fast 1-token test completion to guarantee key and model work.
    """
    key = (api_key or "").strip()
    if not key:
        return {"success": False, "error": "API key cannot be empty."}

    detected = detect_provider_from_key(key, hint_provider=hint_provider)
    resolved_base_url = (base_url or "").strip() or detected["base_url"]
    resolved_model = (model or "").strip() or resolve_model_for_base_url(resolved_base_url, detected["default_model"])

    req_headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    if detected.get("headers"):
        req_headers.update(detected["headers"])

    available_models: List[str] = []

    # Step 1: Probe /models endpoint (if supported)
    try:
        models_url = resolved_base_url.rstrip("/") + "/models"
        resp = requests.get(models_url, headers=req_headers, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
                available_models = [m["id"] for m in data["data"] if isinstance(m, dict) and "id" in m]
    except Exception as e:
        logger.debug(f"/models probe note: {e}")

    # If the user's requested model is not in available_models and we have a list, pick optimal
    if available_models and resolved_model not in available_models:
        # Check if our default candidate models exist in available_models
        matched_model = None
        for candidate in detected.get("candidate_models", []):
            if candidate in available_models:
                matched_model = candidate
                break
        if not matched_model:
            # Pick first chat model containing keywords or first model
            for m in available_models:
                m_lower = m.lower()
                if any(k in m_lower for k in ("mini", "flash", "chat", "plus", "turbo", "8b")):
                    matched_model = m
                    break
        if matched_model:
            logger.info(f"Adjusted model from {resolved_model} to provider-active model {matched_model}")
            resolved_model = matched_model

    # Step 2: Test 1-token completion
    test_url = resolved_base_url.rstrip("/") + "/chat/completions"
    test_payload = {
        "model": resolved_model,
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 1
    }

    try:
        chat_resp = requests.post(test_url, headers=req_headers, json=test_payload, timeout=timeout)
        if chat_resp.status_code == 200:
            return {
                "success": True,
                "provider": detected["provider"],
                "provider_name": detected["name"],
                "base_url": resolved_base_url,
                "model": resolved_model,
                "available_models": available_models[:15],
                "message": f"Verified successfully with {detected['name']} using model {resolved_model}!"
            }
        else:
            err_text = chat_resp.text[:200]
            logger.warning(f"Probe chat failed with status {chat_resp.status_code}: {err_text}")
            return {
                "success": False,
                "provider": detected["provider"],
                "provider_name": detected["name"],
                "base_url": resolved_base_url,
                "model": resolved_model,
                "error": f"Provider responded with status {chat_resp.status_code}: {err_text}"
            }
    except Exception as e:
        logger.error(f"Probe exception: {e}")
        return {
            "success": False,
            "provider": detected["provider"],
            "provider_name": detected["name"],
            "base_url": resolved_base_url,
            "model": resolved_model,
            "error": f"Connection error: {str(e)}"
        }
