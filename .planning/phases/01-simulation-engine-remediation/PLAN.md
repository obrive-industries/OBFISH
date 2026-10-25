# Phase 01: Simulation Engine Remediation — Execution Plan

## Goal
Eliminate all structural failures, crashes, 429 token limit exhaustion, dummy text generation, and execution bottlenecks across the entire MiroFish simulation pipeline (Steps 1–4).

---

## Task 1: Resilient LLM Client, Multi-Key Pool & Rate-Limit Backoff Layer
**Files:**
- `backend/app/utils/llm_client.py`
- `backend/app/utils/openai_chat_compat.py`
- `backend/app/config.py`

**Key Changes:**
1. **Universal Key & Rate-Limit Rotator in `llm_client.py`:**
   - Normalize comma-separated `LLM_API_KEY` in `Config` and `LLMClient`.
   - Implement intelligent exponential backoff with jitter on 429 (`RateLimitError`) even when only 1 key is configured (respecting `retry-after` header when provided by Groq/OpenAI).
   - Add automatic fallback model/provider support if the primary model/key hits daily quota (TPD).
2. **Selective Tool Injection in `openai_chat_compat.py`:**
   - Only inject function tools (`insight_forge`, etc.) when `tools` are explicitly requested by the caller, rather than auto-injecting into every call where `response_format is None`.
3. **Verification:**
   - Run unit tests for `llm_client.py` testing key rotation, 429 backoff, and clean chat completions.

---

## Task 2: Token Budget Optimization for Step 1 (Graph) & Step 2 (Setup & Agents)
**Files:**
- `backend/app/services/ontology_generator.py`
- `backend/app/services/oasis_profile_generator.py`
- `backend/app/services/simulation_config_generator.py`
- `backend/app/services/zep_entity_reader.py`

**Key Changes:**
1. **Lean Persona Prompting & Batch Generation in `oasis_profile_generator.py`:**
   - Replace the verbose 2,000-word prompt with a targeted ~150-word persona specification. An OASIS agent only needs: concise role/bio, 2-sentence background, stance, and personality traits.
   - Batch persona generation: generate 5–10 agent personas in a single LLM JSON call instead of 1 individual prompt per entity.
   - Use normalized keys so comma-separated `LLM_API_KEY` never crashes with 401.
   - Reduce token usage in Step 2 from ~75,000 tokens down to < 10,000 tokens.
2. **Consolidated Simulation Config Generation in `simulation_config_generator.py`:**
   - Merge time, event, and agent activity generation into 1 unified JSON generation request with compact entity summaries.
   - Eliminate 4 redundant sequential LLM calls.
3. **Verification:**
   - Test `/prepare` endpoint with sample graph entities. Verify total tokens consumed < 15,000 and time taken < 15 seconds.

---

## Task 3: Fast-Path Simulation Execution & Concurrency Acceleration (Step 3)
**Files:**
- `backend/scripts/run_parallel_simulation.py`
- `backend/scripts/action_logger.py`
- `backend/app/services/simulation_runner.py`
- `backend/app/services/zep_graph_memory_updater.py`

**Key Changes:**
1. **Fast-Path Agent Stepping in `run_parallel_simulation.py`:**
   - Optimize agent activation distribution to prevent large bursts.
   - Implement caching and prompt compression for CAMEL `LLMAction` decisions.
   - Add explicit stdout flushing (`sys.stdout.flush()`) after action logging so the parent monitor thread receives real-time updates without buffer delay.
   - Enable SQLite WAL mode (`PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;`) on `twitter_simulation.db` and `reddit_simulation.db` to eliminate database locked errors between reader and writer threads.
2. **Non-Blocking Memory Updater Drain:**
   - Decouple Zep memory synchronization so slow Zep Cloud responses never block round progression or prevent natural transition to `COMPLETED`.
3. **Verification:**
   - Run a live 10-round test via `run_parallel_simulation.py`. Verify clean round progression, no DB locks, and swift completion.

---

## Task 4: Report Generation Integrity & Resilience (Step 4)
**Files:**
- `backend/app/services/report_agent.py`
- `backend/app/api/report.py`

**Key Changes:**
1. **Eradicate Fake Dummy Text Fallback:**
   - In `report_agent.py:1725`, remove the silent placeholder injection.
   - Implement true retry logic with exponential backoff on section generation. If rate-limited, wait for quota recovery or fail gracefully with explicit descriptive status rather than generating fake reports.
2. **Token-Efficient ReACT Loop:**
   - Optimize section outline and prompt: limit ReACT iterations from 4 down to 2 focused passes with compressed tool results.
   - Reduce report generation tokens from ~80,000 tokens down to < 20,000 tokens.
3. **Verification:**
   - Trigger `/api/report/generate` on a completed simulation. Verify authentic, detailed analytical sections without placeholder copy.

---

## Task 5: End-to-End Pipeline Integration & Benchmark Verification
**Files:**
- Full test suite across backend and API.

**Key Changes:**
1. Run full regression test suite (ensuring 166+ tests pass).
2. Execute a complete live end-to-end simulation from Scenario Input -> Graph Build -> Prepare -> Start -> Action Logs -> Generate Report.
3. Measure and verify:
   - Total pipeline token consumption < 50,000 tokens (survives Groq daily limit with 75% headroom).
   - Zero structural crashes or unhandled exceptions.
   - High-fidelity analytical report generated.
