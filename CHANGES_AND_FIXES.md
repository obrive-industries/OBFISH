# 📋 Ob-Fish (MiroFish) - Complete Changelog & Architecture Modifications

**Repository:** `https://github.com/shivansh-006/ob-fish.git`  
**Production Domain:** `https://obfish.obrive.com`  
**Target Environment:** Hostinger KVM VPS (Ubuntu 22.04 / 24.04 LTS)  
**Author / Engineering:** Obrive Technical Operations  
**Date:** October 2026  

---

## 📌 Executive Summary

This document details all structural, configuration, and architectural modifications made to the original MiroFish platform to adapt it for **Obpark** and enable seamless production deployment on a **Hostinger VPS** under the custom domain `obfish.obrive.com`.

---

## 🚨 1. The Hostinger VPS "Network Error" (Root Cause & Fix)

### Symptom Observed
When accessing `https://obfish.obrive.com/process/new` and clicking "Generate Ontology", the system immediately failed with:
```
00:28:25.761 Starting ontology generation: Uploading files...
00:28:25.843 Exception in handleNewProject: Network Error
```

### Technical Root Cause
1. **Hardcoded Localhost Fallback:**  
   In `frontend/src/api/index.js`, the Axios instance had:
   ```javascript
   baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'
   ```
2. **Client-Side Execution Context:**  
   When a user opens `https://obfish.obrive.com` from their personal computer (laptop/mobile), the frontend JavaScript runs inside the **user's local browser**.
3. **Request Hijacking & Mixed Content Blocking:**  
   Without `VITE_API_BASE_URL` defined, Axios attempted to make HTTP requests to `http://localhost:5001/api/graph/ontology/generate` on the **visitor's local machine**, rather than the VPS!
   - Modern browsers immediately block HTTP calls from an HTTPS origin (**Mixed Content Security Violation**).
   - Even if allowed, the user's laptop has no Flask backend running on port 5001, resulting in an immediate connection failure (**Network Error** within 80ms).

---

## 🛠️ 2. Detailed File Modifications

### Commit `4c5cfae` — Fix Axios BaseURL for Reverse Proxy

#### 1. `frontend/src/api/index.js`
* **Purpose:** Switch from hardcoded `localhost:5001` to relative paths (`''`).
* **Before / After Diff:**
```diff
--- a/frontend/src/api/index.js
+++ b/frontend/src/api/index.js
@@ -2,8 +2,9 @@ import axios from 'axios'
 import i18n from '../i18n'
 
 // 创建axios实例
+// 生产环境与本地通过相对路径直接请求 /api/（生产环境由 Nginx 代理，本地由 Vite proxy 转发）
 const service = axios.create({
-  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001',
+  baseURL: import.meta.env.VITE_API_BASE_URL || '',
   timeout: 300000, // 5分钟超时（本体生成可能需要较长时间）
   headers: {
     'Content-Type': 'application/json'
```
* **Why it works:**
  - **In Production (`https://obfish.obrive.com`):** Calls go to `https://obfish.obrive.com/api/...`, which Nginx receives on port 443 (SSL) and internally proxies to `http://127.0.0.1:5001/api/...`. No CORS, no Mixed Content, no client-side localhost resolution.
  - **In Local Development (`http://localhost:3000`):** Calls go to `http://localhost:3000/api/...`, which Vite's dev server (`vite.config.js`) proxies to `http://localhost:5001/api/...`.

---

#### 2. `frontend/src/components/Step4Report.vue`
* **Purpose:** Fix hardcoded report download anchor tags to use relative URLs.
* **Before / After Diff (Lines 16 & 351):**
```diff
@@ -16,3 +16,3 @@
-  <a :href="`http://localhost:5001/api/report/${reportId}/download`" download ...>
+  <a :href="`/api/report/${reportId}/download`" download ...>

