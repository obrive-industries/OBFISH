"""Recovery of a run whose monitor thread died with the server.

run_state.json is only a projection written by the monitor thread, so when that
thread is gone the file can still describe the start of a run. These tests drive
the real recovery path, the real stop finalization and the real report gate.
"""

import json
import os
import subprocess
import sys
from types import SimpleNamespace

import pytest
from flask import Flask

from app.api import report as report_api
from app.api import simulation as simulation_api
from app.models.project import ProjectStatus
from app.services import simulation_runner as runner_module
from app.services.simulation_manager import SimulationManager, SimulationState, SimulationStatus
from app.services.simulation_runner import (
    RunnerStatus,
    SimulationRunState,
    SimulationRunner,
)
from app.services.zep_graph_memory_updater import ZepIngestionIncompleteError


@pytest.fixture(autouse=True)
def isolated_runner_state(monkeypatch):
    """Give every test its own sim directory and a clean runner registry."""

    def _reset():
        SimulationRunner._run_states.clear()
        SimulationRunner._processes.clear()
        SimulationRunner._monitor_threads.clear()
        SimulationRunner._action_queues.clear()
        SimulationRunner._stdout_files.clear()
        SimulationRunner._stderr_files.clear()
        SimulationRunner._graph_memory_enabled.clear()
        SimulationRunner._manual_stop_requests.clear()

    _reset()
    yield
    _reset()


@pytest.fixture(autouse=True)
def mock_auth_permissions(monkeypatch):
    allow = lambda *args, **kwargs: None
    monkeypatch.setattr(simulation_api, "active_plan_denial", allow)
    monkeypatch.setattr(report_api, "active_plan_denial", allow)


@pytest.fixture
def sim_dirs(tmp_path, monkeypatch):
    """One simulation directory shared by the runner and the manager."""
    monkeypatch.setattr(SimulationRunner, "RUN_STATE_DIR", str(tmp_path))
    monkeypatch.setattr(SimulationManager, "SIMULATION_DATA_DIR", str(tmp_path))
    return tmp_path


def _dead_pid() -> int:
    """A pid that is guaranteed not to be running any more."""
    child = subprocess.Popen([sys.executable, "-c", "pass"])
    child.wait()
    pid = child.pid
    try:
        os.kill(pid, 0)
    except OSError:
        return pid
    pytest.skip(f"pid {pid} was reused before the test could observe it")


def _write_action_log(sim_dir, platform, rounds, actions_per_round, final_round):
    """Write the log the simulation process itself would have appended."""
    platform_dir = sim_dir / platform
    platform_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        json.dumps({
            "event_type": "simulation_start",
            "platform": platform,
            "total_rounds": rounds,
        })
    ]
    for round_num in range(0, final_round + 1):
        lines.append(json.dumps({"event_type": "round_start", "round": round_num}))
        for action_index in range(actions_per_round):
            lines.append(json.dumps({
                "round": round_num,
                "timestamp": f"2026-10-23T21:13:{round_num:02d}:00",
                "agent_id": action_index,
                "agent_name": f"agent-{action_index}",
                "action_type": "CREATE_POST",
                "action_args": {"content": "hello"},
                "success": True,
            }))
        lines.append(json.dumps({
            "event_type": "round_end",
            "round": round_num,
            "simulated_hours": round_num + 1,
        }))
    lines.append(json.dumps({"event_type": "simulation_end", "total_rounds": rounds}))
    log_path = platform_dir / "actions.jsonl"
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(lines)


def _write_profiles(sim_dir, professions):
    profiles = [
        {
            "user_id": index,
            "username": f"agent_{index}",
            "profession": profession,
            "bio": "bio",
        }
        for index, profession in enumerate(professions)
    ]
    (sim_dir / "reddit_profiles.json").write_text(
        json.dumps(profiles), encoding="utf-8"
    )


def _persist_run_state(simulation_id, *, status, total_rounds, pid=None):
    state = SimulationRunState(
        simulation_id=simulation_id,
        runner_status=status,
        total_rounds=total_rounds,
        total_simulation_hours=72,
        process_pid=pid,
        started_at="2026-10-23T21:12:48.277461",
        updated_at="2026-10-23T21:12:48.277461",
        completed_at=None,
    )
    SimulationRunner._save_run_state(state)
    return state


