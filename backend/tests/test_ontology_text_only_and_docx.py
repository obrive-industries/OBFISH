import io
import os
import tempfile
from unittest.mock import MagicMock
import docx
import pytest

from app import create_app
from app.api import graph as graph_api
from app.models.project import ProjectManager, ProjectStatus


def test_ontology_generation_text_only_hypothesis(tmp_path, monkeypatch):
    """Test generating ontology with text-only hypothesis and NO uploaded files."""
    captured = {}

    class MockGenerator:
        def generate(self, document_texts, simulation_requirement, additional_context=None):
            captured['document_texts'] = document_texts
            captured['simulation_requirement'] = simulation_requirement
            return {
                "entity_types": [{"name": "Market", "description": "Target market"}],
                "edge_types": [{"name": "AFFECTS", "description": "Affects relationship"}],
                "analysis_summary": "Summary of text-only hypothesis."
            }

    mock_user = MagicMock(id="test-user-id", is_verified=True, role="admin")
    monkeypatch.setattr("app.utils.auth_middleware.get_current_user", lambda: mock_user)
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path))
    monkeypatch.setattr(graph_api, "OntologyGenerator", MockGenerator)

    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    response = client.post(
        "/api/graph/ontology/generate",
        data={
            "simulation_requirement": "Hypothesis: Renewable energy adoption will accelerate 25% by 2030.",
            "project_name": "Renewable Energy Test"
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    data = response.json
    assert data["success"] is True
    project_id = data["data"]["project_id"]
    
    project = ProjectManager.get_project(project_id)
    assert project is not None
    assert project.status == ProjectStatus.ONTOLOGY_GENERATED
    assert len(project.files) == 1
    assert project.files[0]["filename"] == "hypothesis.txt"
    assert "Renewable energy adoption" in captured['document_texts'][0]
    assert captured['simulation_requirement'] == "Hypothesis: Renewable energy adoption will accelerate 25% by 2030."


def test_ontology_generation_with_docx_upload(tmp_path, monkeypatch):
    """Test generating ontology with a DOCX file upload."""
    captured = {}

    class MockGenerator:
        def generate(self, document_texts, simulation_requirement, additional_context=None):
            captured['document_texts'] = document_texts
            return {
                "entity_types": [{"name": "Stakeholder", "description": "Stakeholder entity"}],
                "edge_types": [],
                "analysis_summary": "DOCX analysis summary."
            }

    mock_user = MagicMock(id="test-user-id", is_verified=True, role="admin")
    monkeypatch.setattr("app.utils.auth_middleware.get_current_user", lambda: mock_user)
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path))
    monkeypatch.setattr(graph_api, "OntologyGenerator", MockGenerator)

    # Generate a real in-memory docx
    doc = docx.Document()
    doc.add_paragraph("Enterprise Strategy Scenario 2026")
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)

    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    response = client.post(
        "/api/graph/ontology/generate",
        data={
            "simulation_requirement": "Evaluate enterprise strategy.",
            "project_name": "DOCX Ingestion Test",
            "files": (doc_io, "strategy.docx")
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    data = response.json
    assert data["success"] is True
    project_id = data["data"]["project_id"]

    project = ProjectManager.get_project(project_id)
    assert project is not None
    assert project.status == ProjectStatus.ONTOLOGY_GENERATED
    assert any("strategy.docx" in f["filename"] for f in project.files)
    assert any("Enterprise Strategy Scenario 2026" in t for t in captured['document_texts'])
