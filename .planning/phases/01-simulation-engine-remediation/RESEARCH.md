# Phase 01: Simulation Engine Remediation — Research & Root-Cause Audit

## 1. Executive Summary
An exhaustive audit of the MiroFish simulation engine from initial graph generation to final report delivery was conducted. The audit revealed five foundational issues causing the engine to fail structurally, get stuck, generate hollow reports, or run excessively slowly:

1. **Token Quota Depletion (The Primary Structural Blocker):**
   - The platform uses Groq (`api.groq.com/openai/v1`) with model `openai/gpt-oss-20b`. Groq on-demand / free accounts enforce a strict **200,000 Tokens Per Day (TPD)**, **8,000 Tokens Per Minute (TPM)**, and **30 Requests Per Minute (RPM)**.
   - A single end-to-end simulation run under the current design consumes **250,000 – 450,000 tokens**. As a result, almost every complete run hits HTTP 429 (`rate_limit_exceeded: Limit 200000, Used 198250`) during Step 3 or Step 4.
2. **Silent Failure & Hollow Report Degradation:**
   - In `backend/app/services/report_agent.py` (lines 1725–1735), when a 429 rate limit or LLM error occurs while generating report sections, the exception is caught and silently replaced with generic placeholder boilerplate:
     ```python
     section_content = (
         f"**{section.title} Analysis Summary**\n\n"
         f"Preliminary synthesis for this section indicates key behavioral patterns..."
     )
     ```
     The report is then saved and marked 100% complete, returning a hollow, meaningless report to the user without alerting them to the LLM failure.
3. **Explosion of Serial LLM Calls in Setup & Stepping:**
   - In `oasis_profile_generator.py`, each entity in the graph (20–50 entities) triggers an individual LLM prompt requesting a 2,000-word persona plus Zep retrieval, consuming ~2,500 tokens per entity (~75,000 tokens in Step 2 alone).
   - In `run_parallel_simulation.py`, each simulation round runs 5–20 agents. Each agent calls CAMEL `LLMAction()` individually with `semaphore=5`. For a 15–40 round simulation, this produces 100–300 individual LLM calls, causing severe latency (15–30s per round, up to 20 minutes total) and hitting TPM/RPM rate limits immediately.
4. **Multi-Key Inconsistency & Missing Retries:**
   - While `run_parallel_simulation.py` implements a custom key rotator for comma-separated `LLM_API_KEY`, `oasis_profile_generator.py` and `simulation_config_generator.py` pass `Config.LLM_API_KEY` directly to `OpenAI(api_key=...)`. If multiple keys are set (e.g. `key1,key2`), they crash with HTTP 401.
   - In `llm_client.py:149`, if `num_clients <= 1`, rate limits (429) and network blips are NOT retried—they raise immediately.
5. **Concurrency & Subprocess Deadlocks:**
   - SQLite concurrency between the simulation subprocess writing trace actions and the parent process reading `actions.jsonl` / database causes locks.
   - Zep Graph Memory Updater queue drainage locks the parent runner on simulation completion, stalling state transitions to `COMPLETED` and blocking the report API with 409 responses.

---

## 2. Step-by-Step Failure & Bottleneck Audit

### Step 1: Graph Construction & Ingestion
- **Code Paths:** `backend/app/api/graph.py`, `backend/app/services/ontology_generator.py`, `backend/app/services/graph_builder.py`, `backend/app/utils/zep.py`.
- **Identified Issues:**
  1. *Prompt Bloat:* `ONTOLOGY_MAX_TEXT_LENGTH` allows up to 30,000 characters to be sent in a single shot. This consumes ~8,000–10,000 input tokens in one request, risking immediate TPM 429 on Groq.
  2. *Zep Ingestion Polling Timeout:* `_wait_for_batch` in `graph_builder.py` polls `client.batch.get(batch_id)` every 3s. If Zep Cloud takes longer than `ZEP_INGESTION_WAIT_TIMEOUT_SECONDS` (300s) to extract entities from large document chunks, it raises `TimeoutError`, causing the whole graph build to fail.
  3. *Sequential Paging:* `fetch_all_nodes` and `fetch_all_edges` in `zep_paging.py` fetch sequentially with `limit=100`, introducing high network roundtrip overhead for graphs with 200+ nodes.

