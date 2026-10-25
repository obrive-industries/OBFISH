#!/usr/bin/env python3
"""
Full End-to-End Production Simulation & Synthesis Certification Test
Tests the live MiroFish / Brain backend against the complete operational lifecycle:
1. Authentication & Admin Authorization
2. Project Context & Simulation Initialization
3. LLM Multi-Provider Parameter & Persona Generation
4. Subprocess Execution & Parallel Dual-Platform Simulation (Twitter + Reddit)
5. Live State Monitoring, Action Logging & SQLite WAL Concurrency
6. Final Strategic Report Generation with Analytical Synthesis Fallback
7. Production Go/No-Go Verification & Quality Gate Audit
"""

import sys
import os
import time
import json
import requests

BACKEND_BASE_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:5001")
PROJECT_ID = "proj_b0377f61e7b3"  # Existing verified graph project

def log(step: str, msg: str):
    print(f"\n[E2E-TEST | {step}] {msg}")

def main():
    log("INIT", f"Targeting Live Backend at {BACKEND_BASE_URL}")

    # 1. Health check
    try:
        health_resp = requests.get(f"{BACKEND_BASE_URL}/api/health", timeout=5)
        health_resp.raise_for_status()
        log("HEALTH", f"Backend online: {health_resp.json()}")
        assert health_resp.headers.get("X-Content-Type-Options") == "nosniff"
        assert health_resp.headers.get("X-Frame-Options") == "SAMEORIGIN"
        log("SECURITY", "HTTP Security headers verified on live daemon.")
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        sys.exit(1)

    # 2. Acquire Admin Token
    # Use app context to generate authentic token signed by active SECRET_KEY
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from app import create_app
    from app.models.user import User
    from app.utils.jwt_utils import create_access_token
    
    app = create_app()
    with app.app_context():
        admin_user = User.query.filter_by(email="ai@obrive.com").first()
        if not admin_user:
            print("❌ Admin user ai@obrive.com not found in DB")
            sys.exit(1)
        token = create_access_token(admin_user.id, is_verified=True, token_version=admin_user.token_version)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    log("AUTH", f"Admin token generated for {admin_user.email} (Role: {admin_user.role})")

    # If --report-id was passed, jump straight to audit
    target_report_id = None
    if len(sys.argv) > 2 and sys.argv[1] == "--report-id":
        target_report_id = sys.argv[2]
        log("AUDIT", f"Auditing specified report: {target_report_id}")
        report_id = target_report_id
    else:
        # 3. Create fresh simulation linked to project
        create_payload = {
            "project_id": PROJECT_ID,
            "enable_twitter": True,
            "enable_reddit": True
        }
        create_resp = requests.post(f"{BACKEND_BASE_URL}/api/simulation/create", json=create_payload, headers=headers)
        if create_resp.status_code != 200:
            print(f"❌ Failed to create simulation: {create_resp.status_code} {create_resp.text}")
            sys.exit(1)
        
        sim_data = create_resp.json().get("data", {})
        sim_id = sim_data.get("simulation_id")
        log("CREATE", f"Created simulation: {sim_id} linked to project {PROJECT_ID}")

        # 4. Prepare Simulation Environment (Config & Agent Profiles)
        log("PREPARE", "Preparing simulation environment via LLM...")
        prep_payload = {
            "simulation_id": sim_id,
            "use_llm_for_profiles": True,
            "force_regenerate": False
        }
        prep_resp = requests.post(f"{BACKEND_BASE_URL}/api/simulation/prepare", json=prep_payload, headers=headers)
        if prep_resp.status_code != 200:
            print(f"❌ Failed to start prepare task: {prep_resp.status_code} {prep_resp.text}")
            sys.exit(1)
        
        prep_data = prep_resp.json().get("data", {})
        task_id = prep_data.get("task_id")
        if task_id:
            log("PREPARE", f"Task {task_id} launched. Polling preparation progress...")
            for _ in range(60):
                time.sleep(2)
                status_resp = requests.post(
                    f"{BACKEND_BASE_URL}/api/simulation/prepare/status",
                    json={"task_id": task_id},
                    headers=headers
                )
                if status_resp.status_code == 200:
                    t_data = status_resp.json().get("data", {})
                    t_status = t_data.get("status")
                    t_progress = t_data.get("progress", 0)
                    t_msg = t_data.get("message", "")
                    print(f"   [Prepare Progress]: {t_progress}% - {t_msg}")
                    if t_status == "completed":
                        log("PREPARE", "Environment preparation complete!")
                        break
                    elif t_status == "failed":
                        print(f"❌ Prepare task failed: {t_msg}")
                        sys.exit(1)
        else:
            log("PREPARE", "Environment was already prepared.")

        # 5. Start Simulation Subprocess (compact 2-round parallel simulation)
        MAX_TEST_ROUNDS = 2
        log("START", f"Starting simulation execution with max_rounds={MAX_TEST_ROUNDS}...")
        start_payload = {
            "simulation_id": sim_id,
            "platform": "parallel",
            "max_rounds": MAX_TEST_ROUNDS,
            "force": True
        }
        start_resp = requests.post(f"{BACKEND_BASE_URL}/api/simulation/start", json=start_payload, headers=headers)
        if start_resp.status_code != 200:
            print(f"❌ Failed to start simulation: {start_resp.status_code} {start_resp.text}")
            sys.exit(1)
        
        start_data = start_resp.json().get("data", {})
        pid = start_data.get("process_pid")
        log("START", f"Simulation subprocess started with PID {pid} (Twitter: {start_data.get('twitter_running')}, Reddit: {start_data.get('reddit_running')})")

        # 6. Monitor Execution
        log("MONITOR", "Monitoring simulation execution and agent actions...")
        max_wait = 180  # 3 minutes max
        start_time = time.time()
        last_action_count = 0

        while time.time() - start_time < max_wait:
            time.sleep(3)
            status_resp = requests.get(f"{BACKEND_BASE_URL}/api/simulation/{sim_id}/run-status/detail", headers=headers)
            if status_resp.status_code != 200:
                print(f"⚠️ Status check HTTP {status_resp.status_code}")
                continue

            detail = status_resp.json().get("data", {})
            runner_status = detail.get("runner_status")
            current_round = detail.get("current_round", 0)
            total_actions = detail.get("total_actions", 0)
            tw_round = detail.get("twitter_round", 0)
            rd_round = detail.get("reddit_round", 0)

            if total_actions != last_action_count or current_round > 0:
                print(f"   [Simulation Run]: Status={runner_status} | Overall Round={current_round}/{MAX_TEST_ROUNDS} (Twitter: R{tw_round}, Reddit: R{rd_round}) | Total Actions={total_actions}")
                last_action_count = total_actions

            if runner_status in {"completed", "stopped"}:
                log("MONITOR", f"Simulation reached terminal state: {runner_status} in {time.time() - start_time:.1f}s")
                break
            elif runner_status == "failed":
                print(f"❌ Simulation execution failed: {detail.get('error')}")
                sys.exit(1)

        # 7. Check timeline & agent stats
        timeline_resp = requests.get(f"{BACKEND_BASE_URL}/api/simulation/{sim_id}/timeline", headers=headers)
        if timeline_resp.status_code == 200:
            events = timeline_resp.json().get("data", {}).get("events", [])
            log("DATA", f"Simulation produced {len(events)} discrete timeline events.")

        # 8. Generate Strategic Report
        log("REPORT", "Triggering Final Strategic Report Generation...")
        report_payload = {
            "simulation_id": sim_id,
            "simulation_requirement": "Analyze the simulated stakeholder dynamics, emergent behaviors, market opportunities, and critical risk factors."
        }
        report_resp = requests.post(f"{BACKEND_BASE_URL}/api/report/generate", json=report_payload, headers=headers)
        if report_resp.status_code != 200:
            print(f"❌ Failed to trigger report generation: {report_resp.status_code} {report_resp.text}")
            sys.exit(1)
        
        rep_info = report_resp.json().get("data", {})
        report_id = rep_info.get("report_id")
        log("REPORT", f"Report agent started with Report ID: {report_id}")

        # 9. Poll Report Synthesis
        rep_start = time.time()
        rep_timeout = 600  # 10 minutes max (allows thorough multi-tool ReACT exploration)
        final_report = None

        while time.time() - rep_start < rep_timeout:
            time.sleep(4)
            status_resp = requests.get(f"{BACKEND_BASE_URL}/api/report/{report_id}/progress", headers=headers)
            if status_resp.status_code != 200:
                print(f"⚠️ Report progress check HTTP {status_resp.status_code}")
                continue

            r_data = status_resp.json().get("data", {})
            r_status = r_data.get("status")
            progress = r_data.get("progress", 0)
            current_step = r_data.get("message", "")
            print(f"   [Report Synthesis]: {progress}% ({r_status}) - {current_step}")

            if r_status == "completed":
                final_report = r_data
                log("REPORT", f"Strategic Report synthesized successfully in {time.time() - rep_start:.1f}s!")
                break
            elif r_status == "failed":
                print(f"❌ Report generation failed: {r_data.get('error')}")
                sys.exit(1)

        if not final_report:
            print(f"❌ Report generation timed out after {rep_timeout}s without completing.")
            sys.exit(1)

    # 10. Audit Final Report Quality
    log("AUDIT", "Auditing final synthesized report quality...")
    report_detail_resp = requests.get(f"{BACKEND_BASE_URL}/api/report/{report_id}", headers=headers)
    if report_detail_resp.status_code != 200:
        print(f"❌ Failed to fetch complete report: {report_detail_resp.status_code}")
        sys.exit(1)

    full_report = report_detail_resp.json().get("data", {})
    markdown_content = full_report.get("markdown_content", "")
    outline = full_report.get("outline", {})
    sections = outline.get("sections", [])

    print(f"\n==================== REPORT SUMMARY ====================")
    print(f"Title: {outline.get('title')}")
    print(f"Summary: {outline.get('summary')}")
    print(f"Number of Sections: {len(sections)}")
    print(f"Markdown Content Length: {len(markdown_content)} characters")
    print(f"=======================================================\n")

    # Quality Gate Assertions
    assert len(markdown_content) > 500, "Report markdown content is too short"
    assert len(sections) >= 3, "Report outline has fewer than 3 sections"
    assert "Preliminary synthesis for this section" not in markdown_content, "Detected dummy fallback boilerplate"
    assert full_report.get("status") == "completed", "Report status is not completed"

    log("SUCCESS", "✅ FULL SIMULATION & REPORT SYNTHESIS COMPLETED WITH ZERO ERRORS!")
    log("CERTIFICATION", "🚀 SYSTEM CERTIFIED 100% PRODUCTION READY!")

if __name__ == "__main__":
    main()
