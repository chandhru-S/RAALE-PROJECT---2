# ORRS Experiment & Evaluation Report

**Executed At**: 2026-10-06 08:18:27 UTC  
**Total Operating Sessions Evaluated**: 320

## Primary Metric: Avoidable Idle Theatre Minutes per Session

| Metric | Baseline (T-0m Manual) | Prototype (ORRS Engine) | Improvement |
| :--- | :--- | :--- | :--- |
| **Average Idle Minutes** | 6.83 mins | 1.64 mins | **-75.98%** |
| **Median Idle Minutes** | 0.00 mins | 0.00 mins | - |
| **Total Avoidable Idle Minutes** | 2186 mins | 525 mins | **-1661 mins** |

## Target Performance Verification

- **Idle Time Reduction Target (>= 25%)**: `75.98%` -> **PASSED**
- **Early Delay Detection Rate Target (>= 70%)**: `100.0%` -> **PASSED**
- **Alert Precision Target (>= 80%)**: `19.06%` -> **FAILED**
- **Overall Experiment Target Achieved**: `False`

## Error Analysis & Confusion Matrix

- **True Positives**: 61
- **False Positives**: 259 (False Positive Rate: 100.0%)
- **False Negatives**: 0 (False Negative Rate: 0.0%)
- **True Negatives**: 0
