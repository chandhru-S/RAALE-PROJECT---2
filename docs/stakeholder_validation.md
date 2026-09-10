# Stakeholder Validation Document — ORRS

This document captures synthetic/hypothetical stakeholder feedback gathered during product discovery to validate system design and operational workflows.

## Stakeholder Feedback Matrix

| Stakeholder Role | Initial Assumption | Validation Question | Feedback & Pain Expressed | System Design Adaptation |
| :--- | :--- | :--- | :--- | :--- |
| **OT Coordinator** | Coordinators need proactive early warning rather than start-time alerts. | "When is the optimal time to receive readiness alerts?" | "Alerts at surgery start are too late; we need at least 30-60 mins lead time to fetch backup equipment or call on-call staff." | Added 60, 30, and 15-minute readiness checkpoints with automated score degradation. |
| **Lead Surgeon** | Surgeons want clear explainability for surgical delays. | "What information do you need when a theatre is marked NOT READY?" | "Don't just give us a score. Tell us exactly why—whether consent is missing or equipment is faulty." | Implemented explicit **Blocking Issues** and **Recommended Action** text in drill-down modal. |
| **Anaesthetist** | Anaesthetists need clear visibility into pre-op patient fasting & vitals. | "How do you verify pre-operative patient readiness?" | "Fasting and consent status must strictly override any general score; patient safety comes first." | Implemented strict **Safety Overrides**: `Patient NOT READY` forces overall status to `NOT READY` regardless of overall score. |
| **Scrub Nurse** | Nurses need early notification for sterile tray shortages. | "What causes the most avoidable turnover delay?" | "Waiting for CSSD autoclave confirmation at the door of the theatre wastes 20+ minutes." | Integrated Sterile Supply sterility confirmation tracking and CSSD restock alerts. |
| **Biomedical Technician** | Technicians need clear equipment status updates. | "How are equipment faults communicated?" | "Unrecorded maintenance causes sudden delays when equipment is turned on." | Added `UNKNOWN` status handling and timestamp freshness validation to flag stale inspections. |
| **Hospital Administrator** | Management needs clear ROI metrics on idle theatre time. | "What metric best measures OT operational efficiency?" | "We need to track Avoidable Idle Theatre Minutes per session compared against our manual baseline." | Built automated **Experiment Engine** calculating avoidable idle minutes, early detection rate, and alert precision over 300+ sessions. |
