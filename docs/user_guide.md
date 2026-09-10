# User Guide — Operating Room Readiness Synchroniser (ORRS)

## 1. Operating Theatre Coordinator Walkthrough

### Step 1: Open Operating Room Readiness Dashboard
- Access the main dashboard to view the high-level operational KPIs (Total Theatres, Ready, At Risk, Not Ready, Data Incomplete, Avg Idle Minutes).
- Monitor the **Live Operating Theatre Grid** for color-coded status badges:
  - 🟢 **READY**: All critical resources confirmed.
  - 🟡 **AT RISK**: Potential delay detected (e.g. prior session overrun or partial supplies).
  - 🔴 **NOT READY**: Critical resource missing or patient consent incomplete.
  - ⚪ **DATA INCOMPLETE**: Missing or stale data; confidence score low.

### Step 2: Inspect Surgery Assessment Details
- Click on any theatre card or surgery row to open the **Surgery Detail Modal**.
- Review the 5 component score breakdowns (Patient, Staff, Equipment, Supplies, Theatre).
- Check **Blocking Operational Issues** and review the **Recommended Action Plan**.

### Step 3: Review & Acknowledge Operational Alerts
- Navigate to the **Alerts** page.
- Review active high-priority alerts with severity levels, root causes, and recommended actions.
- Click **Acknowledge Alert** once action has been initiated by OT staff.

### Step 4: Run Interactive Failure Simulations
- Navigate to the **Failure Simulator** page.
- Test system resilience by clicking any of the 6 scenario triggers (e.g., *Simulate Equipment Failure*, *Simulate Missing Staff*).
- Observe real-time status updates, alert generation, and actionable recommendations.

---

## 2. Administrator Walkthrough

### Step 1: Operational Analytics & Delay Breakdown
- Open the **Analytics** page to inspect Recharts visualizations:
  - Avoidable Idle Minutes: Baseline vs Prototype comparison.
  - Delay category distribution pie chart.
  - Department performance & on-time start rates.
  - Checkpoint readiness score progression timeline.
  - Data quality & stale timestamp frequency.

### Step 2: Evaluation & Experiment Matrix
- Access the **Evaluation Report** page to review empirical baseline comparison metrics across 300+ synthetic operating sessions.
- Verify target achievements (&ge;25% idle time reduction, &ge;70% early delay detection).
- Inspect the **Failure Test Suite Checklist** and **System Error Analysis Report**.
