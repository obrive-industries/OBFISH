"""
Tests for production readiness enhancements:
1. HTTP Security Headers
2. Global JSON Error Handlers on /api/*
3. CORS configuration
4. LLM failover condition coverage (timeouts, connection drops, quota)
5. Atomic persistence of Project and Report metadata
"""

import json
import os
import pytest
from flask import Flask

from app import create_app
from app.config import Config
from app.utils.llm_client import is_retryable_llm_error
from app.models.project import Project, ProjectManager, ProjectStatus
from app.services.report_agent import Report, ReportManager, ReportOutline


@pytest.fixture
def app_client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_http_security_headers_present(app_client):
    """Verify production security headers are set on all responses."""
    resp = app_client.get("/api/health")
    assert resp.status_code == 200
    assert resp.headers.get("X-Content-Type-Options") == "nosniff"
    assert resp.headers.get("X-Frame-Options") == "SAMEORIGIN"
    assert resp.headers.get("X-XSS-Protection") == "1; mode=block"
    assert resp.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"


def test_api_404_returns_json(app_client):
    """Verify non-existent API routes return structured JSON rather than HTML."""
    resp = app_client.get("/api/non-existent-endpoint-12345")
    assert resp.status_code == 404
    assert resp.is_json
    data = resp.get_json()
    assert data["success"] is False
    assert data["code"] == "NOT_FOUND"


def test_api_405_returns_json(app_client):
    """Verify method not allowed on API routes returns structured JSON."""
    resp = app_client.delete("/api/health")
    assert resp.status_code == 405
    assert resp.is_json
    data = resp.get_json()
    assert data["success"] is False
    assert data["code"] == "METHOD_NOT_ALLOWED"


def test_llm_is_retryable_error_coverage():
    """Verify timeout, connection drops, quota exhaustion, and rate limits trigger failover."""
    class MockStatusError(Exception):
        def __init__(self, status):
            self.status_code = status

    class MockConnectionError(Exception):
        pass

    class MockTimeoutError(Exception):
        pass

    # HTTP codes that must failover
    assert is_retryable_llm_error(MockStatusError(429)) is True
    assert is_retryable_llm_error(MockStatusError(403)) is True  # Quota
    assert is_retryable_llm_error(MockStatusError(503)) is True
    assert is_retryable_llm_error(MockStatusError(500)) is True

    # Named connection exceptions
    assert is_retryable_llm_error(MockConnectionError("APIConnectionError: connection reset by peer")) is True
    assert is_retryable_llm_error(MockTimeoutError("Request timed out after 30.0 seconds")) is True

    # Error body keyword indicators
    assert is_retryable_llm_error(Exception("You have exceeded your monthly quota")) is True
    assert is_retryable_llm_error(Exception("Rate limit reached for model")) is True
    assert is_retryable_llm_error(Exception("Server temporarily overloaded")) is True

    # Non-retryable error
    assert is_retryable_llm_error(ValueError("Invalid argument 'temperature'")) is False


def test_atomic_project_save(tmp_path, monkeypatch):
    """Verify ProjectManager.save_project creates and replaces files cleanly."""
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path))
    project = ProjectManager.create_project(name="Test Atomic Project")
    meta_path = ProjectManager._get_project_meta_path(project.project_id)

    assert os.path.exists(meta_path)
    # The temporary file should be replaced and no longer exist
    assert not os.path.exists(meta_path + ".tmp")

    loaded = ProjectManager.get_project(project.project_id)
    assert loaded is not None
    assert loaded.name == "Test Atomic Project"


def test_atomic_report_save(tmp_path, monkeypatch):
    """Verify ReportManager.save_report and save_outline write atomically."""
    monkeypatch.setattr(ReportManager, "REPORTS_DIR", str(tmp_path))
    from app.services.report_agent import ReportSection
    outline = ReportOutline(
        title="Test Report",
        summary="Test Executive Summary",
        sections=[ReportSection(title="Intro", content="Overview")]
    )
    from app.services.report_agent import ReportStatus
    report = Report(
        report_id="rep_test_atomic",
        simulation_id="sim_123",
        graph_id="g_123",
        simulation_requirement="Testing requirement",
        status=ReportStatus.COMPLETED,
        outline=outline,
        markdown_content="# Test Report Content"
    )
    ReportManager.save_report(report)

    report_path = ReportManager._get_report_path("rep_test_atomic")
    md_path = ReportManager._get_report_markdown_path("rep_test_atomic")

    assert os.path.exists(report_path)
    assert not os.path.exists(report_path + ".tmp")
    assert os.path.exists(md_path)
    assert not os.path.exists(md_path + ".tmp")

    loaded = ReportManager.get_report("rep_test_atomic")
    assert loaded is not None
    assert loaded.report_id == "rep_test_atomic"
    assert loaded.simulation_requirement == "Testing requirement"