### Step 2: Environment Setup & Agent Creation (`/prepare`)
- **Code Paths:** `backend/app/api/simulation.py`, `backend/app/services/simulation_manager.py`, `backend/app/services/oasis_profile_generator.py`, `backend/app/services/simulation_config_generator.py`.
- **Identified Issues:**
  1. *Per-Entity LLM Spawning:* For $N$ entities, $N$ separate LLM requests are dispatched. If $N=30$, 30 full generation calls run concurrently (`parallel_count=3`), instantly saturating Groq's 8,000 TPM limit.
  2. *Verbose Prompting:* Prompts request 2,000 words per agent persona. OASIS social simulation only requires concise `bio`, concise `persona` (~80–120 words), and metadata tags (`profession`, `age`, `gender`, `mbti`). Excessive verbosity wastes 70% of the token budget.
  3. *Raw Key Pass-through:* `oasis_profile_generator.py:259` and `simulation_config_generator.py:240` initialize `OpenAI(api_key=self.api_key)`. If `LLM_API_KEY` contains multiple comma-separated keys, they fail immediately with 401.
  4. *Multi-Step Config Generation Overhead:* `simulation_config_generator.py` executes 4–6 separate LLM calls (time config, event config, N batches of 15 agents, platform configs) sending repetitive context blocks.

### Step 3: Simulation Execution (`/start`, Subprocess & Swarm Dynamics)
- **Code Paths:** `backend/app/services/simulation_runner.py`, `backend/app/services/simulation_ipc.py`, `backend/scripts/run_parallel_simulation.py`, `backend/app/services/zep_graph_memory_updater.py`.
- **Identified Issues:**
  1. *OASIS Stepping Latency:* In `run_parallel_simulation.py`, `env.step(actions)` calls CAMEL for 5–20 agents per round with `semaphore=5`. With network latency and rate limits, each round takes 15–30 seconds. A 40-round simulation takes 15–20 minutes.
  2. *Swallowed Step Exceptions:* Lines 1334–1336:
     ```python
     except Exception as step_err:
         log_info(f"第 {round_num + 1} 轮执行遇到非致命异常: {step_err}，跳过并继续下一轮")
     ```
     When 429 hits, the round executes 0 actions and skips to the next round, resulting in empty simulations.
  3. *Unbuffered Logging & Pipe Drops:* Child process stdout redirection can buffer output unless explicitly flushed, delaying action ingestion by the monitor thread.
  4. *Zep Ingestion Queue Blocking:* `zep_graph_memory_updater.py` attempts to write every action into Zep Cloud during simulation. If Zep Cloud slows down, the queue blocks terminal state transitions, causing the monitor thread to hang or reports to return 409.

### Step 4: Report Generation & Chat
- **Code Paths:** `backend/app/api/report.py`, `backend/app/services/report_agent.py`, `backend/app/utils/llm_client.py`.
- **Identified Issues:**
  1. *Hollow Section Dummy Text:* `report_agent.py:1725` replaces failed sections with dummy placeholder text instead of failing gracefully or retrying with backoff.
  2. *ReACT Token Drain:* 4 iterations * 4–5 sections = 16–20 large LLM calls per report (~80,000 tokens), exhausting whatever token quota survived Step 3.
  3. *Tool Calling Ambiguity:* `create_chat_completion` in `openai_chat_compat.py` unconditionally injects 4 function tool definitions when `response_format is None`. When models generate both `Final Answer:` and tool calls, it triggers conflict loops.

---

## 3. Remediation Architecture & Target Metrics

| Metric | Current State | Target State |
|---|---|---|
| **Token Consumption per Run** | 250,000 – 450,000 tokens | **< 45,000 tokens** (75–85% reduction) |
| **Step 2 (Prepare) Duration** | 45 – 90 seconds | **< 15 seconds** |
| **Step 3 (Simulation) Duration (15 rounds)** | 3 – 8 minutes | **< 45 seconds** |
| **Step 4 (Report) Failure Rate** | Frequent 429 → dummy text | **0% dummy text; resilient retries & fallbacks** |
| **Multi-Key & Provider Support** | Broken in Profile & Config generators | **Unified key pool & automatic 429 provider failover** |
