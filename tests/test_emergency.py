from backend.services.readiness_engine import evaluate_surgery_readiness

def test_emergency_preemption():
    schedule = {"surgery_id": "SURG_TEST_07", "scheduled_start": "2026-09-10 10:00:00", "previous_session_overrun": "Yes"}
    patient = {"consent_complete": True, "fasting_complete": True, "vitals_status": "NORMAL", "patient_ready": True, "last_updated": "2026-09-10 09:40:00"}
    staff = [
        {"role": "Surgeon", "availability_status": "AVAILABLE", "last_updated": "2026-09-10 09:45:00"},
        {"role": "Anaesthetist", "availability_status": "AVAILABLE", "last_updated": "2026-09-10 09:45:00"}
    ]
    equipment = [{"equipment_name": "OT Table", "status": "READY", "last_updated": "2026-09-10 09:30:00"}]
    supplies = {"status": "AVAILABLE", "sterility_confirmed": True, "last_updated": "2026-09-10 09:30:00"}

    res = evaluate_surgery_readiness(schedule, patient, staff, equipment, supplies, checkpoint="T-30m")
    assert res["overall_status"] == "AT_RISK"
