"""Shared Zep Cloud client, request limits, retry policy, and multi-key failover."""

from __future__ import annotations

import os
import threading
import time
from functools import lru_cache
from typing import Any, Callable, TypeVar

import httpx
from zep_cloud.client import Zep
from zep_cloud.core.api_error import ApiError as ZepApiError

from ..config import Config
from .logger import get_logger

logger = get_logger("brain.zep")

T = TypeVar("T")

ZEP_CLOUD_BASE_URL = "https://api.getzep.com/api/v2"
# Keep request behavior aligned with the zep-cloud 3.25.0 SDK default that
# Brain used before introducing the shared client. This is an internal
# integration policy, not a deployment setting users need to tune.
ZEP_HTTP_REQUEST_TIMEOUT_SECONDS = 60.0
# Zep ingestion is asynchronous and may take several minutes. Preserve the
# original GraphBuilder deadline while keeping it separate from HTTP timeout.
ZEP_INGESTION_WAIT_TIMEOUT_SECONDS = 600
MAX_ZEP_SEARCH_QUERY_CHARS = 400
MAX_ZEP_SEARCH_RESULTS = 50


class ZepKeyHealth:
    """Tracks health and cooldown state for a single Zep API key."""

    def __init__(self, key: str):
        self.key = key
        self.is_healthy: bool = True
        self.cooldown_until: float = 0.0
        self.consecutive_errors: int = 0
        self.last_error: str = ""
        self.status_code: int | None = None
        self.success_count: int = 0
        self.error_count: int = 0


class ZepKeyPool:
    """Thread-safe multi-key rotation and automatic failover manager for Zep Cloud."""

    def __init__(self, keys: list[str] | None = None):
        self._lock = threading.RLock()
        self._keys: list[str] = []
        self._health: dict[str, ZepKeyHealth] = {}
        self._active_index: int = 0
        self._graph_key_map: dict[str, str] = {}
        if keys:
            self.set_keys(keys)

    def set_keys(self, keys: list[str]) -> None:
        with self._lock:
            cleaned = []
            seen = set()
            for k in keys:
                item = k.strip()
                if item and item not in seen:
                    seen.add(item)
                    cleaned.append(item)
            self._keys = cleaned
            for k in cleaned:
                if k not in self._health:
                    self._health[k] = ZepKeyHealth(k)
            for k in list(self._health.keys()):
                if k not in seen:
                    del self._health[k]
            if self._active_index >= len(self._keys):
                self._active_index = 0

    @property
    def keys(self) -> list[str]:
        with self._lock:
            if not self._keys:
                self.set_keys(Config.get_zep_api_keys())
            return list(self._keys)

    def get_active_key(self) -> str:
        """Return the current healthy active key, auto-advancing past cooldowns."""
        with self._lock:
            if not self._keys:
                self.set_keys(Config.get_zep_api_keys())
            if not self._keys:
                fallback = (Config.ZEP_API_KEY or "").strip()
                if fallback:
                    self.set_keys([fallback])
            if not self._keys:
                raise ValueError("ZEP_API_KEY 未配置")

            now = time.time()
            # If current active key is healthy, return it
            current_k = self._keys[self._active_index]
            current_h = self._health.get(current_k)
            if current_h and current_h.cooldown_until <= now:
                return current_k

            # Otherwise, scan for any healthy key not on cooldown
            for offset in range(len(self._keys)):
                idx = (self._active_index + offset) % len(self._keys)
                k = self._keys[idx]
                h = self._health.get(k)
                if h and h.cooldown_until <= now:
                    self._active_index = idx
                    return k

            # If all keys are on cooldown, pick the key whose cooldown expires earliest
            best_idx, best_key = min(
                enumerate(self._keys),
                key=lambda item: self._health.get(item[1], ZepKeyHealth(item[1])).cooldown_until
            )
            self._active_index = best_idx
            return best_key

    def rotate_key(self, current_key: str | None = None, reason: str = "") -> str:
        """Switch active key to the next available key in the pool."""
        with self._lock:
            if not self._keys:
                self.set_keys(Config.get_zep_api_keys())
            if not self._keys:
                fallback = (Config.ZEP_API_KEY or "").strip()
                if fallback:
                    self.set_keys([fallback])
            if not self._keys:
                raise ValueError("ZEP_API_KEY 未配置")
            if len(self._keys) <= 1:
                return self._keys[0]

            old_key = current_key or self._keys[self._active_index]
            try:
                curr_idx = self._keys.index(old_key)
            except ValueError:
                curr_idx = self._active_index

            self._active_index = (curr_idx + 1) % len(self._keys)
            new_key = self._keys[self._active_index]
            logger.warning(
                "Zep API key failover: rotated from key ...%s to key ...%s (reason: %s)",
                old_key[-8:] if len(old_key) > 8 else "primary",
                new_key[-8:] if len(new_key) > 8 else "secondary",
                reason or "manual/failover",
            )
            return new_key

    def mark_key_success(self, key: str) -> None:
        """Record successful operation for this key."""
        with self._lock:
            h = self._health.get(key)
            if h:
                h.is_healthy = True
                h.consecutive_errors = 0
                h.success_count += 1

    def mark_key_degraded(
        self,
        key: str,
        *,
        status_code: int | None = None,
        error_msg: str = "",
        cooldown_seconds: float = 60.0,
    ) -> None:
        """Mark a key as temporarily or prolonged degraded due to rate limit or quota."""
        with self._lock:
            h = self._health.get(key)
            if not h:
                h = ZepKeyHealth(key)
                self._health[key] = h
            h.error_count += 1
            h.consecutive_errors += 1
            h.status_code = status_code
            h.last_error = error_msg
            h.cooldown_until = time.time() + cooldown_seconds
            h.is_healthy = False
            logger.warning(
                "Marked Zep key ...%s degraded for %.0fs (status=%s, error=%s)",
                key[-8:] if len(key) > 8 else key,
                cooldown_seconds,
                status_code,
                error_msg[:100],
            )

    def record_graph_key(self, graph_id: str, key: str) -> None:
        """Associate a graph ID with the Zep API key under which it was created."""
        if not graph_id or not key:
            return
        with self._lock:
            self._graph_key_map[graph_id] = key

    def get_key_for_graph(self, graph_id: str | None = None, default_key: str | None = None) -> str:
        """Return the API key associated with graph_id, or active pool key."""
        with self._lock:
            if graph_id and graph_id in self._graph_key_map:
                mapped = self._graph_key_map[graph_id]
                return mapped
            if default_key:
                return default_key
            return self.get_active_key()

    def reset(self) -> None:
        """Reset pool state. Intended for testing."""
        with self._lock:
            self._health.clear()
            self._graph_key_map.clear()
            self._active_index = 0
            self._keys = []


