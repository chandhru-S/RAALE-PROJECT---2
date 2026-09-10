# System Architecture — Operating Room Readiness Synchroniser (ORRS)

## Overview

The Operating Room Readiness Synchroniser (ORRS) is an enterprise full-stack clinical operations engine designed to eliminate avoidable operating theatre idle time by proactively evaluating resource readiness prior to scheduled surgical start times.

## Architectural Diagram

```text
                  SYNTHETIC HOSPITAL DATA GENERATOR
                       (scripts/generate_data.py)
                                   |
         -----------------------------------------------------
         |           |          |            |               |
         v           v          v            v               v
    Theatre       Staff     Equipment     Patient         Sterile
    Schedule      Roster     Status      Readiness        Supplies
         |           |          |            |               |
         -----------------------------------------------------
                                   |
                                   v
                      SQLITE DATABASE (orrs.db)
                                   |
                                   v
                   DATA QUALITY & FRESHNESS ENGINE
                     (services/uncertainty_engine.py)
                                   |
                                   v
                     READINESS SYNCHRONISER ENGINE
                     (services/readiness_engine.py)
            Checkpoints: T-60m | T-30m | T-15m | T-0m
                                   |
         -----------------------------------------------------
         |                         |                         |
         v                         v                         v
     BASELINE              PROTOTYPE SYNCHRONISER    FAILURE SIMULATOR
   (T-0m Manual)           (Multi-checkpoint)        (6 Test Triggers)
         |                         |                         |
         -----------------------------------------------------
                                   |
                                   v
                          EXPERIMENT ENGINE
                    (services/experiment_engine.py)
                                   |
                                   v
                         FASTAPI REST BACKEND
                          (backend/main.py)
                                   |
                                   v
                          REACT DASHBOARD UI
                           (frontend/src/)
```

## Data Flow Pipeline

1. **Synthetic Data Ingestion**: At startup, `generate_data.py` produces 320 synthetic operating sessions across 6 relational CSV datasets in `data/raw/`.
2. **Database Persistence**: `seed_database.py` maps CSV records to SQLite tables via SQLAlchemy ORM models.
3. **Data Quality & Uncertainty Validation**: For each scheduled session, `uncertainty_engine.py` inspects timestamp freshness (>30-60m old) and missing/NULL field states to compute a `confidence_score` (0-100%).
4. **Synchroniser Readiness Engine**: `readiness_engine.py` evaluates Patient (25%), Staff (25%), Equipment (20%), Supplies (15%), and Theatre (15%) scores, enforces safety-critical override rules (`Patient NOT READY` -> Overall `NOT READY`), and classifies status into `READY`, `AT_RISK`, `NOT_READY`, or `DATA_INCOMPLETE`.
5. **Baseline Comparison & Experiments**: `experiment_engine.py` compares traditional T-0m manual start-time checks against ORRS prototype proactive alerts, calculating Avoidable Idle Theatre Minutes per session.
6. **API & Dashboard Interface**: FastAPI serves REST endpoints to React + Vite frontend, enabling live OT status monitoring, drill-down assessment modals, alert acknowledgment, Recharts analytics, failure simulations, and programmatic evaluation reports.
