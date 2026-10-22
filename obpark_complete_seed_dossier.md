# Obpark Enterprise Ecosystem: Complete Architecture & Multi-Agent Seed Dossier

## 1. Executive Summary & Enterprise Scope
**Obpark** (operated by Obrive Industries) is India's next-generation integrated smart mobility and automotive services platform. It unifies four critical pillars of modern urban vehicle ownership into a single, cohesive ecosystem:
1. **Smart Parking & Valet Management**: Real-time slot discovery, airport/mall parking reservations, valet crew assignment, and dynamic QR-based check-in/check-out.
2. **Automotive Utilities & FASTag Services**: Automated Vehicle Registration Certificate (RC) lookups, FASTag balance inquiry, and instant toll recharge verification via external gateways (**Surepass API**).
3. **E-Commerce Automotive Marketplace**: Curated direct-to-consumer marketplace for vehicle accessories, dashcams, hardware, and essentials, featuring real-time inventory and **Razorpay** checkout.
4. **Real-Time Lifecycle Notification & Event Engine**: Event-driven notification gateway (WebSockets + Firebase FCM) delivering sub-second updates across the user lifecycle (e.g., `BOOKING_ACCEPTED`, `CREW_ARRIVED`, `TRIP_STARTED`, `TRIP_COMPLETED`, `KYC_APPROVED`).

---

## 2. Integrated System Architecture (All 15 Modules)

The backend (`obpark-backend`) is built on **Node.js v24+** and **NestJS v11** with **PostgreSQL** and **Prisma ORM v7**, structured across 15 tightly coupled domain modules:

### A. Core Mobility & Parking Dispatch
- **`BookingModule`**: Manages parking spot reservations, duration calculation, pricing rules, QR code issuance, and entry/exit barriers.
- **`CrewModule`**: Manages on-ground parking staff, valets, and field inspectors. Handles shift attendance, job offer assignment (`NEW_JOB_OFFER`), location telemetry, and vehicle handoff states.
- **`VehicleModule`**: Connects with government and transport databases via Surepass API to validate license plates, verify chassis/engine numbers, and fetch FASTag balances.
- **`FormsModule`**: Dynamic verification forms, vehicle inspection checklist before valet handover, photo uploads for damage documentation, and KYC verification.

### B. Commerce, Billing & Payments
- **`ProductsModule`**: Manages automotive product catalog, dynamic pricing, category hierarchies, and stock levels.
- **`CartModule`**: Handles user shopping carts, persistent cart storage, item discounts, and coupon validations.
- **`PaymentModule`**: Integrates **Razorpay Payment Gateway**. Generates order IDs, handles webhook callbacks, performs cryptographic signature verification, idempotency checking, and refund processing.
- **`BillingModule`**: Generates GST-compliant tax invoices, handles ledger entries, calculates convenience fees, and generates downloadable PDF receipts.

### C. Real-Time Communications & Alerts
- **`NotificationModule`**: Hybrid communication pipeline:
  - **WebSocket Gateway**: Pushes instant state transitions to active mobile and web clients.
  - **Firebase Cloud Messaging (FCM)**: Mobile push notifications for background apps.
  - **Transactional Alerts**: SMS and WhatsApp alerts for mission-critical notifications (`CREW_ARRIVED`, `BOOKING_ACCEPTED`, `PAYMENT_SUCCESS`).

### D. Identity, Security & Operations
- **`AuthModule`**: Firebase Authentication (Phone OTP, Google OAuth) bridged to custom cryptographically signed JWT sessions.
- **`UsersModule` & `ProfileModule`**: Manages customer profiles, vehicle ownership mappings, driving preferences, and saved emergency contacts.
- **`AdminModule`**: Central operations dashboard providing system health monitoring, booking overrides, crew assignment interventions, and financial reconciliations.
- **`StorageModule`**: S3/Local object storage for KYC identity cards, vehicle damage inspection photos, and invoice storage.

---

## 3. End-to-End Operational Workflows