def _persist_simulation_state(simulation_id, **overrides):
    manager = SimulationManager()
    state = SimulationState(
        simulation_id=simulation_id,
        project_id="proj-1",
        graph_id="graph-1",
        status=SimulationStatus.RUNNING,
        **overrides,
    )
    manager._save_simulation_state(state)
    return state


def test_pid_dead_recovery_rebuilds_progress_from_action_logs(sim_dirs):
    simulation_id = "sim-recover"
    sim_dir = sim_dirs / simulation_id
    sim_dir.mkdir()
    _write_action_log(sim_dir, "twitter", rounds=15, actions_per_round=3, final_round=4)
    _write_action_log(sim_dir, "reddit", rounds=15, actions_per_round=2, final_round=4)
    _write_profiles(sim_dir, ["VehicleOwnerEntity", "CompetitorEntity"])
    (sim_dir / "simulation.log").write_text(
        "[Reddit] 模拟循环完成! 耗时: 30.3秒\n", encoding="utf-8"
    )

    # The snapshot a monitor thread died before ever updating.
    _persist_run_state(
        simulation_id,
        status=RunnerStatus.RUNNING,
        total_rounds=15,
        pid=_dead_pid(),
    )
    _persist_simulation_state(
        simulation_id,
        current_round=0,
        entity_types=[],
    )

    state = SimulationRunner.get_run_state(simulation_id)

    assert state.runner_status == RunnerStatus.COMPLETED
    assert state.completed_at, "a recovered terminal state must be timestamped"
    # 5 rounds x 3/2 actions, read from the producers' own logs.
    assert state.twitter_actions_count == 15
    assert state.reddit_actions_count == 10
    assert state.current_round == 15
    assert state.twitter_simulated_hours == 5
    assert state.reddit_simulated_hours == 5

    # state.json is reconciled with the same run instead of staying at round 0
    # with empty entity types.
    simulation = SimulationManager().get_simulation(simulation_id)
    assert simulation.current_round == 15
    assert simulation.entity_types == ["CompetitorEntity", "VehicleOwnerEntity"]
    assert simulation.status == SimulationStatus.COMPLETED


def test_stale_stopping_state_with_dead_pid_recovers_to_terminal(sim_dirs):
    simulation_id = "sim-stale-stopping"
    sim_dir = sim_dirs / simulation_id
    sim_dir.mkdir()
    # Partial logs and no completion marker: the run was stopped mid-flight.
    _write_action_log(sim_dir, "twitter", rounds=15, actions_per_round=2, final_round=3)
    (sim_dir / "simulation.log").write_text("run interrupted\n", encoding="utf-8")

    _persist_run_state(
        simulation_id,
        status=RunnerStatus.STOPPING,
        total_rounds=15,
        pid=_dead_pid(),
    )
    _persist_simulation_state(simulation_id)

    state = SimulationRunner.get_run_state(simulation_id)

    assert state.runner_status == RunnerStatus.STOPPED
    assert state.completed_at
    assert state.twitter_actions_count == 8
    assert state.current_round == 3
    # The report gate accepts exactly these two statuses.
    assert state.runner_status in {RunnerStatus.COMPLETED, RunnerStatus.STOPPED}


def test_recovery_does_not_fire_while_the_process_is_still_tracked(sim_dirs):
    simulation_id = "sim-live"
    sim_dir = sim_dirs / simulation_id
    sim_dir.mkdir()
    _write_action_log(sim_dir, "twitter", rounds=5, actions_per_round=1, final_round=1)
    _persist_run_state(
        simulation_id,
        status=RunnerStatus.RUNNING,
        total_rounds=5,
        pid=os.getpid(),
    )

    SimulationRunner._processes[simulation_id] = object()

    try:
        state = SimulationRunner.get_run_state(simulation_id)
        assert state.runner_status == RunnerStatus.RUNNING
    finally:
        SimulationRunner._processes.pop(simulation_id, None)