_zep_key_pool = ZepKeyPool()


def get_zep_key_pool() -> ZepKeyPool:
    """Return the global ZepKeyPool instance."""
    return _zep_key_pool


def normalize_zep_search_query(query: Any) -> str:
    """Return a non-empty query within Zep Cloud's endpoint limit."""

    if not isinstance(query, str):
        raise ValueError("Zep search query must be a string")
    normalized = query.strip()
    if not normalized:
        raise ValueError("Zep search query must not be empty")
    return normalized[:MAX_ZEP_SEARCH_QUERY_CHARS]


def normalize_zep_search_limit(limit: Any) -> int:
    """Clamp a search result limit to the current Zep Cloud contract."""

    try:
        normalized = int(limit)
    except (TypeError, ValueError) as exc:
        raise ValueError("Zep search limit must be an integer") from exc
    if normalized < 1:
        raise ValueError("Zep search limit must be at least 1")
    return min(normalized, MAX_ZEP_SEARCH_RESULTS)


@lru_cache(maxsize=8)
def _cached_zep_client(api_key: str, timeout: float) -> Zep:
    return Zep(
        api_key=api_key,
        base_url=ZEP_CLOUD_BASE_URL,
        timeout=timeout,
    )


def get_zep_client(api_key: str | None = None, timeout: float | None = None) -> Zep:
    """Return a process-shared, explicitly configured Zep Cloud client."""

    # zep-cloud gives ZEP_API_URL precedence even when base_url is explicit.
    # Reject it so this Cloud-only integration cannot silently target a
    # self-hosted or compatibility endpoint.
    if os.environ.get("ZEP_API_URL"):
        raise ValueError("ZEP_API_URL is unsupported; unset it to use Zep Cloud")

    normalized_key = (api_key or "").strip()
    if not normalized_key:
        try:
            normalized_key = _zep_key_pool.get_active_key()
        except ValueError:
            normalized_key = (Config.ZEP_API_KEY or "").strip()

    if not normalized_key:
        raise ValueError("ZEP_API_KEY 未配置")

    request_timeout = float(
        timeout if timeout is not None else ZEP_HTTP_REQUEST_TIMEOUT_SECONDS
    )
    if request_timeout <= 0:
        raise ValueError("Zep request timeout must be greater than 0")
    return _cached_zep_client(normalized_key, request_timeout)


def clear_zep_client_cache() -> None:
    """Clear cached clients and pool state. Intended for tests and reconfiguration."""

    _cached_zep_client.cache_clear()
    _zep_key_pool.reset()


def is_retryable_zep_error(error: BaseException) -> bool:
    """Return whether a failed *read* is safe and useful to retry."""

    if isinstance(error, (httpx.TimeoutException, httpx.TransportError)):
        return True
    if isinstance(error, (ConnectionError, TimeoutError, OSError)):
        return True
    if isinstance(error, ZepApiError):
        status_code = error.status_code
        return status_code in {408, 429} or (
            status_code is not None and 500 <= status_code <= 599
        )
    return False


