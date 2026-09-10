# Risk Register — Operating Room Readiness Synchroniser (ORRS)

| Risk | Probability | Impact | Risk Score | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Missing Data** | Medium | High | High | Confidence score algorithm flags incomplete records and sets status to `DATA_INCOMPLETE`. |
| **Stale Data** | Medium | High | High | Timestamp validation penalises records older than 30–60 minutes relative to checkpoint. |
| **False Alerts** | Medium | Medium | Medium | Threshold tuning for readiness scores and distinction between `AT_RISK` and `NOT_READY`. |
| **Staff Roster Incorrect** | Medium | High | High | Staff availability status requires explicit verification and supports inline manual override. |
| **Equipment Status Incorrect** | Medium | High | High | Equipment status freshness checks and bio-medical clearance verification workflows. |
| **Emergency Surgery Preemption** | High | High | Critical | Dynamic schedule recalculation and automated preemption alerts across affected theatres. |
| **Data Privacy Violations** | Low | Critical | Critical | Strict enforcement of 100% synthetic, de-identified data generation (`PAT001`, `SURG001`). |
