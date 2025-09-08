# Talk To Prometheus (Teaching skeleton)

This repository is a compact, teachable skeleton for **Talk To Prometheus** — a natural-language interface that converts user questions into Prometheus queries, runs them locally, and analyzes results.

---

## What you get in this archive

- A simplified, single-file-per-concern structure under `src/` (easy to teach)
- `analysis-runner/` container image and job for heavy analysis
- A small CLI for running queries locally
- `README` (this file), `.env.example`, and a `docker-compose.yml` for convenience

---

## Quick start (local, no Docker)

1. Copy `.env.example` to `.env` and fill any values you need:
   ```bash
   cp .env.example .env
   ```

2. Install requirements (recommended in a venv):
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the CLI:
   ```bash
   python src/main.py query "What is memory available on node-exporter:9100 in the last 30m?"
   ```

> The current codebase is a teaching skeleton. It includes basic heuristics for planning queries and simple execution and analysis code paths. It also includes placeholders where you can hook a real LLM (OpenRouter / Qwen) and the CrewAI orchestration.

---

## Running heavy analysis in Docker (recommended for Windows)

The `analysis-runner` image provides a small Python environment (pandas, numpy) to process large JSON data. The project writes large query results to `./data/run.json` and the runner can be used to analyze keys from that file.

Build the runner image:
```bash
docker build -t talk-prom-analysis ./analysis-runner
```

Run the job (example):
```bash
docker run --rm -v ${PWD}/data:/data talk-prom-analysis python /runner/job.py --file /data/run.json --key exec/2025-...
```

If you prefer the code to run locally instead of Docker, set `DOCKER_PREFER=false` in your `.env`.

---

## Project layout

```
talk-to-prometheus/
├── docker-compose.yml
├── .env.example
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── agents.py
│   ├── tasks.py
│   ├── utils.py
│   ├── schemas.py
│   ├── tools.py
│   └── config.py
└── analysis-runner/
    ├── Dockerfile
    └── job.py
```

---

## Included architecture plan (high-level)

# Talk To Prometheus – High-Level Architecture Plan

## Overview
The "Talk To Prometheus" system allows users to interact with Prometheus using natural language. The workflow includes:
- User query input
- Planning and refinement into Prometheus-compatible queries
- Execution of queries and data storage
- Analysis of results with fallback to local file-based processing when data is large

## Core Components

### 1. Agents (in one file)
- **PlanningAgent** – Converts user query into structured Prometheus queries.
- **ExecutorAgent** – Runs queries on Prometheus and stores results (memory/JSON).
- **AnalyzerAgent** – Analyzes results and uses Docker-based local analysis if needed.

### 2. Tasks (in one file)
- **PlanTask** – Orchestrates PlanningAgent.
- **ExecuteTask** – Orchestrates ExecutorAgent.
- **AnalyzeTask** – Orchestrates AnalyzerAgent.

### 3. Utils (in one file)
- Helper functions for time ranges, PromQL sanitization, file operations, etc.

### 4. Schemas (in one file)
- Pydantic models for Plan, Execution Results, and Analysis.

## Overall Flow of the System

1. **User Input**
   - A user asks a question in natural language (e.g., "What is the CPU usage for the last 1 hour?").

2. **PlanTask → PlanningAgent**
   - CrewAI invokes **PlanningAgent** with the user query.
   - Tools used: None at this stage (LLM only).
   - Decisions:
     - Determine which PromQL query or queries are needed.
     - Decide the correct endpoint (`query` or `query_range`).
     - Choose a time window and step size if not provided.
     - Package output into a **Plan schema**.

3. **ExecuteTask → ExecutorAgent**
   - CrewAI passes the Plan schema to **ExecutorAgent**.
   - Tools used: **Prometheus query tool**, **File storage tool**.
   - Decisions:
     - Execute queries against Prometheus.
     - Estimate result size.
       - If small → keep in memory.
       - If large → save to JSON file with comments.
     - Return an **Execution Result schema** referencing memory or file.

4. **AnalyzeTask → AnalyzerAgent**
   - CrewAI passes Execution Results to **AnalyzerAgent**.
   - Tools used: **Stats helper** for small data, **Docker Python runner** for large data.
   - Decisions:
     - If result in memory → run quick stats and summary directly.
     - If result in file → launch Docker container to run analysis on JSON file.
   - Produces an **Analysis schema** with:
     - Summary of metrics (min, max, avg, percentiles).
     - Findings (e.g., anomalies, trends).
     - Recommendations and possible next questions.

5. **Final Output**
   - The Analysis schema is returned to the user.
   - CLI (main.py) can display both raw JSON output and a human-readable summary.

---

## Notes / Next steps

- Replace the simple PlanningAgent heuristics with a CrewAI workflow connected to an LLM (Qwen via OpenRouter).
- Harden PromQL generation and sanitization before running queries in production.
- Add unit tests and integration tests (mock Prometheus server).
