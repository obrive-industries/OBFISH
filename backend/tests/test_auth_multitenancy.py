"""
Auth, plan-gate and multi-tenancy coverage for Brain.

1. Registration / email verification barrier
2. Free accounts cannot start paid work
3. Tenant isolation for projects, simulations, reports and graph tasks
4. Session revocation and removed BYOK endpoints
"""

import pytest
from unittest.mock import MagicMock, patch

from app import create_app
from app.config import Config
from app.models.user import db, User
from app.models.project import ProjectManager
from app.models.task import TaskManager
from app.services.simulation_manager import (
    SimulationManager,
    SimulationState,
    SimulationStatus,
)
from app.services.report_agent import ReportManager, Report, ReportStatus


@pytest.fixture
def app_instance(tmp_path):
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_path}/test_auth.db"
        JWT_SECRET_KEY = "test-jwt-secret-key-123456"

    app = create_app(TestConfig)

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


def test_user_registration_and_plan_barrier(app_instance):
    app, _ = app_instance
    client = app.test_client()

    with patch("app.services.email_service.send_verification_email", return_value=True):
        response = client.post(
            "/api/auth/register",
            json={
                "email": "customer@example.com",
                "password": "SecurePassword123!",
                "full_name": "Customer One",
            },
        )
    assert response.status_code == 201
    data = response.get_json()
    token = data["access_token"]
    assert data["user"]["is_verified"] is False
    assert data["user"]["is_admin"] is False

    unverified = client.post(
        "/api/simulation/start",
        headers=_auth_header(token),
        json={"simulation_id": "sim_test", "platform": "parallel"},
    )
    assert unverified.status_code == 403
    assert unverified.get_json()["code"] == "EMAIL_NOT_VERIFIED"

    with app.app_context():
        user = User.query.filter_by(email="customer@example.com").first()
        verify_token = user.verification_token

    verified = client.post("/api/auth/verify-email", json={"token": verify_token})
    assert verified.status_code == 200
    verified_token = verified.get_json()["access_token"]

    # A verified free account still has no live-run capacity.
    free_check = client.get("/api/billing/me", headers=_auth_header(verified_token))
    assert free_check.status_code == 200
    entitlement = free_check.get_json()["entitlement"]
    assert entitlement["plan"] == "free"
    assert entitlement["can_start"] is False

    gated = client.post(
        "/api/graph/ontology/generate",
        headers=_auth_header(verified_token),
        data={"simulation_requirement": "Test scenario"},
        content_type="multipart/form-data",
    )
    assert gated.status_code == 402
    assert gated.get_json()["code"] == "PLAN_REQUIRED"


def test_profile_no_longer_accepts_byok_keys(app_instance):
    app, _ = app_instance
    client = app.test_client()

    with patch("app.services.email_service.send_verification_email", return_value=True):
        response = client.post(
            "/api/auth/register",
            json={
                "email": "nokeys@example.com",
                "password": "Password123!",
                "full_name": "No Keys",
            },
        )
    token = response.get_json()["access_token"]

    updated = client.patch(
        "/api/auth/profile",
        headers=_auth_header(token),
        json={
            "full_name": "Renamed User",
            "custom_llm_api_key": "sk-should-be-ignored",
            "custom_llm_base_url": "https://example.com/v1",
        },
    )
    assert updated.status_code == 200
    payload = updated.get_json()["user"]
    assert payload["full_name"] == "Renamed User"
    assert "custom_llm_api_key" not in payload
    assert "has_custom_api_key" not in payload

    assert (
        client.post(
            "/api/auth/probe-llm-key",
            headers=_auth_header(token),
            json={"api_key": "sk-test"},
        ).status_code
        == 404
    )


