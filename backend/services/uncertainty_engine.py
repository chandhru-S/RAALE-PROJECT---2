from datetime import datetime, timedelta
from typing import Dict, Any, List

def calculate_confidence_score(
    patient_data: Dict[str, Any],
    staff_data: List[Dict[str, Any]],
    equipment_data: List[Dict[str, Any]],
    supply_data: Dict[str, Any],
    checkpoint_time: datetime
) -> Dict[str, Any]:
    """
    Evaluates data quality, completeness, and freshness to calculate confidence score (0-100).
    """
    total_checks = 0
    passed_checks = 0
    data_quality_issues = []

    # 1. Patient Data Completeness & Freshness
    total_checks += 3
    if patient_data:
        if patient_data.get("consent_complete") is not None and patient_data.get("fasting_complete") is not None:
            passed_checks += 1
        else:
            data_quality_issues.append("Patient preparation checklist fields missing")
            
        if patient_data.get("vitals_status") and patient_data.get("vitals_status") != "UNKNOWN":
            passed_checks += 1
        else:
            data_quality_issues.append("Patient vitals status unknown or unrecorded")

        last_upd = patient_data.get("last_updated")
        if last_upd:
            if isinstance(last_upd, str):
                last_upd = datetime.strptime(last_upd, "%Y-%m-%d %H:%M:%S")
            if (checkpoint_time - last_upd).total_seconds() <= 3600:
                passed_checks += 1
            else:
                data_quality_issues.append("Patient readiness record is stale (>60 mins old)")
        else:
            data_quality_issues.append("Patient record timestamp missing")

    # 2. Staff Data Completeness & Freshness
    total_checks += 6
    if staff_data:
        roles_found = {s.get("role") for s in staff_data}
        if "Surgeon" in roles_found and "Anaesthetist" in roles_found:
            passed_checks += 1
        else:
            data_quality_issues.append("Roster missing required Surgeon or Anaesthetist assignment")

        null_staff_status = any(s.get("availability_status") is None or str(s.get("availability_status")).upper() in ["NULL", "NONE"] for s in staff_data)
        if not null_staff_status:
            passed_checks += 3  # Penalty for NULL staff status
        else:
            data_quality_issues.append("Staff availability status has NULL/unconfirmed entries")

        stale_staff = False
        for s in staff_data:
            l_upd = s.get("last_updated")
            if l_upd:
                if isinstance(l_upd, str):
                    l_upd = datetime.strptime(l_upd, "%Y-%m-%d %H:%M:%S")
                if (checkpoint_time - l_upd).total_seconds() > 3600:
                    stale_staff = True
                    break
        if not stale_staff:
            passed_checks += 2
        else:
            data_quality_issues.append("Staff roster update timestamp is stale (>60 mins old)")
    else:
        data_quality_issues.append("No staff roster records found for surgery")

    # 3. Equipment Data Completeness & Freshness
    total_checks += 3
    if equipment_data:
        unknown_eq = any(eq.get("status") in [None, "UNKNOWN"] for eq in equipment_data)
        if not unknown_eq:
            passed_checks += 1
        else:
            data_quality_issues.append("Equipment status recorded as UNKNOWN or NULL")

        faulty_eq = any(eq.get("status") == "FAULTY" for eq in equipment_data)
        if not faulty_eq:
            passed_checks += 1
        else:
            data_quality_issues.append("Equipment defect logged")

        stale_eq = False
        for eq in equipment_data:
            l_upd = eq.get("last_updated")
            if l_upd:
                if isinstance(l_upd, str):
                    l_upd = datetime.strptime(l_upd, "%Y-%m-%d %H:%M:%S")
                if (checkpoint_time - l_upd).total_seconds() > 3600:
                    stale_eq = True
                    break
        if not stale_eq:
            passed_checks += 1
        else:
            data_quality_issues.append("Equipment status timestamp is stale (>60 mins old)")
    else:
        data_quality_issues.append("No equipment records assigned to theatre")

    # 4. Supply Data Completeness
    total_checks += 2
    if supply_data:
        if supply_data.get("status") in ["AVAILABLE", "PARTIAL", "STERILITY_PENDING", "MISSING"]:
            passed_checks += 1
        else:
            data_quality_issues.append("Sterile supply status field invalid or missing")

        if supply_data.get("sterility_confirmed") is not None:
            passed_checks += 1
        else:
            data_quality_issues.append("Sterility confirmation state missing")
    else:
        data_quality_issues.append("Sterile supply record missing")

    confidence_pct = round((passed_checks / max(total_checks, 1)) * 100.0, 1)

    if confidence_pct >= 90:
        level = "HIGH"
    elif confidence_pct >= 70:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "confidence_score": confidence_pct,
        "confidence_level": level,
        "data_quality_issues": data_quality_issues
    }
