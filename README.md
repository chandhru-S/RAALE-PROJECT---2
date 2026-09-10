# Operating Room Readiness Synchroniser (ORRS)

[![Full-Stack MVP](https://img.shields.io/badge/Status-Functioning%20MVP-success)](#)
[![Python FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20SQLAlchemy-blue)](#)
[![React TypeScript](https://img.shields.io/badge/Frontend-React%20%7C%20TypeScript%20%7C%20Vite-cyan)](#)
[![SQLite Database](https://img.shields.io/badge/Database-SQLite-lightgrey)](#)
[![Pytest Passed](https://img.shields.io/badge/Tests-8%2F8%20Passed-emerald)](#)

A complete, production-grade full-stack engineering + product discovery project built for multi-specialty hospitals to eliminate avoidable operating theatre idle time by synchronising resource readiness prior to scheduled surgery start times.

---

## 1. Problem Statement

An operating theatre loses valuable clinical time when seven interdependent resources are not ready together:
1. Patient Preparation & Consent
2. Surgeon Availability
3. Anaesthetist Availability
4. Surgical Nursing Staff
5. Bio-Medical Equipment
6. Sterile Surgical Supplies (CSSD)
7. Operating Theatre Space & Turnover

Traditional hospital workflows evaluate readiness reactively at scheduled start time ($T-0m$). If equipment is faulty or consent is incomplete, the surgery is delayed and the operating room remains idle. **ORRS identifies these readiness bottlenecks BEFORE the scheduled surgery start time.**

---

## 2. System Architecture

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

---

## 3. Technology Stack

- **Backend**: Python 3.14, FastAPI, Pydantic v2, SQLAlchemy 2.0
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Recharts, Lucide Icons, Axios
- **Database**: SQLite (`orrs.db`), designed for clean PostgreSQL migration
- **Data Processing**: Pandas, NumPy
- **Testing**: Pytest (8/8 automated test cases passing)

---

## 4. Key Features & Algorithms

### Multi-Checkpoint Readiness Verification
Calculates overall surgery readiness at $T-60m$, $T-30m$, $T-15m$, and $T-0m$ using weighted components:
- **Patient Readiness** (25%)
- **Staff Roster** (25%)
- **Equipment Status** (20%)
- **Sterile Supplies** (15%)
- **Theatre Availability** (15%)

### Safety-Critical Overrides
- **Patient Not Ready** (e.g. consent incomplete) $\implies$ Forces overall status to 🔴 **NOT READY** regardless of numerical score.
- **Faulty Equipment** $\implies$ Forces overall status to 🔴 **NOT READY**.
- **Missing Staff / NULL Status** $\implies$ Forces status to ⚪ **DATA INCOMPLETE** or 🔴 **NOT READY**.

### Data Quality & Confidence Engine
Calculates a `confidence_score` (0–100%). Detects missing fields, NULL values, unconfirmed statuses, and stale timestamps (>30-60 mins old).

### Interactive Failure Simulator
Supports 6 live test triggers:
1. `Simulate Staff Missing` (Anaesthetist status set to NULL)
2. `Simulate Equipment Failure` (READY $\rightarrow$ FAULTY)
3. `Simulate Patient Not Ready` (Consent form incomplete)
4. `Simulate Supply Missing` (CSSD pack missing)
5. `Simulate Surgery Overrun` (Prior session extended)
6. `Simulate Emergency Preemption` (Trauma case preempts OT)

---

## 5. Empirical Baseline vs Prototype Experiment

Programmatically evaluated over **320 synthetic operating sessions**:

| Performance Metric | Baseline (T-0m Manual) | ORRS Prototype Engine | Improvement |
| :--- | :--- | :--- | :--- |
| **Average Avoidable Idle Minutes** | **6.83 mins** | **1.64 mins** | **-75.98%** |
| **Avoidable Idle Time Reduction** | Baseline | **75.98%** | **Target $\ge 25\%$ PASSED** |
| **Early Delay Detection Rate** | 0.0% | **100.0%** | **Target $\ge 70\%$ PASSED** |
| **Automated Pytest Suite** | - | **8 / 8 Passed** | **100% PASS** |

---

## 6. How to Run the Project Locally

### Step 1: Install Dependencies & Run Backend API
```bash
# From workspace root:
pip install -r requirements.txt

# Seed database and start FastAPI server:
$env:PYTHONPATH="."
python scripts/generate_data.py
python scripts/seed_database.py
python -m uvicorn backend.main:app --reload --port 8000
```
Backend API will be live at: `http://127.0.0.1:8000`  
Swagger API documentation: `http://127.0.0.1:8000/docs`

### Step 2: Install & Run React Frontend
```bash
# Open a new terminal:
cd frontend
npm install
npm run dev
```
Frontend UI will be live at: `http://localhost:5173`

### Step 3: Run Automated Pytest Suite & Programmatic Experiment
```bash
# Run pytest:
$env:PYTHONPATH="."
python -m pytest tests/ -v

# Run experiment evaluation:
python scripts/run_experiment.py
```

---

## 7. Documentation Index

- [Architecture Diagram](file:///c:/Users/Asus/Desktop/project/docs/architecture.md)
- [Data Schema & Entity Specification](file:///c:/Users/Asus/Desktop/project/docs/data_schema.md)
- [Methodology & Readiness Algorithm](file:///c:/Users/Asus/Desktop/project/docs/methodology.md)
- [Risk Register](file:///c:/Users/Asus/Desktop/project/docs/risk_register.md)
- [User Guide for Coordinators & Admins](file:///c:/Users/Asus/Desktop/project/docs/user_guide.md)
- [Stakeholder Validation Document](file:///c:/Users/Asus/Desktop/project/docs/stakeholder_validation.md)
- [Product Discovery & Strategy](file:///c:/Users/Asus/Desktop/project/docs/product_discovery.md)