def test_multitenancy_project_and_history_isolation(app_instance, monkeypatch):
    app, tmp_path = app_instance
    client = app.test_client()

    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))
    monkeypatch.setattr(
        SimulationManager, "SIMULATION_DATA_DIR", str(tmp_path / "simulations")
    )
    monkeypatch.setattr(ReportManager, "REPORTS_DIR", str(tmp_path / "reports"))

    with patch("app.services.email_service.send_verification_email", return_value=True):
        res_a = client.post(
            "/api/auth/register",
            json={
                "email": "a@domain.com",
                "password": "Password123!",
                "full_name": "User A",
            },
        )
        token_a = res_a.get_json()["access_token"]
        user_a_id = res_a.get_json()["user"]["id"]

        res_b = client.post(
            "/api/auth/register",
            json={
                "email": "b@domain.com",
                "password": "Password123!",
                "full_name": "User B",
            },
        )
        token_b = res_b.get_json()["access_token"]
        user_b_id = res_b.get_json()["user"]["id"]

    with app.app_context():
        for uid in (user_a_id, user_b_id):
            user = db.session.get(User, uid)
            user.is_verified = True
        db.session.commit()

    proj_a = ProjectManager.create_project(name="Project of A", user_id=user_a_id)
    proj_b = ProjectManager.create_project(name="Project of B", user_id=user_b_id)

    list_a = client.get(
        "/api/graph/project/list", headers=_auth_header(token_a)
    ).get_json()["data"]
    assert [project["project_id"] for project in list_a] == [proj_a.project_id]

    list_b = client.get(
        "/api/graph/project/list", headers=_auth_header(token_b)
    ).get_json()["data"]
    assert [project["project_id"] for project in list_b] == [proj_b.project_id]

    assert (
        client.get(
            f"/api/graph/project/{proj_b.project_id}", headers=_auth_header(token_a)
        ).status_code
        == 403
    )
    assert (
        client.delete(
            f"/api/graph/project/{proj_b.project_id}", headers=_auth_header(token_a)
        ).status_code
        == 403
    )

    sim_mgr = SimulationManager()
    sim_mgr._save_simulation_state(
        SimulationState(
            simulation_id="sim_a_123",
            project_id=proj_a.project_id,
            graph_id="graph_a",
            status=SimulationStatus.COMPLETED,
        )
    )
    sim_mgr._save_simulation_state(
        SimulationState(
            simulation_id="sim_b_456",
            project_id=proj_b.project_id,
            graph_id="graph_b",
            status=SimulationStatus.COMPLETED,
        )
    )

    sims_a = sim_mgr.list_simulations(user_id=user_a_id)
    assert [sim.simulation_id for sim in sims_a] == ["sim_a_123"]
    sims_b = sim_mgr.list_simulations(user_id=user_b_id)
    assert [sim.simulation_id for sim in sims_b] == ["sim_b_456"]

    assert (
        client.get(
            "/api/simulation/sim_b_456", headers=_auth_header(token_a)
        ).status_code
        == 403
    )


def test_unauthenticated_requests_cannot_read_tenant_data(app_instance, monkeypatch):
    app, tmp_path = app_instance
    client = app.test_client()

    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))
    monkeypatch.setattr(
        SimulationManager, "SIMULATION_DATA_DIR", str(tmp_path / "simulations")
    )
    monkeypatch.setattr(ReportManager, "REPORTS_DIR", str(tmp_path / "reports"))

    with patch("app.services.email_service.send_verification_email", return_value=True):
        response = client.post(
            "/api/auth/register",
            json={
                "email": "owner@company.com",
                "password": "StrongPassword123!",
                "full_name": "Project Owner",
            },
        )
        owner_token = response.get_json()["access_token"]
        owner_id = response.get_json()["user"]["id"]

    with app.app_context():
        user = db.session.get(User, owner_id)
        user.is_verified = True
        db.session.commit()

    project = ProjectManager.create_project(name="Confidential", user_id=owner_id)
    sim_mgr = SimulationManager()
    simulation = SimulationState(
        simulation_id="sim_owner_secret",
        project_id=project.project_id,
        graph_id="graph_owner_secret",
        status=SimulationStatus.COMPLETED,
    )
    sim_mgr._save_simulation_state(simulation)

    report = Report(
        report_id="rep_owner_secret",
        simulation_id=simulation.simulation_id,
        graph_id="graph_owner_secret",
        simulation_requirement="Confidential Requirement",
        status=ReportStatus.COMPLETED,
        markdown_content="# Secret Analysis Report",
    )
    ReportManager.save_report(report)

    assert (
        client.get(f"/api/graph/project/{project.project_id}").status_code == 403
    )
    assert (
        client.delete(f"/api/graph/project/{project.project_id}").status_code == 403
    )
    assert client.get("/api/graph/project/list").get_json()["data"] == []
    assert client.get(f"/api/simulation/{simulation.simulation_id}").status_code == 403
    assert (
        client.post(
            "/api/simulation/start",
            json={"simulation_id": simulation.simulation_id},
        ).status_code
        == 401
    )
    assert client.get("/api/simulation/history").get_json()["data"] == []
    assert client.get("/api/simulation/list").get_json()["data"] == []
    assert client.get(f"/api/report/{report.report_id}").status_code == 403
    assert (
        client.get(
            f"/api/report/by-simulation/{simulation.simulation_id}"
        ).status_code
        == 403
    )
    assert client.get("/api/report/list").get_json()["data"] == []

    assert (
        client.get(
            f"/api/graph/project/{project.project_id}",
            headers=_auth_header(owner_token),
        ).status_code
        == 200
    )
    assert (
        client.get(
            f"/api/simulation/{simulation.simulation_id}",
            headers=_auth_header(owner_token),
        ).status_code
        == 200
    )
    assert (
        client.get(
            f"/api/report/{report.report_id}", headers=_auth_header(owner_token)
        ).status_code
        == 200
    )


