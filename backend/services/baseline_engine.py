from typing import Dict, Any, List, Optional

def evaluate_baseline_readiness(
    schedule: Dict[str, Any],
    patient_data: Optional[Dict[str, Any]],
    staff_data: List[Dict[str, Any]],
    equipment_data: List[Dict[str, Any]],
    supply_data: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Baseline Engine (Traditional / Manual approach):
    Checks readiness ONLY at the scheduled surgery start time (T-0m).
    No proactive early warnings or checkpoint tracking.
    """
    # 1. Patient check
    patient_ready = False
    if patient_data and patient_data.get("consent_complete") and patient_data.get("fasting_complete") and patient_data.get("vitals_status") == "NORMAL":
        patient_ready = True

    # 2. Staff check
    staff_ready = False
    surgeons = [s for s in staff_data if s.get("role") == "Surgeon" and s.get("availability_status") == "AVAILABLE"]
    anaesthetists = [s for s in staff_data if s.get("role") == "Anaesthetist" and s.get("availability_status") == "AVAILABLE"]
    if surgeons and anaesthetists:
        staff_ready = True

    # 3. Equipment check
    equipment_ready = True
    if equipment_data:
        faulty_or_maint = any(eq.get("status") in ["FAULTY", "MAINTENANCE", "UNKNOWN"] for eq in equipment_data)
        if faulty_or_maint:
            equipment_ready = False

    # 4. Supplies check
    supplies_ready = False
    if supply_data and supply_data.get("status") == "AVAILABLE" and supply_data.get("sterility_confirmed"):
        supplies_ready = True

    # Baseline logic
    surgery_can_start = (patient_ready and staff_ready and equipment_ready and supplies_ready)

    return {
        "surgery_id": schedule.get("surgery_id"),
        "surgery_can_start": surgery_can_start,
        "is_delayed": not surgery_can_start,
        "checked_at": "T-0m (Scheduled Start)"
    }
