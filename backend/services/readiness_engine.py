from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from backend.services.uncertainty_engine import calculate_confidence_score

def evaluate_surgery_readiness(
    schedule: Dict[str, Any],
    patient_data: Optional[Dict[str, Any]],
    staff_data: List[Dict[str, Any]],
    equipment_data: List[Dict[str, Any]],
    supply_data: Optional[Dict[str, Any]],
    checkpoint: str = "T-30m"
) -> Dict[str, Any]:
    """
    Evaluates complete readiness for an operating room session across 5 components.
    Applies safety overrides and confidence scoring.
    """
    blocking_issues = []
    recommended_actions = []

    # Parse scheduled start time
    sched_start = schedule.get("scheduled_start")
    if isinstance(sched_start, str):
        sched_start = datetime.strptime(sched_start, "%Y-%m-%d %H:%M:%S")

    # Set checkpoint evaluation timestamp
    checkpoint_offsets = {"T-60m": 60, "T-30m": 30, "T-15m": 15, "T-0m": 0}
    offset = checkpoint_offsets.get(checkpoint, 30)
    eval_time = sched_start - timedelta(minutes=offset)

    # 1. Patient Score (Weight: 25%)
    patient_score = 0.0
    patient_critical_pass = True
    if patient_data:
        if patient_data.get("consent_complete"):
            patient_score += 40.0
        else:
            patient_critical_pass = False
            blocking_issues.append("Patient surgical consent is incomplete")
            recommended_actions.append("Obtain signed consent form from surgical team/patient")

        if patient_data.get("fasting_complete"):
            patient_score += 35.0
        else:
            patient_critical_pass = False
            blocking_issues.append("Patient fasting protocol not met")
            recommended_actions.append("Verify last oral intake; consult anaesthetist for delay requirement")

        if patient_data.get("vitals_status") == "NORMAL":
            patient_score += 25.0
        else:
            blocking_issues.append(f"Patient vitals abnormal: {patient_data.get('vitals_status')}")
            recommended_actions.append("Re-evaluate patient vital signs with attending nurse")

        if not patient_data.get("patient_ready", True):
            patient_critical_pass = False
    else:
        patient_critical_pass = False
        blocking_issues.append("Patient readiness record missing")
        recommended_actions.append("Complete pre-operative assessment form for patient")

    # 2. Staff Score (Weight: 25%)
    staff_score = 0.0
    staff_critical_pass = True
    surgeons = [s for s in staff_data if s.get("role") == "Surgeon"]
    anaesthetists = [s for s in staff_data if s.get("role") == "Anaesthetist"]
    nurses = [s for s in staff_data if s.get("role") == "Nurse"]

    # Surgeon check
    if surgeons and surgeons[0].get("availability_status") == "AVAILABLE":
        staff_score += 40.0
    elif surgeons and surgeons[0].get("availability_status") in [None, "NULL"]:
        staff_critical_pass = False
        blocking_issues.append("Surgeon availability status is NULL / unconfirmed")
        recommended_actions.append("Contact Lead Surgeon to confirm availability for session")
    else:
        staff_critical_pass = False
        status_text = surgeons[0].get("availability_status") if surgeons else "UNASSIGNED"
        blocking_issues.append(f"Surgeon unavailable ({status_text})")
        recommended_actions.append("Assign on-call backup surgeon or reschedule start time")

    # Anaesthetist check
    if anaesthetists and anaesthetists[0].get("availability_status") == "AVAILABLE":
        staff_score += 40.0
    elif anaesthetists and anaesthetists[0].get("availability_status") in [None, "NULL"]:
        staff_critical_pass = False
        blocking_issues.append("Anaesthetist availability status is NULL / unconfirmed")
        recommended_actions.append("Contact Anaesthesia Department to confirm assignment")
    else:
        staff_critical_pass = False
        status_text = anaesthetists[0].get("availability_status") if anaesthetists else "UNASSIGNED"
        blocking_issues.append(f"Anaesthetist unavailable ({status_text})")
        recommended_actions.append("Request immediate allocation of backup Anaesthetist")

    # Nurse check
    if nurses and nurses[0].get("availability_status") == "AVAILABLE":
        staff_score += 20.0
    else:
        staff_score += 5.0
        blocking_issues.append("Scrub / Circulating Nurse assignment pending")
        recommended_actions.append("Dispatch nursing staff to assigned theatre")

    # 3. Equipment Score (Weight: 20%)
    equipment_score = 100.0
    eq_critical_pass = True
    if equipment_data:
        for eq in equipment_data:
            st = eq.get("status", "READY")
            if st == "FAULTY":
                equipment_score = 0.0
                eq_critical_pass = False
                blocking_issues.append(f"Equipment faulty: {eq.get('equipment_name')}")
                recommended_actions.append(f"Deploy backup {eq.get('equipment_name')} from equipment store")
                break
            elif st in ["MAINTENANCE", "UNKNOWN"]:
                equipment_score = min(equipment_score, 40.0)
                blocking_issues.append(f"Equipment {eq.get('equipment_name')} status: {st}")
                recommended_actions.append(f"Verify biomedical engineering clearance for {eq.get('equipment_name')}")
    else:
        equipment_score = 50.0
        blocking_issues.append("No equipment checks logged for OT")

    # 4. Sterile Supply Score (Weight: 15%)
    supply_score = 0.0
    supply_critical_pass = True
    if supply_data:
        st = supply_data.get("status", "AVAILABLE")
        if st == "AVAILABLE" and supply_data.get("sterility_confirmed"):
            supply_score = 100.0
        elif st == "PARTIAL":
            supply_score = 50.0
            blocking_issues.append("Surgical supply pack incomplete")
            recommended_actions.append("Request immediate restock of missing surgical trays from CSSD")
        elif st == "STERILITY_PENDING":
            supply_score = 30.0
            blocking_issues.append("Sterile supply autoclave confirmation pending")
            recommended_actions.append("Check CSSD sterilization batch completion timestamp")
        else: # MISSING
            supply_score = 0.0
            supply_critical_pass = False
            blocking_issues.append("Required sterile surgical supply pack MISSING")
            recommended_actions.append("Expedite emergency sterilization pack from central supply")
    else:
        supply_score = 40.0
        blocking_issues.append("Sterile supply checklist missing")

    # 5. Theatre Availability Score (Weight: 15%)
    theatre_score = 100.0
    if schedule.get("previous_session_overrun") == "Yes":
        theatre_score = 40.0
        blocking_issues.append("Previous surgical session in OT overrun scheduled time")
        recommended_actions.append("Notify OT turnover team for rapid cleaning upon session end")

    # Calculate Weighted Total Score
    total_readiness_score = round(
        (0.25 * patient_score) +
        (0.25 * staff_score) +
        (0.20 * equipment_score) +
        (0.15 * supply_score) +
        (0.15 * theatre_score),
        1
    )

    # Uncertainty / Confidence Calculation
    uncertainty_res = calculate_confidence_score(
        patient_data=patient_data or {},
        staff_data=staff_data or [],
        equipment_data=equipment_data or [],
        supply_data=supply_data or {},
        checkpoint_time=eval_time
    )
    confidence_score = uncertainty_res["confidence_score"]
    blocking_issues.extend(uncertainty_res["data_quality_issues"])

    # Determine Overall Status Rules
    # GREY: Data incomplete or confidence < 60%
    if confidence_score < 60.0 or any("NULL" in issue or "missing" in issue.lower() for issue in uncertainty_res["data_quality_issues"]):
        overall_status = "DATA_INCOMPLETE"
    # RED: Safety critical overrides (Patient not ready, Equipment faulty, Critical staff missing)
    elif not patient_critical_pass or not eq_critical_pass or not staff_critical_pass or total_readiness_score < 50.0:
        overall_status = "NOT_READY"
    # YELLOW: At risk if minor issues or score between 50 and 84
    elif total_readiness_score < 85.0 or len(blocking_issues) > 0:
        overall_status = "AT_RISK"
    # GREEN: Ready
    else:
        overall_status = "READY"

    # Deduplicate issues and actions
    unique_issues = list(dict.fromkeys(blocking_issues))
    unique_actions = list(dict.fromkeys(recommended_actions))

    return {
        "surgery_id": schedule.get("surgery_id"),
        "checkpoint": checkpoint,
        "overall_status": overall_status,
        "readiness_score": total_readiness_score,
        "confidence_score": confidence_score,
        "patient_score": patient_score,
        "staff_score": staff_score,
        "equipment_score": equipment_score,
        "supply_score": supply_score,
        "theatre_score": theatre_score,
        "blocking_issues": "; ".join(unique_issues) if unique_issues else "None",
        "recommended_actions": "; ".join(unique_actions) if unique_actions else "Proceed with scheduled procedure",
        "assessed_at": eval_time
    }