def test_missing_state_json_is_reconstructed_without_fabricated_values(sim_dirs):
    simulation_id = "sim-no-state"
    sim_dir = sim_dirs / simulation_id
    sim_dir.mkdir()
    _write_profiles(sim_dir, ["VehicleOwnerEntity", "CompetitorEntity", "Person"])
    state_file = sim_dir / "state.json"
    state_file.write_text("", encoding="utf-8")

    run_state = SimulationRunState(
        simulation_id=simulation_id,
        runner_status=RunnerStatus.COMPLETED,
        current_round=7,
        total_rounds=15,
    )
    SimulationRunner._save_run_state(run_state)

    simulation = SimulationManager().get_simulation(simulation_id)

    assert simulation is not None
    assert simulation.entities_count == 3
    assert simulation.profiles_count == 3
    assert simulation.entity_types == ["CompetitorEntity", "Person", "VehicleOwnerEntity"]
    assert simulation.config_generated is False
    assert simulation.profiles_generated is True
    # current_round is whatever run_state.json actually holds, never invented.
    persisted_run_state = json.loads((sim_dir / "run_state.json").read_text("utf-8"))
    assert simulation.current_round == persisted_run_state["current_round"]
    assert simulation.status == SimulationStatus.COMPLETED


def test_failed_zep_batch_keeps_the_run_terminal_and_reportable(sim_dirs, monkeypatch):
    simulation_id = "sim-batch-failure"
    _persist_run_state(
        simulation_id, status=RunnerStatus.RUNNING, total_rounds=5, pid=_dead_pid()
    )
    _persist_simulation_state(simulation_id)

    # A registered updater keeps recovery from terminalizing the run, so the
    # request reaches the synchronous finalization that is under test.
    registry = {simulation_id: object()}
    monkeypatch.setattr(
        runner_module.ZepGraphMemoryManager,
        "get_updater",
        classmethod(lambda _cls, _simulation_id: registry.get(_simulation_id)),
    )
    monkeypatch.setattr(
        runner_module.ZepGraphMemoryManager,
        "stop_updater",
        classmethod(
            lambda _cls, _simulation_id: (_ for _ in ()).throw(
                ZepIngestionIncompleteError(1)
            )
        ),
    )
    monkeypatch.setattr(
        runner_module.ZepGraphMemoryManager,
        "discard_inactive_updater",
        classmethod(
            lambda _cls, _simulation_id: registry.pop(_simulation_id, None)
            is not None
        ),
    )
    SimulationRunner._graph_memory_enabled[simulation_id] = True

    try:
        result = SimulationRunner.stop_simulation(simulation_id)
    finally:
        SimulationRunner._graph_memory_enabled.pop(simulation_id, None)
        SimulationRunner._manual_stop_requests.discard(simulation_id)

    # The simulation finished; only the graph projection is partial.
    assert result.runner_status == RunnerStatus.STOPPED
    assert result.completed_at
    assert result.error and "Zep activity batch" in result.error
    # An inert updater must not stay registered or the report gate would keep
    # reporting a pending ingestion.
    assert registry == {}
    # state.json agrees with run_state.json instead of flipping to "failed".
    simulation = SimulationManager().get_simulation(simulation_id)
    assert simulation.status == SimulationStatus.STOPPED
    assert "Zep activity batch" in simulation.error


def test_structural_drain_failure_is_still_terminal_failure(sim_dirs, monkeypatch):
    """Only ingestion-incomplete is non-terminal; other drain errors still fail."""
    simulation_id = "sim-drain-failure"
    _persist_run_state(
        simulation_id, status=RunnerStatus.RUNNING, total_rounds=5, pid=_dead_pid()
    )
    _persist_simulation_state(simulation_id)

    registry = {simulation_id: object()}
    monkeypatch.setattr(
        runner_module.ZepGraphMemoryManager,
        "get_updater",
        classmethod(lambda _cls, _simulation_id: registry.get(_simulation_id)),
    )
    monkeypatch.setattr(
        runner_module.ZepGraphMemoryManager,
        "stop_updater",
        classmethod(
            lambda _cls, _simulation_id: (_ for _ in ()).throw(
                RuntimeError("Zep updater worker did not stop within 60s")
            )
        ),
    )
    SimulationRunner._graph_memory_enabled[simulation_id] = True

    try:
        with pytest.raises(RuntimeError, match="did not stop"):
            SimulationRunner.stop_simulation(simulation_id)
    finally:
        SimulationRunner._graph_memory_enabled.pop(simulation_id, None)
        SimulationRunner._manual_stop_requests.discard(simulation_id)

    state = SimulationRunner.get_run_state(simulation_id)
    assert state.runner_status == RunnerStatus.FAILED
    assert "did not stop" in state.error
    # The updater stays registered so the finalization can be retried.
    assert simulation_id in registry


