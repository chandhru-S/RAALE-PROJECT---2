#!/usr/bin/env python3
"""
Run Baseline Evaluation script.
Calculates traditional start-time baseline metrics.
"""

from backend.database import SessionLocal
from backend.models import TheatreSchedule, DelayReason
from backend.services.baseline_engine import evaluate_baseline_readiness

def main():
    db = SessionLocal()
    try:
        schedules = db.query(TheatreSchedule).all()
        print(f"Evaluating traditional T-0m Baseline on {len(schedules)} operating sessions...")

        total_idle_mins = 0
        delayed_count = 0

        for sched in schedules:
            delay = db.query(DelayReason).filter(DelayReason.surgery_id == sched.surgery_id).first()
            if delay and delay.avoidable:
                total_idle_mins += delay.delay_minutes
                delayed_count += 1

        avg_idle = total_idle_mins / max(len(schedules), 1)
        print("\n--- BASELINE METRICS ---")
        print(f"Total Operating Sessions : {len(schedules)}")
        print(f"Delayed Sessions (Avoidable): {delayed_count}")
        print(f"Total Avoidable Idle Mins: {total_idle_mins} mins")
        print(f"Average Idle Mins / Session: {avg_idle:.2f} mins")
    finally:
        db.close()

if __name__ == "__main__":
    main()