### Workflow 1: The Airport Smart Parking & Valet Journey
1. **Discovery & Booking**: A commuter traveling for 3 days books an airport valet slot via Obpark 24 hours in advance.
2. **Crew Dispatch**: Upon approaching the airport terminal, the system broadcasts `NEW_JOB_OFFER` to nearby active valets. A certified valet accepts (`BOOKING_ACCEPTED`).
3. **Vehicle Inspection & Handover**: Valet arrives (`CREW_ARRIVED`), takes baseline photos of the vehicle using `FormsModule`, records fuel/odometer readings, and hands a digital inspection token to the customer.
4. **Trip & Secure Parking**: Valet parks the car in Obpark's secure monitored lot (`TRIP_STARTED` -> `TRIP_COMPLETED`).
5. **Return & Delivery**: Upon flight return, customer requests car retrieval. Valet delivers vehicle to terminal curb; customer scans QR to pay final parking charges via Razorpay.

### Workflow 2: Toll Plaza FASTag Crisis Management
1. **Low-Balance Detection**: Commuter approaching a highway toll discovers their FASTag balance is below threshold.
2. **Instant Verification**: Commuter enters registration number into Obpark; `VehicleModule` queries Surepass API in real time.
3. **Emergency Top-Up**: User recharges via UPI through Razorpay. Webhook instantly acknowledges transaction and pushes confirmation via `NotificationModule`.

### Workflow 3: Automotive Accessories Cross-Sell
1. Commuters booking long-distance weekend parking are recommended highway essentials (emergency puncture kits, dashcams, fast chargers).
2. Items added to `CartModule` are bundled with the parking invoice for unified checkout.

---

## 4. Real-World Failure Modes & Friction Scenarios (For Simulation)

To stress-test Obpark's ecosystem in MiroFish, the multi-agent swarm should model the following real-world stress points:

1. **Third-Party API Rate Limiting & Latency Spikes**:
   - Surepass API takes 6-10 seconds to respond or returns HTTP 429 during national holiday traffic rushes.
   - Razorpay webhook delivery delays causing users to wonder if their FASTag recharge went through.
2. **Valet Crew Supply-Demand Mismatch**:
   - Flight delays cause 50 customers to request vehicle deliveries simultaneously at Terminal 2, resulting in longer pickup queues.
3. **Push Notification Deliverability Failures**:
   - Network connectivity drops in underground parking basements preventing WebSocket receipt of `CREW_ARRIVED`.
4. **Data Privacy & KYC Scrutiny**:
   - Customer sensitivity regarding vehicle registration data and vehicle inspection photograph storage.
5. **Competitive Poaching & Churn**:
   - Competing apps (Park+, Fastag apps, Airport parking aggregators) targeting Obpark users with cashback ads during service latency events.

---

## 5. Swarm Agent Personas & Ecosystem Stakeholders

The simulation environment will simulate social interactions and behavioral trends among 6 key persona groups:

1. **Daily Urban Commuters & Corporate Travelers (`DailyCommuterEntity`)**:
   - Values predictability and sub-minute parking check-ins. Extremely vocal on social media (Twitter/X) if airport valet pickup exceeds 10 minutes.
2. **Automotive Enthusiasts & Highway Drivers (`VehicleOwnerEntity`)**:
   - Focuses on vehicle safety, accurate FASTag toll logs, and high-quality genuine accessories.
3. **On-Ground Valet & Parking Crew Agents (`CrewAgentEntity`)**:
   - Field staff balancing tip income, job dispatch fairness, attendance tracking, and physical transit bottlenecks.
4. **E-Commerce Buyers & Bargain Shoppers (`OnlineShopperEntity`)**:
   - Buys automotive lifestyle products; expects Amazon-grade order tracking, packaging quality, and hassle-free returns.
5. **Customer Support & Social Response Operations (`SupportAgentEntity`)**:
   - Obpark internal brand representatives de-escalating customer complaints, issuing recharge refunds, and reassuring users during gateway outages.
6. **Fintech & Mobility Competitors (`CompetitorEntity`)**:
   - Competing platforms monitoring Obpark's service sentiment and advertising aggressive promotional discounts when Obpark experiences downtime.

---

## 6. Simulation Objectives & Predictive Outcomes

1. **12-Month Sentiment & Brand Evolution**: Trace public perception trajectory from launch to maturity across Info Plaza (Twitter) and Topic Community (Reddit).
2. **Operational Resilience Index**: Measure customer churn percentage during peak holiday rushes when gateway timeouts occur.
3. **Crew Utilization & Satisfaction Dynamics**: Assess on-ground valet morale and customer satisfaction correlation under high booking volumes.
4. **Feature Impact & Retention Drivers**: Quantify the impact of instant real-time notification alerts on customer trust scores and repeat booking rates.