@@ -351,3 +351,3 @@
-  <a :href="`http://localhost:5001/api/report/${reportId}/download`" download ...>
+  <a :href="`/api/report/${reportId}/download`" download ...>
```
* **Why it works:** Allows one-click downloading of generated markdown reports directly through the secure Nginx domain without failing on the client machine.

---

### Commit `05b871b` — Obpark Integration, Groq LLM Compatibility & English Reports

#### 3. `obpark_seed_dossier.md` (New File)
* **Purpose:** Seed intelligence document for Obpark's 12-month simulation.
* **Contains:**
  - Target: 100,000 active users across 5 Tier-1 metro areas.
  - Revenue models: 15% booking commission, Valet parking subscriptions, EV charging fees.
  - Competitor landscape: Park+, Fastag, GetMyParking.
  - Operational metrics and stress-test assumptions for autonomous agents.

---

#### 4. `backend/app/utils/openai_chat_compat.py` (New File)
* **Purpose:** Compatibility layer for Groq Llama 3.3 70B and OpenAI SDK endpoints.
* **Why needed:**
  - Original MiroFish was hardwired for Alibaba DashScope / Qwen API schemas.
  - Groq enforces strict token limits and distinct tool-call response formats.
  - This module normalizes function tool calls and handles automatic retry and response formatting.

---

#### 5. `backend/app/services/report_agent.py`
* **Purpose:** Enforce English report generation & manage Groq context window.
* **Modifications:**
  - Updated system prompts and output formatting templates from Chinese to 100% executive English.
  - Implemented token compression for agent history so multi-round simulations do not overflow Groq's context window.
  - Added robust exception fallbacks if individual sections take longer than 60 seconds.

---

#### 6. `frontend/src/components/Step3Simulation.vue` & `Step5Interaction.vue`
* **Purpose:** UI Localization & Step 5 Agent Chat Activation.
* **Modifications:**
  - Translated progress headers, agent activity tags, and status badges from Chinese to English.
  - Fixed direct routing from Step 4 ("Report Complete") into Step 5 ("Chat with Report").

---

#### 7. `.gitignore`
* **Purpose:** Security and credential protection.
* **Modifications:**
  - Added `.env`, `.env*`, `.venv`, and `backend/uploads/` to prevent API keys (Groq, Zep) and simulation caches from leaking to public or collaborative git repositories.

---

## 🏗️ 3. Request Routing Architecture (Before vs After)

### Before (Caused Network Error on VPS)
```
User Laptop Browser (https://obfish.obrive.com)
       │
       └─── [Axios Request] ────► http://localhost:5001/api/graph/ontology/generate
                                         │
                                         ▼
                               [User Laptop Localhost]
                               ❌ Connection Refused / Mixed Content Block
```

### After (Clean Reverse Proxy via Nginx)
```
User Laptop Browser (https://obfish.obrive.com)
       │
       └─── [Axios Request] ────► https://obfish.obrive.com/api/graph/ontology/generate
                                         │ (Encrypted HTTPS Port 443)
                                         ▼
                                 [Hostinger VPS Nginx]
                                         │ (Proxied internally to 127.0.0.1:5001)
                                         ▼
                                 [Flask Backend API]
                                         │
                                         ▼
                               [Groq LLM + Zep Graph]
                               ✅ 200 OK Response Streamed Back
```

---

## 🚀 4. How to Apply These Updates on Hostinger VPS

Run the following commands on your server terminal:

```bash
# 1. Navigate to the repository folder
cd /var/www/ob-fish

# 2. Pull the latest commits from GitHub
git pull origin main

# 3. If running via Docker:
docker compose restart

# 4. If running via PM2 / Node:
pm2 restart all
```

Once pulled, perform a **Hard Refresh** (`Ctrl + Shift + R` on Windows/Linux or `Cmd + Shift + R` on Mac) on `https://obfish.obrive.com` to clear the browser's cached JavaScript.

---
*Document produced for Obrive Technical Operations • Repository: shivansh-006/ob-fish*
