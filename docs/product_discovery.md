# Product Discovery Document — Operating Room Readiness Synchroniser (ORRS)

## 1. Problem Statement
Multi-specialty hospitals share expensive operating theatres across departments. Significant operational time is lost when interdependent resources (Patient, Surgeon, Anaesthetist, Nurses, Equipment, Sterile Supplies, and Theatre space) are not ready simultaneously at the scheduled surgery start time.

Traditional manual workflows evaluate readiness reactively at $T-0m$ (scheduled start time), leading to idle operating rooms, delayed surgeries, and reduced hospital throughput.

## 2. Target Users & Personas
- **OT Coordinator**: Requires a live command grid and early warnings ($T-60m$, $T-30m$) to resolve resource bottlenecks before surgery start times.
- **Surgeons & Anaesthetists**: Require transparent readiness status and clear root-cause explanations for delays.
- **Hospital Administrator**: Requires empirical metrics tracking avoidable idle theatre minutes, department performance, and system precision.

## 3. Product Decisions & Rationale
- **Rule-Based Readiness Engine over Pure ML**: In safety-critical hospital environments, operational rules must be 100% transparent, explainable, and auditable. Rules allow explicit safety overrides (`Patient NOT READY` forces overall status to `NOT READY`).
- **Uncertainty & Data Freshness Engine**: The system must not produce misleading high-readiness scores when data is missing or stale. Stale timestamps (>30-60m old) or NULL statuses degrade the `confidence_score` and flag the session as `DATA_INCOMPLETE`.
- **Multi-Checkpoint Evaluation ($T-60m, T-30m, T-15m, T-0m$)**: Allows proactive intervention, giving staff sufficient lead time to dispatch backup equipment or confirm consent.

## 4. Success Metrics
- **Primary Metric**: Reduction of Avoidable Idle Theatre Minutes per session by at least **25%** compared to traditional $T-0m$ manual baseline.
- **Early Delay Detection Rate**: $\ge 70\%$ of avoidable delays detected prior to scheduled start time.
- **Alert Signal Precision**: $\ge 80\%$ precision on high-priority actionable alerts.
