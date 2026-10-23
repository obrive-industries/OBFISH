"""Unit tests for Zep Cloud multi-key pooling, rotation, and failover."""

import pytest
from zep_cloud.core.api_error import ApiError as ZepApiError

from app.config import Config
from app.services.graph_builder import GraphBuilderService
from app.utils import zep


@pytest.fixture(autouse=True)
def reset_pool_and_cache():
    """Ensure clean pool and client cache for every test."""
    zep.clear_zep_client_cache()
    yield
    zep.clear_zep_client_cache()


def test_config_parses_multiple_zep_keys(monkeypatch):
    """Verify Config.get_zep_api_keys extracts, deduplicates, and orders keys."""
    monkeypatch.setenv("ZEP_API_KEY", "key_alpha, key_beta")
    monkeypatch.setenv("ZEP_BACKUP_API_KEY", "key_gamma")
    monkeypatch.setattr(Config, "ZEP_API_KEY", "key_alpha, key_beta")
    monkeypatch.setattr(Config, "ZEP_BACKUP_API_KEY", "key_gamma")
    monkeypatch.setattr(Config, "ZEP_API_KEYS_ENV", None)

    keys = Config.get_zep_api_keys()
    assert keys == ["key_alpha", "key_beta", "key_gamma"]


def test_execute_with_zep_failover_rotates_on_quota_error(monkeypatch):
    """When the active key hits quota/payment error (402), failover immediately calls the backup key."""
    pool = zep.get_zep_key_pool()
    pool.set_keys(["key_1", "key_2"])

    calls = []

    def fake_operation(client, key):
        calls.append(key)
        if key == "key_1":
            raise ZepApiError(status_code=402, body={"message": "plan quota exceeded"})
        return f"success_from_{key}"

    result = zep.execute_with_zep_failover(
        fake_operation,
        operation_name="test_quota_failover",
    )

    assert result == "success_from_key_2"
    assert calls == ["key_1", "key_2"]
    # Key 1 was marked degraded, active key is now key_2
    assert pool.get_active_key() == "key_2"


def test_execute_with_zep_failover_probes_on_404_for_graph_id():
    """When a graph read gets 404 on Key 1, failover probes Key 2 and records the affinity."""
    pool = zep.get_zep_key_pool()
    pool.set_keys(["key_primary", "key_secondary"])

    calls = []

    def fake_operation(client, key):
        calls.append(key)
        if key == "key_primary":
            raise ZepApiError(status_code=404, body={"message": "graph not found"})
        return "graph_found"

    result = zep.execute_with_zep_failover(
        fake_operation,
        operation_name="fetch_graph",
        graph_id="brain_target_123",
    )

    assert result == "graph_found"
    assert calls == ["key_primary", "key_secondary"]
    # The pool remembers that brain_target_123 belongs to key_secondary
    assert pool.get_key_for_graph("brain_target_123") == "key_secondary"


def test_all_keys_exhausted_raises_last_error():
    """When all keys in the pool fail, the final exception is raised."""
    pool = zep.get_zep_key_pool()
    pool.set_keys(["key_a", "key_b"])

    calls = []

    def fake_operation(client, key):
        calls.append(key)
        raise ZepApiError(status_code=429, body={"message": f"rate limit on {key}"})

    with pytest.raises(ZepApiError) as exc_info:
        zep.execute_with_zep_failover(
            fake_operation,
            operation_name="test_all_exhausted",
        )

    assert exc_info.value.status_code == 429
    assert calls == ["key_a", "key_b"]


def test_graph_builder_create_graph_auto_failover_updates_client(monkeypatch):
    """GraphBuilderService.create_graph automatically fails over to backup key on quota limit."""
    pool = zep.get_zep_key_pool()
    pool.set_keys(["key_exhausted", "key_backup"])

    created_graphs = []

    class FakeGraphClient:
        def __init__(self, key):
            self.key = key

        def create(self, graph_id, name, description):
            if self.key == "key_exhausted":
                raise ZepApiError(status_code=402, body={"message": "payment required"})
            created_graphs.append((self.key, graph_id))

    class FakeClient:
        def __init__(self, key):
            self.graph = FakeGraphClient(key)

    monkeypatch.setattr(zep, "_cached_zep_client", lambda key, timeout: FakeClient(key))

    builder = GraphBuilderService(api_key="key_exhausted")
    assert builder.api_key == "key_exhausted"

    graph_id = builder.create_graph("Failover Graph")

    assert len(created_graphs) == 1
    assert created_graphs[0][0] == "key_backup"
    assert created_graphs[0][1] == graph_id
    # Builder updated its active api_key to the winning backup key
    assert builder.api_key == "key_backup"
    assert pool.get_key_for_graph(graph_id) == "key_backup"