def test_logout_revokes_refresh_tokens(app_instance):
    app, _ = app_instance
    client = app.test_client()

    with patch("app.services.email_service.send_verification_email", return_value=True):
        response = client.post(
            "/api/auth/register",
            json={
                "email": "session@example.com",
                "password": "Password123!",
                "full_name": "Session Tester",
            },
        )
    data = response.get_json()
    token = data["access_token"]
    refresh_token = data["refresh_token"]

    refreshed = client.post(
        "/api/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert refreshed.status_code == 200
    new_token = refreshed.get_json()["access_token"]
    new_refresh = refreshed.get_json()["refresh_token"]

    assert (
        client.post("/api/auth/logout", headers=_auth_header(new_token)).status_code
        == 200
    )

    revoked = client.post("/api/auth/refresh", json={"refresh_token": new_refresh})
    assert revoked.status_code == 401
    assert revoked.get_json()["code"] == "TOKEN_REVOKED"


def test_graph_task_and_data_isolation(app_instance):
    app, _ = app_instance
    client = app.test_client()

    with patch("app.services.email_service.send_verification_email", return_value=True):
        res_a = client.post(
            "/api/auth/register",
            json={
                "email": "task_a@tenant.com",
                "password": "Password123!",
                "full_name": "Tenant A",
            },
        )
        token_a = res_a.get_json()["access_token"]
        user_a_id = res_a.get_json()["user"]["id"]

        res_b = client.post(
            "/api/auth/register",
            json={
                "email": "task_b@tenant.com",
                "password": "Password123!",
                "full_name": "Tenant B",
            },
        )
        token_b = res_b.get_json()["access_token"]
        user_b_id = res_b.get_json()["user"]["id"]

    task_manager = TaskManager()
    task_a_id = task_manager.create_task(
        "build_graph", metadata={"user_id": user_a_id, "project_id": "proj_a"}
    )
    task_b_id = task_manager.create_task(
        "build_graph", metadata={"user_id": user_b_id, "project_id": "proj_b"}
    )

    tasks_a = task_manager.list_tasks(user_id=user_a_id)
    assert any(task["task_id"] == task_a_id for task in tasks_a)
    assert not any(task["task_id"] == task_b_id for task in tasks_a)

    assert client.get("/api/graph/tasks").status_code == 401
    res_tasks_a = client.get("/api/graph/tasks", headers=_auth_header(token_a))
    assert res_tasks_a.status_code == 200
    ids_a = [task["task_id"] for task in res_tasks_a.get_json()["data"]]
    assert task_a_id in ids_a
    assert task_b_id not in ids_a

    assert client.get(f"/api/graph/task/{task_a_id}").status_code == 401
    assert (
        client.get(
            f"/api/graph/task/{task_a_id}", headers=_auth_header(token_b)
        ).status_code
        == 403
    )
    assert (
        client.get(
            f"/api/graph/task/{task_a_id}", headers=_auth_header(token_a)
        ).status_code
        == 200
    )

    project = ProjectManager.create_project(name="Project Graph A", user_id=user_a_id)
    project.graph_id = "graph_sec_test_a"
    ProjectManager.save_project(project)

    assert (
        client.get(
            "/api/graph/data/graph_sec_test_a", headers=_auth_header(token_b)
        ).status_code
        == 403
    )
    assert (
        client.delete(
            "/api/graph/delete/graph_sec_test_a", headers=_auth_header(token_b)
        ).status_code
        == 403
    )
    assert client.get("/api/graph/data/graph_sec_test_a").status_code == 401
    assert client.delete("/api/graph/delete/graph_sec_test_a").status_code == 401
