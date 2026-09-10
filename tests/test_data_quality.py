from datetime import datetime, timedelta
from backend.services.uncertainty_engine import calculate_confidence_score

def test_stale_timestamp_confidence_reduction():
    checkpoint_time = datetime(2026, 9, 10, 10, 0, 0)
    stale_time = checkpoint_time - timedelta(hours=2) # 2 hours old

    patient = {"consent_complete": True, "fasting_complete": True, "vitals_status": "NORMAL", "last_updated": stale_time}
    staff = [{"role": "Surgeon", "availability_status": "AVAILABLE", "last_updated": stale_time}]
    equipment = [{"equipment_name": "OT Workstation", "status": "READY", "last_updated": stale_time}]
    supplies = {"status": "AVAILABLE", "sterility_confirmed": True}

    res = calculate_confidence_score(patient, staff, equipment, supplies, checkpoint_time)
    assert res["confidence_score"] < 90.0
    assert any("stale" in issue.lower() for issue in res["data_quality_issues"])
