"""
Comprehensive verification test suite for Brain:
1. Multi-tenancy data isolation (projects, simulations, reports)
2. Email verification simulation barrier (ontology, prepare, start, report)
3. BYOK (Bring Your Own Key) injection into subprocess and LLM clients
"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock
from app import create_app
from app.models.user import db, User
from app.models.project import ProjectManager, Project
from app.models.task import TaskManager
from app.services.simulation_manager import SimulationManager, SimulationState, SimulationStatus
from app.services.report_agent import ReportManager, Report, ReportStatus
from app.services.simulation_runner import SimulationRunner
from app.utils.auth_middleware import get_user_llm_client, check_simulation_permission


from app.config import Config


@pytest.fixture
def app_instance(tmp_path):
    """Create test application with isolated test database and directories."""
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_path}/test_auth.db"
        JWT_SECRET_KEY = "test-jwt-secret-key-123456"
        REQUIRE_BYOK = False

    app = create_app(TestConfig)

    # Set isolated directories
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir(parents=True, exist_ok=True)
    sim_dir = tmp_path / "simulations"
    sim_dir.mkdir(parents=True, exist_ok=True)
    rep_dir = tmp_path / "reports"
    rep_dir.mkdir(parents=True, exist_ok=True)

    with app.app_context():
        db.create_all()
        yield app, tmp_path
        db.session.remove()
        db.drop_all()


def _auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_user_registration_and_verification_barrier(app_instance, monkeypatch):
    app, tmp_path = app_instance
    client = app.test_client()

    with patch("app.services.email_service.send_verification_email", return_value=True):
        # 1. Register unverified user
        reg_res = client.post("/api/auth/register", json={
            "email": "customer@example.com",
            "password": "SecurePassword123!",
            "full_name": "Customer One"
        })
        assert reg_res.status_code == 201
        data = reg_res.get_json()
        token = data["access_token"]
        assert data["user"]["is_verified"] is False

    # 2. Try to start simulation as unverified user -> should be 403 EMAIL_NOT_VERIFIED
    sim_res = client.post(
        "/api/simulation/start",
        headers=_auth_header(token),
        json={"simulation_id": "sim_test", "platform": "parallel"}
    )
    assert sim_res.status_code == 403
    assert sim_res.get_json()["code"] == "EMAIL_NOT_VERIFIED"

    # 3. Verify user's email
    with app.app_context():
        user = User.query.filter_by(email="customer@example.com").first()
        verify_token = user.verification_token

    ver_res = client.post("/api/auth/verify-email", json={"token": verify_token})
    assert ver_res.status_code == 200
    assert ver_res.get_json()["user"]["is_verified"] is True

    # 4. Check simulation permission now passes
    with app.app_context():
        user = User.query.filter_by(email="customer@example.com").first()
        allowed, reason = check_simulation_permission(user)
        assert allowed is True
        assert reason is None

        # 5. Check BYOK requirement when REQUIRE_BYOK is True
        app.config["REQUIRE_BYOK"] = True
        byok_allowed, byok_reason = check_simulation_permission(user)
        assert byok_allowed is False
        assert "LLM API Key required" in byok_reason

        # Set custom BYOK key and confirm permission passes
        user.custom_llm_api_key = "sk-test-custom-byok-key-999"
        db.session.commit()
        byok_allowed_ok, byok_reason_ok = check_simulation_permission(user)
        assert byok_allowed_ok is True
        assert byok_reason_ok is None
        app.config["REQUIRE_BYOK"] = False


def test_multitenancy_project_and_history_isolation(app_instance, monkeypatch):
    app, tmp_path = app_instance
    client = app.test_client()

    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))
    monkeypatch.setattr(SimulationManager, "SIMULATION_DATA_DIR", str(tmp_path / "simulations"))
    monkeypatch.setattr(ReportManager, "REPORTS_DIR", str(tmp_path / "reports"))

    # Register and verify User A
    with patch("app.services.email_service.send_verification_email", return_value=True):
        res_a = client.post("/api/auth/register", json={
            "email": "a@domain.com",
            "password": "Password123!",
            "full_name": "User A"
        })
        token_a = res_a.get_json()["access_token"]
        user_a_id = res_a.get_json()["user"]["id"]

        res_b = client.post("/api/auth/register", json={
            "email": "b@domain.com",
            "password": "Password123!",
            "full_name": "User B"
        })
        token_b = res_b.get_json()["access_token"]
        user_b_id = res_b.get_json()["user"]["id"]

    # Verify both users
    with app.app_context():
        for uid in (user_a_id, user_b_id):
            u = db.session.get(User, uid)
            u.is_verified = True
        db.session.commit()

    # User A creates a project
    proj_a = ProjectManager.create_project(name="Project of A", user_id=user_a_id)
    # User B creates a project
    proj_b = ProjectManager.create_project(name="Project of B", user_id=user_b_id)

    # 1. User A lists projects -> sees ONLY proj_a
    list_a = client.get("/api/graph/project/list", headers=_auth_header(token_a)).get_json()["data"]
    assert len(list_a) == 1
    assert list_a[0]["project_id"] == proj_a.project_id

    # 2. User B lists projects -> sees ONLY proj_b
    list_b = client.get("/api/graph/project/list", headers=_auth_header(token_b)).get_json()["data"]
    assert len(list_b) == 1
    assert list_b[0]["project_id"] == proj_b.project_id

    # 3. User A cannot access User B's project (403 Forbidden)
    forbidden_get = client.get(f"/api/graph/project/{proj_b.project_id}", headers=_auth_header(token_a))
    assert forbidden_get.status_code == 403

    # 4. User A cannot delete User B's project (403 Forbidden)
    forbidden_del = client.delete(f"/api/graph/project/{proj_b.project_id}", headers=_auth_header(token_a))
    assert forbidden_del.status_code == 403

    # 5. Create simulation states for Project A and Project B
    sim_mgr = SimulationManager()
    sim_a = SimulationState(
        simulation_id="sim_a_123",
        project_id=proj_a.project_id,
        graph_id="graph_a",
        status=SimulationStatus.COMPLETED
    )
    sim_mgr._save_simulation_state(sim_a)

    sim_b = SimulationState(
        simulation_id="sim_b_456",
        project_id=proj_b.project_id,
        graph_id="graph_b",
        status=SimulationStatus.COMPLETED
    )
    sim_mgr._save_simulation_state(sim_b)

    # User A lists simulations -> sees ONLY sim_a
    sims_user_a = sim_mgr.list_simulations(user_id=user_a_id)
    assert len(sims_user_a) == 1
    assert sims_user_a[0].simulation_id == "sim_a_123"

    # User B lists simulations -> sees ONLY sim_b
    sims_user_b = sim_mgr.list_simulations(user_id=user_b_id)
    assert len(sims_user_b) == 1
    assert sims_user_b[0].simulation_id == "sim_b_456"

    # User A cannot GET User B's simulation
    sim_b_access = client.get("/api/simulation/sim_b_456", headers=_auth_header(token_a))
    assert sim_b_access.status_code == 403


def test_byok_profile_update_and_simulation_injection(app_instance, monkeypatch):
    app, tmp_path = app_instance
    client = app.test_client()

    with patch("app.services.email_service.send_verification_email", return_value=True):
        res = client.post("/api/auth/register", json={
            "email": "byok@customer.com",
            "password": "Password123!",
            "full_name": "BYOK Tester"
        })
        token = res.get_json()["access_token"]
        user_id = res.get_json()["user"]["id"]

    # Save BYOK credentials in profile
    custom_key = "sk-custom-openai-key-xyz123"
    custom_base = "https://custom.llm.provider.com/v1"
    custom_model = "gpt-4o-custom"

    patch_res = client.patch(
        "/api/auth/profile",
        headers=_auth_header(token),
        json={
            "custom_llm_api_key": custom_key,
            "custom_llm_base_url": custom_base,
            "custom_llm_model_name": custom_model
        }
    )
    assert patch_res.status_code == 200
    user_data = patch_res.get_json()["user"]
    assert user_data["has_custom_api_key"] is True
    assert user_data["custom_llm_model_name"] == custom_model

    # Verify LLMClient initialization with BYOK
    with app.app_context():
        user = db.session.get(User, user_id)
        assert user.custom_llm_api_key == custom_key
        client_instance = get_user_llm_client(user)
        assert client_instance.api_key == custom_key
        assert client_instance.base_url == custom_base
        assert client_instance.model == custom_model

    # Verify SimulationRunner passes custom BYOK env vars to subprocess
    sim_dir = tmp_path / "simulations" / "sim_byok_test"
    sim_dir.mkdir(parents=True, exist_ok=True)
    config_file = sim_dir / "simulation_config.json"
    config_file.write_text(json.dumps({
        "time_config": {"total_simulation_hours": 10, "minutes_per_round": 30}
    }), encoding="utf-8")
    monkeypatch.setattr(SimulationRunner, "RUN_STATE_DIR", str(tmp_path / "simulations"))

    captured_env = {}

    def mock_popen(*args, **kwargs):
        nonlocal captured_env
        captured_env = kwargs.get("env", {})
        proc = MagicMock()
        proc.pid = 99999
        proc.poll.return_value = None
        return proc

    try:
        with patch("subprocess.Popen", side_effect=mock_popen):
            with patch.object(SimulationRunner, "_monitor_simulation", return_value=None):
                SimulationRunner.start_simulation(
                    simulation_id="sim_byok_test",
                    platform="twitter",
                    custom_llm_api_key=custom_key,
                    custom_llm_base_url=custom_base,
                    custom_llm_model_name=custom_model
                )

        assert captured_env.get("LLM_API_KEY") == custom_key
        assert captured_env.get("LLM_BASE_URL") == custom_base
        assert captured_env.get("LLM_MODEL_NAME") == custom_model
    finally:
        SimulationRunner._processes.pop("sim_byok_test", None)
        SimulationRunner._monitor_threads.pop("sim_byok_test", None)
        SimulationRunner._stdout_files.pop("sim_byok_test", None)
        SimulationRunner._stderr_files.pop("sim_byok_test", None)


def test_unauthenticated_request_cannot_access_private_tenant_data(app_instance, monkeypatch):
    """
    Assert that anonymous / unauthenticated requests cannot inspect, delete, or
    execute actions on registered users' private projects, simulations, or reports,
    and history listing never leaks registered users' simulations.
    """
    app, tmp_path = app_instance
    client = app.test_client()

    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))
    monkeypatch.setattr(SimulationManager, "SIMULATION_DATA_DIR", str(tmp_path / "simulations"))
    monkeypatch.setattr(ReportManager, "REPORTS_DIR", str(tmp_path / "reports"))

    # Register and verify a tenant user
    with patch("app.services.email_service.send_verification_email", return_value=True):
        res = client.post("/api/auth/register", json={
            "email": "owner@company.com",
            "password": "StrongPassword123!",
            "full_name": "Project Owner"
        })
        owner_token = res.get_json()["access_token"]
        owner_id = res.get_json()["user"]["id"]

    with app.app_context():
        u = db.session.get(User, owner_id)
        u.is_verified = True
        db.session.commit()

    # Create owner project and simulation
    owner_proj = ProjectManager.create_project(name="Confidential Project", user_id=owner_id)
    sim_mgr = SimulationManager()
    owner_sim = SimulationState(
        simulation_id="sim_owner_secret",
        project_id=owner_proj.project_id,
        graph_id="graph_owner_secret",
        status=SimulationStatus.COMPLETED
    )
    sim_mgr._save_simulation_state(owner_sim)

    # Create a report for owner simulation
    owner_rep = Report(
        report_id="rep_owner_secret",
        simulation_id=owner_sim.simulation_id,
        graph_id="graph_owner_secret",
        simulation_requirement="Confidential Requirement",
        status=ReportStatus.COMPLETED,
        markdown_content="# Secret Analysis Report"
    )
    ReportManager.save_report(owner_rep)

    # 1. Unauthenticated GET /project/<id> -> 403 Forbidden
    anon_get_proj = client.get(f"/api/graph/project/{owner_proj.project_id}")
    assert anon_get_proj.status_code == 403

    # 2. Unauthenticated DELETE /project/<id> -> 403 Forbidden
    anon_del_proj = client.delete(f"/api/graph/project/{owner_proj.project_id}")
    assert anon_del_proj.status_code == 403

    # 3. Unauthenticated RESET /project/<id>/reset -> 403 Forbidden
    anon_reset_proj = client.post(f"/api/graph/project/{owner_proj.project_id}/reset")
    assert anon_reset_proj.status_code == 403

    # 4. Unauthenticated project listing -> empty (0 private projects leaked)
    anon_list_proj = client.get("/api/graph/project/list").get_json()["data"]
    assert len(anon_list_proj) == 0

    # 5. Unauthenticated GET /simulation/<id> -> 403 Forbidden
    anon_get_sim = client.get(f"/api/simulation/{owner_sim.simulation_id}")
    assert anon_get_sim.status_code == 403

    # 6. Unauthenticated POST /simulation/start -> 403 Forbidden
    anon_start_sim = client.post("/api/simulation/start", json={
        "simulation_id": owner_sim.simulation_id,
        "platform": "parallel"
    })
    assert anon_start_sim.status_code == 403

    # 7. Unauthenticated POST /simulation/stop -> 403 Forbidden
    anon_stop_sim = client.post("/api/simulation/stop", json={
        "simulation_id": owner_sim.simulation_id
    })
    assert anon_stop_sim.status_code == 403

    # 8. Unauthenticated history -> empty (0 simulations leaked)
    anon_history = client.get("/api/simulation/history").get_json()["data"]
    assert len(anon_history) == 0

    # 9. Unauthenticated simulation listing -> empty
    anon_list_sim = client.get("/api/simulation/list").get_json()["data"]
    assert len(anon_list_sim) == 0

    # 10. Unauthenticated GET /report/<id> -> 403 Forbidden
    anon_get_rep = client.get(f"/api/report/{owner_rep.report_id}")
    assert anon_get_rep.status_code == 403

    # 11. Unauthenticated GET /report/by-simulation/<id> -> 403 Forbidden
    anon_get_rep_by_sim = client.get(f"/api/report/by-simulation/{owner_sim.simulation_id}")
    assert anon_get_rep_by_sim.status_code == 403

    # 12. Unauthenticated DELETE /report/<id> -> 403 Forbidden
    anon_del_rep = client.delete(f"/api/report/{owner_rep.report_id}")
    assert anon_del_rep.status_code == 403

    # 13. Unauthenticated report listing -> empty
    anon_list_rep = client.get("/api/report/list").get_json()["data"]
    assert len(anon_list_rep) == 0

    # 14. Owner with valid token CAN access their own project, simulation, report
    owner_get_proj = client.get(f"/api/graph/project/{owner_proj.project_id}", headers=_auth_header(owner_token))
    assert owner_get_proj.status_code == 200

    owner_get_sim = client.get(f"/api/simulation/{owner_sim.simulation_id}", headers=_auth_header(owner_token))
    assert owner_get_sim.status_code == 200

    owner_get_rep = client.get(f"/api/report/{owner_rep.report_id}", headers=_auth_header(owner_token))
    assert owner_get_rep.status_code == 200

    owner_history = client.get("/api/simulation/history", headers=_auth_header(owner_token)).get_json()["data"]
    assert len(owner_history) == 1
    assert owner_history[0]["simulation_id"] == owner_sim.simulation_id


def test_byok_removal_reverts_to_platform_default(app_instance):
    """Verify that removing a custom BYOK key reverts to platform default configuration."""
    app, _ = app_instance
    client = app.test_client()

    with patch("app.services.email_service.send_verification_email", return_value=True):
        res = client.post("/api/auth/register", json={
            "email": "keyrevert@customer.com",
            "password": "Password123!",
            "full_name": "Revert Tester"
        })
        token = res.get_json()["access_token"]
        user_id = res.get_json()["user"]["id"]

    # 1. Set key
    client.patch("/api/auth/profile", headers=_auth_header(token), json={
        "custom_llm_api_key": "sk-temp-key-abc"
    })
    with app.app_context():
        u = db.session.get(User, user_id)
        assert u.custom_llm_api_key == "sk-temp-key-abc"

    # 2. Clear key (send empty string)
    clear_res = client.patch("/api/auth/profile", headers=_auth_header(token), json={
        "custom_llm_api_key": ""
    })
    assert clear_res.status_code == 200
    assert clear_res.get_json()["user"]["has_custom_api_key"] is False

    with app.app_context():
        u = db.session.get(User, user_id)
        assert u.custom_llm_api_key is None
        llm = get_user_llm_client(u)
        # Should fall back to Config defaults
        from app.config import Config
        assert llm.api_key == Config.LLM_API_KEY


def test_byok_key_is_encrypted_at_rest_and_logout_revokes_token(app_instance):
    """Verify that BYOK keys are encrypted at rest and logout invalidates refresh tokens."""
    app, _ = app_instance
    client = app.test_client()

    with patch("app.services.email_service.send_verification_email", return_value=True):
        res = client.post("/api/auth/register", json={
            "email": "crypto_test@example.com",
            "password": "Password123!",
            "full_name": "Crypto Tester"
        })
        data = res.get_json()
        token = data["access_token"]
        refresh_token = data["refresh_token"]
        user_id = data["user"]["id"]

    # 1. Save custom API key
    client.patch("/api/auth/profile", headers=_auth_header(token), json={
        "custom_llm_api_key": "sk-super-secret-production-key"
    })

    with app.app_context():
        u = db.session.get(User, user_id)
        # In-memory property decrypts:
        assert u.custom_llm_api_key == "sk-super-secret-production-key"
        # In SQLite column, raw data is Fernet-encrypted ciphertext starting with gAAAAA:
        assert u._custom_llm_api_key.startswith("gAAAAA")
        assert "sk-super-secret" not in u._custom_llm_api_key

    # 2. Token refresh works before logout
    ref_res = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    assert ref_res.status_code == 200
    new_token = ref_res.get_json()["access_token"]
    new_refresh = ref_res.get_json()["refresh_token"]

    # 3. Log out via API
    logout_res = client.post("/api/auth/logout", headers=_auth_header(new_token))
    assert logout_res.status_code == 200

    # 4. Old refresh tokens are now revoked!
    revoked_res = client.post("/api/auth/refresh", json={"refresh_token": new_refresh})
    assert revoked_res.status_code == 401
    assert revoked_res.get_json()["code"] == "TOKEN_REVOKED"


def test_graph_task_and_data_isolation(app_instance):
    """Verify task and graph data isolation between tenants."""
    app, _ = app_instance
    client = app.test_client()

    with patch("app.services.email_service.send_verification_email", return_value=True):
        res_a = client.post("/api/auth/register", json={
            "email": "task_a@tenant.com",
            "password": "Password123!",
            "full_name": "Tenant A"
        })
        token_a = res_a.get_json()["access_token"]
        user_a_id = res_a.get_json()["user"]["id"]

        res_b = client.post("/api/auth/register", json={
            "email": "task_b@tenant.com",
            "password": "Password123!",
            "full_name": "Tenant B"
        })
        token_b = res_b.get_json()["access_token"]
        user_b_id = res_b.get_json()["user"]["id"]

    tm = TaskManager()
    task_a_id = tm.create_task("build_graph", metadata={"user_id": user_a_id, "project_id": "proj_a"})
    task_b_id = tm.create_task("build_graph", metadata={"user_id": user_b_id, "project_id": "proj_b"})

    # TaskManager.list_tasks filtering
    tasks_a = tm.list_tasks(user_id=user_a_id)
    assert any(t["task_id"] == task_a_id for t in tasks_a)
    assert not any(t["task_id"] == task_b_id for t in tasks_a)

    tasks_b = tm.list_tasks(user_id=user_b_id)
    assert any(t["task_id"] == task_b_id for t in tasks_b)
    assert not any(t["task_id"] == task_a_id for t in tasks_b)

    # GET /api/graph/tasks requires auth
    anon_tasks = client.get("/api/graph/tasks")
    assert anon_tasks.status_code == 401

    # GET /api/graph/tasks filters by current user
    res_tasks_a = client.get("/api/graph/tasks", headers=_auth_header(token_a))
    assert res_tasks_a.status_code == 200
    ids_a = [t["task_id"] for t in res_tasks_a.get_json()["data"]]
    assert task_a_id in ids_a
    assert task_b_id not in ids_a

    # GET /api/graph/task/<id> requires auth
    anon_task = client.get(f"/api/graph/task/{task_a_id}")
    assert anon_task.status_code == 401

    # Cross-tenant access to task is 403 Forbidden
    cross_task = client.get(f"/api/graph/task/{task_a_id}", headers=_auth_header(token_b))
    assert cross_task.status_code == 403

    # Owner access to task is 200 OK
    own_task = client.get(f"/api/graph/task/{task_a_id}", headers=_auth_header(token_a))
    assert own_task.status_code == 200
    assert own_task.get_json()["data"]["task_id"] == task_a_id

    # Create project owned by User A with a graph_id
    proj_a = ProjectManager.create_project(name="Project Graph A", user_id=user_a_id)
    proj_a.graph_id = "graph_sec_test_a"
    ProjectManager.save_project(proj_a)

    # User B accessing User A's graph data gets 403 Forbidden
    cross_data = client.get("/api/graph/data/graph_sec_test_a", headers=_auth_header(token_b))
    assert cross_data.status_code == 403

    # User B deleting User A's graph gets 403 Forbidden
    cross_del = client.delete("/api/graph/delete/graph_sec_test_a", headers=_auth_header(token_b))
    assert cross_del.status_code == 403

    # Unauthenticated requests get 401
    assert client.get("/api/graph/data/graph_sec_test_a").status_code == 401
    assert client.delete("/api/graph/delete/graph_sec_test_a").status_code == 401



