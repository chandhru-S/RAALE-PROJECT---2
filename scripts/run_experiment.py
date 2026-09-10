#!/usr/bin/env python3
"""
Run Full Experiment script.
Executes baseline vs prototype experiment and generates CSV/Markdown reports.
"""

from backend.database import SessionLocal
from backend.services.experiment_engine import run_experiment

def main():
    print("Running ORRS Empirical Evaluation Experiment...")
    db = SessionLocal()
    try:
        results = run_experiment(db)
        print("\n==========================================")
        print("EXPERIMENT EVALUATION RESULTS")
        print("==========================================")
        print(f"Total Sessions Evaluated     : {results['total_sessions']}")
        print(f"Baseline Avg Idle Mins       : {results['baseline_avg_idle_mins']} mins")
        print(f"Prototype Avg Idle Mins      : {results['prototype_avg_idle_mins']} mins")
        print(f"Avoidable Idle Time Reduction: {results['idle_time_reduction_pct']}% (Target >= 25%)")
        print(f"Early Detection Rate         : {results['early_detection_rate']}% (Target >= 70%)")
        print(f"Alert Precision              : {results['alert_precision']}% (Target >= 80%)")
        print(f"False Positive Rate          : {results['false_positive_rate']}%")
        print(f"False Negative Rate          : {results['false_negative_rate']}%")
        print(f"Target Achieved              : {'[YES - TARGET PASSED]' if results['target_achieved'] else '[NO - TARGET FAILED]'}")
        print("==========================================")
        print("Reports generated in reports/experiment_results.csv and reports/experiment_report.md")
    finally:
        db.close()

if __name__ == "__main__":
    main()