def is_quota_or_rate_limit_error(error: BaseException) -> bool:
    """Return whether an error indicates rate limiting (429) or quota exhaustion (402/403)."""

    if isinstance(error, ZepApiError):
        code = error.status_code
        if code in {402, 429}:
            return True
        if code == 403:
            msg = str(error.body or "").lower()
            if any(term in msg for term in ("quota", "limit", "payment", "credits", "plan", "exhausted")):
                return True
    err_str = str(error).lower()
    quota_terms = (
        "rate limit", "ratelimit", "too many requests",
        "quota", "quota exceeded", "limit reached", "limit exceeded",
        "credits", "insufficient credits", "payment required",
        "resource exhausted", "plan limit", "upgrade your plan",
    )
    return any(term in err_str for term in quota_terms)


def _retry_after_seconds(error: BaseException) -> float | None:
    if not isinstance(error, ZepApiError) or not error.headers:
        return None
    value = next(
        (
            header_value
            for header_name, header_value in error.headers.items()
            if header_name.lower() == "retry-after"
        ),
        None,
    )
    if value is None:
        return None
    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return None


def execute_with_zep_failover(
    operation: Callable[[Zep, str], T],
    *,
    operation_name: str,
    graph_id: str | None = None,
    preferred_key: str | None = None,
    timeout: float | None = None,
) -> T:
    """Execute a Zep operation with automatic multi-key failover across the key pool."""

    pool = get_zep_key_pool()
    all_keys = pool.keys
    if not all_keys:
        all_keys = Config.get_zep_api_keys()
        pool.set_keys(all_keys)
    if not all_keys:
        fallback = (Config.ZEP_API_KEY or "").strip()
        if fallback:
            all_keys = [fallback]
            pool.set_keys(all_keys)
    if not all_keys:
        raise ValueError("ZEP_API_KEY 未配置")

    # Start with preferred key or mapped key for graph_id or current active key
    start_key = preferred_key or pool.get_key_for_graph(graph_id)
    ordered_keys = [start_key] + [k for k in all_keys if k != start_key]

    last_error: BaseException | None = None
    for attempt_idx, key in enumerate(ordered_keys):
        try:
            client = get_zep_client(key, timeout=timeout)
            result = operation(client, key)
            pool.mark_key_success(key)
            if graph_id:
                pool.record_graph_key(graph_id, key)
            return result
        except Exception as err:
            last_error = err
            # If graph_id got 404, check other keys in case the graph was created on another key
            is_404 = (
                isinstance(err, ZepApiError) and err.status_code == 404
            ) or ("not found" in str(err).lower() and isinstance(err, ZepApiError))
            if is_404 and graph_id and attempt_idx < len(ordered_keys) - 1:
                logger.info(
                    "Zep %s got 404 for graph %s on key ...%s; trying alternative key in pool...",
                    operation_name,
                    graph_id,
                    key[-8:] if len(key) > 8 else "key",
                )
                continue

            # Check if quota or rate limit error
            if is_quota_or_rate_limit_error(err) and attempt_idx < len(ordered_keys) - 1:
                is_quota = (
                    isinstance(err, ZepApiError) and err.status_code in {402, 403}
                ) or ("quota" in str(err).lower())
                cooldown = 3600.0 if is_quota else 60.0
                pool.mark_key_degraded(
                    key,
                    status_code=getattr(err, "status_code", None),
                    error_msg=str(err),
                    cooldown_seconds=cooldown,
                )
                next_key = pool.rotate_key(
                    current_key=key,
                    reason=f"{operation_name} failed ({type(err).__name__}: {err})",
                )
                logger.warning(
                    "Zep operation %s failed on key ...%s with %s. Automatically failed over to key ...%s.",
                    operation_name,
                    key[-8:] if len(key) > 8 else "primary",
                    type(err).__name__,
                    next_key[-8:] if len(next_key) > 8 else "secondary",
                )
                continue

            raise

    if last_error is not None:
        raise last_error
    raise AssertionError("unreachable")


def call_zep_read_with_retry(
    operation: Callable[[], T],
    *,
    operation_name: str,
    max_attempts: int = 3,
    initial_delay: float = 2.0,
    max_delay: float = 60.0,
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    """Retry a safe Zep read only for transport, 408, 429, or 5xx errors."""

    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except Exception as error:
            if attempt == max_attempts or not is_retryable_zep_error(error):
                raise

            retry_after = _retry_after_seconds(error)
            delay = min(
                retry_after if retry_after is not None else initial_delay * (2 ** (attempt - 1)),
                max_delay,
            )
            logger.warning(
                "Zep %s attempt %s/%s failed (%s); retrying in %.1fs",
                operation_name,
                attempt,
                max_attempts,
                type(error).__name__,
                delay,
            )
            sleep(delay)

    raise AssertionError("unreachable")
