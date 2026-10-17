# Obpark Project Seed Dossier for MiroFish Swarm Simulation

## 1. Project Background & Business Overview
**Obpark** is an emerging dual-utility automotive e-commerce and vehicle services platform based in India. It aims to bridge the gap between automotive utility management and automotive retail.

### Core Value Propositions:
1. **Automotive Utilities**:
   - Real-time FASTag lookup, balance inquiry, and recharge verification.
   - Vehicle Registration Certificate (RC) lookups and vehicle validation.
   - Integration with external government/data aggregator gateways via **Surepass API**.
2. **E-Commerce Automotive Marketplace**:
   - Catalog of car accessories, essentials, and hardware products.
   - Real-time shopping cart and dynamic pricing engine.
   - Integrated Indian payment checkout via **Razorpay**.
   - User authentication via **Firebase OTP / Social Logins** paired with backend JWT issuance.

---

## 2. Technical Architecture & Current State
The backend service (`obpark-backend`) is built as a monolithic service designed with domain modules:

- **Framework**: Node.js v24+, NestJS v11 (TypeScript)
- **Database & ORM**: PostgreSQL with Prisma ORM v7
- **Authentication**: Firebase Admin SDK (ID token verification) + Custom JWT session tokens
- **External Integrations**:
  - `Surepass API`: Handles all FASTag and RC lookup HTTP requests.
  - `Razorpay API`: Generates order IDs and verifies payment signatures.
- **Data Persistence**:
  - PostgreSQL stores users, addresses, orders, and payment records.
  - **Notice**: Currently, the product catalog is partially hardcoded in static TypeScript arrays rather than completely driven by database tables.

---

## 3. Known Technical Debt, Vulnerabilities & System Bottlenecks
For the multi-agent prediction simulation, the following real-world architectural friction points are active:

1. **Third-Party API Dependency & Lack of Caching**:
   - Every FASTag and RC request directly makes an outbound HTTP call to Surepass.
   - **No Redis cache** is currently installed. Repeated queries for identical vehicle numbers trigger duplicate paid API calls and accumulate network latency.
2. **Security Vulnerabilities**:
   - `pnpm audit` identifies **76 package vulnerabilities** (1 Critical, 45 High).
   - Known race condition in `multer < 2.3.0` for file uploads.
   - No centralized global exception sanitization filter; unexpected Prisma errors may leak database schema details in error payloads.
3. **Database & Transaction Strain**:
   - Duplicate models exist in Prisma schema (`User` vs `Users`).
   - During payment confirmation, cart items are sequentially deleted inside the payment callback transaction block, creating a potential latency bottleneck on high-traffic checkout spikes.
4. **Testing Debt**:
   - Test suite currently encounters Dependency Injection errors in `StorageService` (`LocalStorageService` missing in module metadata), leaving core pricing logic without automated regression guarantees.

---

## 4. Key Simulated Personas & Stakeholders (Target Swarm)

In the MiroFish parallel simulation, the digital environment should be populated with distinct agent personas representing:

1. **Daily Commuters & Vehicle Owners**:
   - Needs instantaneous FASTag status and reliable balance checks before hitting highway toll plazas.
   - Highly sensitive to app downtime, incorrect balance reports, or delayed recharge reflections.
2. **Online Automotive Accessory Shoppers**:
   - Price-conscious consumers buying dashboard cams, air purifiers, and seat covers.
   - Demands instantaneous Razorpay checkout; intolerant of payment deductions with delayed order confirmations.
3. **Automotive Tech Critics & Ethical Security Researchers**:
   - Scrutinizes API responses for data leakage (chassis numbers, owner names from RC lookup).
   - Tests file upload endpoints for KYC/crew document vulnerabilities.
4. **Fintech & Automotive Competitors** (e.g., Park+, Paytm FASTag, Cars24):
   - Monitors Obpark's stability, pricing, and server reliability.
   - Ready to capture churned users if Obpark experiences downtime during peak transit hours.
5. **Obpark Customer Support & Operations Agents**:
   - Handles escalated tickets when third-party gateways (Surepass / Razorpay) report timeouts or inconsistent states.

---

## 5. Simulation Scenarios & Prediction Objectives

MiroFish is tasked with simulating social interaction, stakeholder behavior, and predicting outcomes across the following dimensions:

### Objective 1: High-Volume Surge Simulation (The "Diwali Festive Rush")
- **Premise**: Traffic increases by 10x (50,000 daily active users). Highway toll recharges surge while a 20% discount sale is launched on car accessories.
- **Simulation Goal**: Predict user satisfaction drop, checkout abandonment rates, Surepass API rate-limit failure cascades, and server stability.

### Objective 2: Third-Party Downtime & Fault Injection
- **Premise**: Surepass API experiences intermittent latency spikes (5-8 seconds per call) or complete 429 rate-limiting.
- **Simulation Goal**: Observe how vehicle owners react, how complaints propagate across social channels, and quantify customer churn.

### Objective 3: Security & Trust Assessment
- **Premise**: Public discourse regarding KYC documents and vehicle registration privacy.
- **Simulation Goal**: Evaluate customer retention and trust score if an edge-case error message exposes backend database structures.

### Objective 4: Remediation Impact Prediction
- **Premise**: Obpark introduces Redis caching with a 24-hour TTL for vehicle lookups, updates vulnerable packages, and migrates the catalog to PostgreSQL.
- **Simulation Goal**: Predict cost savings on third-party APIs, user retention recovery, and platform reliability index.
