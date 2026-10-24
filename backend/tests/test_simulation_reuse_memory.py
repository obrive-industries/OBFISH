import json
from unittest.mock import MagicMock

import pytest
from app import create_app
from app.api import simulation as simulation_api
from app.config import Config
from app.models.project import Project, ProjectManager, ProjectStatus
from app.services.simulation_manager import SimulationManager, SimulationState, SimulationStatus
from app.utils import auth_middleware


def test_project_model_simulation_id_persistence(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path))
    ProjectManager.PROJECTS_DIR = str(tmp_path / "projects")

    project = ProjectManager.create_project(name="Test Project")
    assert project.simulation_id is None
    d = project.to_dict()
    assert "simulation_id" in d
    assert d["simulation_id"] is None

    project.simulation_id = "sim_test_123"
    ProjectManager.save_project(project)

    loaded = ProjectManager.get_project(project.project_id)
    assert loaded is not None
    assert loaded.simulation_id == "sim_test_123"
    assert loaded.to_dict()["simulation_id"] == "sim_test_123"


def test_create_simulation_reuses_existing_simulation(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path / "uploads"))
    monkeypatch.setattr(Config, "OASIS_SIMULATION_DATA_DIR", str(tmp_path / "simulations"))
    ProjectManager.PROJECTS_DIR = str(tmp_path / "uploads" / "projects")

    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()
    monkeypatch.setattr(auth_middleware, "get_current_user", lambda: MagicMock(id=None))
    monkeypatch.setattr(simulation_api, "active_plan_denial", lambda *args, **kwargs: None)

    project = ProjectManager.create_project(name="Reuse Test")
    project.graph_id = "graph_test_123"
    project.status = ProjectStatus.GRAPH_COMPLETED
    ProjectManager.save_project(project)

    # First call: creates new simulation
    res1 = client.post(
        "/api/simulation/create",
        json={"project_id": project.project_id, "graph_id": "graph_test_123"},
    )
    assert res1.status_code == 200
    data1 = res1.json["data"]
    sim_id_1 = data1["simulation_id"]
    assert "reused" not in res1.json or res1.json.get("reused") is not True

    # Check project has simulation_id saved
    updated_project = ProjectManager.get_project(project.project_id)
    assert updated_project.simulation_id == sim_id_1

    # Second call (navigating back to Step 1 and clicking Enter Env Setup again):
    # Must reuse the same simulation_id and NOT burn tokens
    res2 = client.post(
        "/api/simulation/create",
        json={"project_id": project.project_id, "graph_id": "graph_test_123"},
    )
    assert res2.status_code == 200
    assert res2.json.get("reused") is True
    assert res2.json["data"]["simulation_id"] == sim_id_1

    # Third call with force_new: True creates a new simulation
    res3 = client.post(
        "/api/simulation/create",
        json={
            "project_id": project.project_id,
            "graph_id": "graph_test_123",
            "force_new": True,
        },
    )
    assert res3.status_code == 200
    assert res3.json.get("reused") is not True
    sim_id_3 = res3.json["data"]["simulation_id"]
    assert sim_id_3 != sim_id_1

    final_project = ProjectManager.get_project(project.project_id)
    assert final_project.simulation_id == sim_id_3
