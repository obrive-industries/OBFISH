import os
import shutil
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from app.config import Config
from app.services.report_agent import (
    Report,
    ReportAgent,
    ReportManager,
    ReportOutline,
    ReportSection,
    ReportStatus,
)


@pytest.fixture
def temp_reports_dir(monkeypatch):
    temp_dir = tempfile.mkdtemp()
    reports_dir = os.path.join(temp_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    monkeypatch.setattr(ReportManager, "REPORTS_DIR", reports_dir)
    yield reports_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_corrupted_placeholder_section_is_not_reused(temp_reports_dir):
    report_id = "test_rep_123"
    ReportManager._ensure_report_folder(report_id)
    sec_path = ReportManager._get_section_path(report_id, 1)

    dummy_content = (
        "## Strategic Overview\n\n"
        "**Strategic Overview Analysis Summary**\n\n"
        "Preliminary synthesis for this section indicates key behavioral patterns aligned with the simulated conditions. "
        "Multi-agent trajectories reflect emergent dynamics and sentiment shifts across demographic cohorts.\n\n"
        "> Note: Detailed retrieval encountered an operational exception (rate limit reached)."
    )
    with open(sec_path, "w", encoding="utf-8") as f:
        f.write(dummy_content)

    mock_llm = MagicMock()
    mock_llm.chat.return_value = "Final Answer: Genuine synthesized analysis grounded in agent actions."

    agent = ReportAgent(
        graph_id="g_123",
        simulation_id="sim_123",
        simulation_requirement="Analyze market sentiment",
        llm_client=mock_llm,
        zep_tools=MagicMock()
    )

    outline = ReportOutline(
        title="Test Report",
        summary="A test report summary",
        sections=[ReportSection(title="Strategic Overview")]
    )
    ReportManager.save_outline(report_id, outline)

    report = agent.generate_report(report_id=report_id)

    assert report.status == ReportStatus.COMPLETED
    assert "Preliminary synthesis for this section" not in report.markdown_content
    assert "Genuine synthesized analysis" in report.markdown_content


def test_react_failure_uses_fallback_synthesis(temp_reports_dir):
    report_id = "test_rep_fallback"
    ReportManager._ensure_report_folder(report_id)

    mock_llm = MagicMock()
    # Direct fallback chat returns valid analysis
    mock_llm.chat.return_value = "### Direct Synthesis\n\nFallback analysis showing clear user shift toward alternative solutions."

    agent = ReportAgent(
        graph_id="g_456",
        simulation_id="sim_456",
        simulation_requirement="Test requirement",
        llm_client=mock_llm,
        zep_tools=MagicMock()
    )

    outline = ReportOutline(
        title="Test Report",
        summary="Summary",
        sections=[ReportSection(title="Market Impact")]
    )
    ReportManager.save_outline(report_id, outline)

    with patch.object(agent, "_generate_section_react", side_effect=RuntimeError("ReACT tool timeout")):
        report = agent.generate_report(report_id=report_id)

    assert report.status == ReportStatus.COMPLETED
    assert "Fallback analysis showing clear user shift" in report.markdown_content
    assert "Preliminary synthesis" not in report.markdown_content


def test_react_and_fallback_failure_marks_report_failed(temp_reports_dir):
    report_id = "test_rep_failed"
    ReportManager._ensure_report_folder(report_id)

    mock_llm = MagicMock()
    mock_llm.chat.side_effect = RuntimeError("429 Rate limit reached on tokens per day (TPD)")

    agent = ReportAgent(
        graph_id="g_789",
        simulation_id="sim_789",
        simulation_requirement="Test requirement",
        llm_client=mock_llm,
        zep_tools=MagicMock()
    )

    outline = ReportOutline(
        title="Test Report",
        summary="Summary",
        sections=[ReportSection(title="Market Impact")]
    )
    ReportManager.save_outline(report_id, outline)

    with patch.object(agent, "_generate_section_react", side_effect=RuntimeError("429 Rate limit reached")):
        report = agent.generate_report(report_id=report_id)

    assert report.status == ReportStatus.FAILED
    assert "Rate limit" in report.error
    assert "Preliminary synthesis" not in (report.markdown_content or "")
