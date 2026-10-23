"""
Comprehensive verification test suite for ObMind:
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
from app.services.simulation_manager import SimulationManager, SimulationState, SimulationStatus
from app.services.report_agent import ReportManager, Report, ReportStatus
from app.services.simulation_runner import SimulationRunner
from app.utils.auth_middleware import get_user_llm_client, check_simulation_permission


@pytest.fixture
def app_instance(tmp_path):
    """Create test application with isolated test database and directories."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path}/test_auth.db",
        "JWT_SECRET_KEY": "test-jwt-secret-key-123456",
    })

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