def test_report_generate_after_recovery_is_not_blocked(sim_dirs, monkeypatch):
    """The real recovery path must unblock POST /api/report/generate."""
    simulation_id = "sim-report-gate"
    sim_dir = sim_dirs / simulation_id
    sim_dir.mkdir()
    _write_action_log(sim_dir, "twitter", rounds=15, actions_per_round=2, final_round=3)
    (sim_dir / "simulation.log").write_text("run interrupted\n", encoding="utf-8")
    _persist_run_state(
        simulation_id, status=RunnerStatus.STOPPING, total_rounds=15, pid=_dead_pid()
    )

    simulation = SimpleNamespace(
        project_id="proj-1", graph_id="graph-1", status=SimulationStatus.STOPPED
    )
    project = SimpleNamespace(
        project_id="proj-1",
        graph_id="graph-1",
        status=ProjectStatus.GRAPH_COMPLETED,
        simulation_requirement="mock requirement",
    )
    worker_targets = []

    class Tasks:
        def create_task(self, **_kwargs):
            return "task-1"

        def update_task(self, *_args, **_kwargs):
            pass

        def complete_task(self, *_args, **_kwargs):
            pass

        def fail_task(self, *_args, **_kwargs):
            pass

    class ParkedThread:
        def __init__(self, *, target, daemon):
            assert daemon is True
            self.target = target

        def start(self):
            worker_targets.append(self.target)

    class Agent:
        def __init__(self, **_kwargs):
            pass

        def generate_report(self, *, progress_callback, report_id):
            return SimpleNamespace(
                report_id=report_id,
                status=report_api.ReportStatus.COMPLETED,
                error=None,
            )

    monkeypatch.setattr(
        report_api,
        "SimulationManager",
        lambda: SimpleNamespace(get_simulation=lambda _simulation_id: simulation),
    )
    monkeypatch.setattr(
        report_api.ProjectManager,
        "get_project",
        classmethod(lambda _cls, _project_id: project),
    )
    # Only the run-state lookup stays real: it is the code under test.
    monkeypatch.setattr(
        report_api.ZepGraphMemoryManager,
        "get_updater",
        classmethod(lambda _cls, _simulation_id: None),
    )
    monkeypatch.setattr(
        report_api.ReportManager,
        "get_report_by_simulation",
        classmethod(lambda _cls, _simulation_id: None),
    )
    monkeypatch.setattr(
        report_api.ReportManager,
        "save_report",
        classmethod(lambda _cls, _report: None),
    )
    monkeypatch.setattr(report_api, "TaskManager", Tasks)
    monkeypatch.setattr(report_api, "ReportAgent", Agent)
    monkeypatch.setattr(report_api, "LLMClient", lambda: object())
    monkeypatch.setattr(report_api.threading, "Thread", ParkedThread)

    app = Flask(__name__)
    report_id = None
    try:
        with app.test_request_context(
            "/api/report/generate",
            method="POST",
            json={"simulation_id": simulation_id},
        ):
            result = report_api.generate_report()

        if isinstance(result, tuple):
            response, status = result
        else:
            response, status = result, 200
        body = response.get_json()
        assert status == 200, body
        assert body["data"]["already_generated"] is False
        report_id = body["data"]["report_id"]
        assert len(worker_targets) == 1

        recovered = SimulationRunner.get_run_state(simulation_id)
        assert recovered.runner_status == RunnerStatus.STOPPED
    finally:
        if report_id:
            from app.utils.zep_lifecycle import unregister_graph_reader

            unregister_graph_reader("graph-1", report_id)
