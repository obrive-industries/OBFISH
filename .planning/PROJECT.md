# MiroFish (Brain) Social Simulation Platform

## Overview
MiroFish is an autonomous multi-agent social simulation platform that builds knowledge graphs from input scenarios, instantiates synthetic demographic swarms (Twitter & Reddit agents via OASIS / Camel-AI), simulates complex societal discourse and polarization over simulated time, and generates deep analytical reports with follow-up agent interview capabilities.

## Architecture
- **Step 1: Graph Construction**: Text extraction, ontology generation via LLM, text chunking, and knowledge graph ingestion via Zep Cloud.
- **Step 2: Environment Setup & Agent Creation**: Entity reading, OASIS agent profile generation, simulation parameter and schedule generation.
- **Step 3: Simulation Execution**: Dual-platform parallel simulation (`run_parallel_simulation.py`), CAMEL multi-agent stepping, SQLite action tracing, real-time IPC logging, and Zep graph memory synchronization.
- **Step 4: Report Generation & Chat**: Multi-section ReACT analytical report synthesis, graph entity reasoning, and interactive agent interviews.
