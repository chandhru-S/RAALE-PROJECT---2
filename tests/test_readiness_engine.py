import pytest
from datetime import datetime
from backend.services.readiness_engine import evaluate_surgery_readiness

def test_complete_ready_surgery():
    schedule = {"surgery_id": "SURG_TEST_01", "scheduled_start": "2026-09-10 10:00:00", "previous_session_overrun": "No"}
    patient = {"consent_complete": True, "fasting_complete": True, "vitals_status": "NORMAL", "patient_ready": True, "last_updated": "2026-09-10 09:40:00"}
    staff = [
        {"role": "Surgeon", "availability_status": "AVAILABLE", "last_updated": "2026-09-10 09:45:00"},
        {"role": "Anaesthetist", "availability_status": "AVAILABLE", "last_updated": "2026-09-10 09:45:00"},
        {"role": "Nurse", "availability_status": "AVAILABLE", "last_updated": "2026-09-10 09:45:00"}
    ]
    equipment = [{"equipment_name": "Surgical Tower", "status": "READY", "last_updated": "2026-09-10 09:30:00"}]
    supplies = {"status": "AVAILABLE", "sterility_confirmed": True, "last_updated": "2026-09-10 09:30:00"}

    res = evaluate_surgery_readiness(schedule, patient, staff, equipment, supplies, checkpoint="T-30m")
    assert res["overall_status"] == "READY"
    assert res["readiness_score"] >= 85.0
    assert res["confidence_score"] >= 80.0
