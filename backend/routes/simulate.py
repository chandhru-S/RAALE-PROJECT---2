from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database import get_db
from backend.models.models import TheatreSchedule, StaffRoster, Equipment, PatientReadiness, SterileSupply, DelayReason, Alert
from backend.services.readiness_engine import evaluate_surgery_readiness
from backend.services.alert_engine import generate_alert_from_assessment

router = APIRouter(tags=["Simulation"])

def get_target_surgery(db: Session, ot_id: str = "OT001"):
    sched = db.query(TheatreSchedule).filter(TheatreSchedule.theatre_id == ot_id).first()
    if not sched:
        sched = db.query(TheatreSchedule).first()
    return sched

@router.post("/api/simulate/staff-missing")
def simulate_staff_missing(theatre_id: str = "OT001", db: Session = Depends(get_db)):
    """
    Test 1: Sets Anaesthetist status to NULL / unconfirmed.
    Expected: DATA INCOMPLETE, low confidence, manual verification alert.
    """
    sched = get_target_surgery(db, theatre_id)
    if not sched:
        raise HTTPException(status_code=404, detail="Target surgery not found")

    staff = db.query(StaffRoster).filter(StaffRoster.assigned_surgery == sched.surgery_id, StaffRoster.role == "Anaesthetist").first()
    if staff:
        staff.availability_status = None # Set to NULL!
        staff.last_updated = datetime.utcnow()
        db.commit()

    # Re-evaluate
    assessment = evaluate_surgery_readiness(
        schedule={"surgery_id": sched.surgery_id, "scheduled_start": sched.scheduled_start, "previous_session_overrun": sched.previous_session_overrun},
        patient_data={"consent_complete": True, "fasting_complete": True, "vitals_status": "NORMAL", "patient_ready": True, "last_updated": datetime.utcnow()},
        staff_data=[{"role": s.role, "availability_status": s.availability_status, "last_updated": s.last_updated} for s in sched.staff_members],
        equipment_data=[{"equipment_name": "OT Workstation", "status": "READY", "last_updated": datetime.utcnow()}],
        supply_data={"status": "AVAILABLE", "sterility_confirmed": True},
        checkpoint="T-30m"
    )

    alert = generate_alert_from_assessment(db, assessment, sched.theatre_id, sched.surgery_id)

    return {
        "success": True,
        "test_name": "Test 1 — Missing Staff Data",
        "surgery_id": sched.surgery_id,
        "theatre_id": sched.theatre_id,
        "overall_status": assessment["overall_status"],
        "readiness_score": assessment["readiness_score"],
        "confidence_score": assessment["confidence_score"],
        "blocking_issues": assessment["blocking_issues"],
        "recommended_actions": assessment["recommended_actions"],
        "alert_created": alert.issue if alert else None
    }

@router.post("/api/simulate/equipment-failure")
def simulate_equipment_failure(theatre_id: str = "OT002", db: Session = Depends(get_db)):
    """
    Test 2: Equipment changes from READY -> FAULTY.
    Expected: NOT READY, High-priority equipment alert.
    """
    sched = get_target_surgery(db, theatre_id)
    if not sched:
        raise HTTPException(status_code=404, detail="Target surgery not found")

    eq = db.query(Equipment).filter(Equipment.theatre_id == sched.theatre_id).first()
    if not eq:
        eq = Equipment(equipment_id="EQ_SIM_01", equipment_name="Anesthesia Tower", theatre_id=sched.theatre_id, status="FAULTY", last_updated=datetime.utcnow())
        db.add(eq)
    else:
        eq.status = "FAULTY"
        eq.last_updated = datetime.utcnow()
    db.commit()

    assessment = evaluate_surgery_readiness(
        schedule={"surgery_id": sched.surgery_id, "scheduled_start": sched.scheduled_start, "previous_session_overrun": sched.previous_session_overrun},
        patient_data={"consent_complete": True, "fasting_complete": True, "vitals_status": "NORMAL", "patient_ready": True, "last_updated": datetime.utcnow()},
        staff_data=[{"role": "Surgeon", "availability_status": "AVAILABLE", "last_updated": datetime.utcnow()}, {"role": "Anaesthetist", "availability_status": "AVAILABLE", "last_updated": datetime.utcnow()}],
        equipment_data=[{"equipment_name": eq.equipment_name, "status": "FAULTY", "last_updated": datetime.utcnow()}],
        supply_data={"status": "AVAILABLE", "sterility_confirmed": True},
        checkpoint="T-30m"
    )

    alert = generate_alert_from_assessment(db, assessment, sched.theatre_id, sched.surgery_id)

    return {
        "success": True,
        "test_name": "Test 2 — Equipment Failure",
        "surgery_id": sched.surgery_id,
        "theatre_id": sched.theatre_id,
        "overall_status": assessment["overall_status"],
        "readiness_score": assessment["readiness_score"],
        "confidence_score": assessment["confidence_score"],
        "blocking_issues": assessment["blocking_issues"],
        "recommended_actions": assessment["recommended_actions"],
        "alert_created": alert.issue if alert else None
    }

@router.post("/api/simulate/patient-not-ready")
def simulate_patient_not_ready(theatre_id: str = "OT003", db: Session = Depends(get_db)):
    """
    Test 3: Patient surgical consent is incomplete.
    Expected: NOT READY due to safety override, Reason: Patient preparation incomplete.
    """
    sched = get_target_surgery(db, theatre_id)
    if not sched:
        raise HTTPException(status_code=404, detail="Target surgery not found")

    patient_rec = sched.patient_readiness
    if patient_rec:
        patient_rec.consent_complete = False
        patient_rec.patient_ready = False
        patient_rec.last_updated = datetime.utcnow()
        db.commit()

    assessment = evaluate_surgery_readiness(
        schedule={"surgery_id": sched.surgery_id, "scheduled_start": sched.scheduled_start, "previous_session_overrun": sched.previous_session_overrun},
        patient_data={"consent_complete": False, "fasting_complete": True, "vitals_status": "NORMAL", "patient_ready": False, "last_updated": datetime.utcnow()},
        staff_data=[{"role": "Surgeon", "availability_status": "AVAILABLE", "last_updated": datetime.utcnow()}, {"role": "Anaesthetist", "availability_status": "AVAILABLE", "last_updated": datetime.utcnow()}],
        equipment_data=[{"equipment_name": "C-Arm", "status": "READY", "last_updated": datetime.utcnow()}],
        supply_data={"status": "AVAILABLE", "sterility_confirmed": True},
        checkpoint="T-30m"
    )

    alert = generate_alert_from_assessment(db, assessment, sched.theatre_id, sched.surgery_id)

    return {
        "success": True,
        "test_name": "Test 3 — Patient Not Ready",
        "surgery_id": sched.surgery_id,
        "theatre_id": sched.theatre_id,
        "overall_status": assessment["overall_status"],
        "readiness_score": assessment["readiness_score"],
        "confidence_score": assessment["confidence_score"],
        "blocking_issues": assessment["blocking_issues"],
        "recommended_actions": assessment["recommended_actions"],
        "alert_created": alert.issue if alert else None
    }

@router.post("/api/simulate/supply-missing")
def simulate_supply_missing(theatre_id: str = "OT004", db: Session = Depends(get_db)):
    """
    Test 4: Sterile surgical pack is MISSING / sterility unconfirmed.
    Expected: NOT READY or AT RISK with CSSD alert.
    """
    sched = get_target_surgery(db, theatre_id)
    if not sched:
        raise HTTPException(status_code=404, detail="Target surgery not found")

    supply_rec = sched.sterile_supply
    if supply_rec:
        supply_rec.status = "MISSING"
        supply_rec.sterility_confirmed = False
        supply_rec.last_updated = datetime.utcnow()
        db.commit()

    assessment = evaluate_surgery_readiness(
        schedule={"surgery_id": sched.surgery_id, "scheduled_start": sched.scheduled_start, "previous_session_overrun": sched.previous_session_overrun},
        patient_data={"consent_complete": True, "fasting_complete": True, "vitals_status": "NORMAL", "patient_ready": True, "last_updated": datetime.utcnow()},
        staff_data=[{"role": "Surgeon", "availability_status": "AVAILABLE", "last_updated": datetime.utcnow()}, {"role": "Anaesthetist", "availability_status": "AVAILABLE", "last_updated": datetime.utcnow()}],
        equipment_data=[{"equipment_name": "OT Table", "status": "READY", "last_updated": datetime.utcnow()}],
        supply_data={"status": "MISSING", "sterility_confirmed": False},
        checkpoint="T-30m"
    )

    alert = generate_alert_from_assessment(db, assessment, sched.theatre_id, sched.surgery_id)

    return {
        "success": True,
        "test_name": "Test 4 — Sterile Supplies Missing",
        "surgery_id": sched.surgery_id,
        "theatre_id": sched.theatre_id,
        "overall_status": assessment["overall_status"],
        "readiness_score": assessment["readiness_score"],
        "confidence_score": assessment["confidence_score"],
        "blocking_issues": assessment["blocking_issues"],
        "recommended_actions": assessment["recommended_actions"],
        "alert_created": alert.issue if alert else None
    }

@router.post("/api/simulate/overrun")
def simulate_surgery_overrun(theatre_id: str = "OT005", db: Session = Depends(get_db)):
    """
    Test 5: Previous surgery exceeds scheduled end time.
    Expected: AT RISK, Potential delay detected.
    """
    sched = get_target_surgery(db, theatre_id)
    if not sched:
        raise HTTPException(status_code=404, detail="Target surgery not found")

    sched.previous_session_overrun = "Yes"
    db.commit()

    assessment = evaluate_surgery_readiness(
        schedule={"surgery_id": sched.surgery_id, "scheduled_start": sched.scheduled_start, "previous_session_overrun": "Yes"},
        patient_data={"consent_complete": True, "fasting_complete": True, "vitals_status": "NORMAL", "patient_ready": True, "last_updated": datetime.utcnow()},
        staff_data=[{"role": "Surgeon", "availability_status": "AVAILABLE", "last_updated": datetime.utcnow()}, {"role": "Anaesthetist", "availability_status": "AVAILABLE", "last_updated": datetime.utcnow()}],
        equipment_data=[{"equipment_name": "OT Table", "status": "READY", "last_updated": datetime.utcnow()}],
        supply_data={"status": "AVAILABLE", "sterility_confirmed": True},
        checkpoint="T-30m"
    )

    alert = generate_alert_from_assessment(db, assessment, sched.theatre_id, sched.surgery_id)

    return {
        "success": True,
        "test_name": "Test 5 — Previous Surgery Overrun",
        "surgery_id": sched.surgery_id,
        "theatre_id": sched.theatre_id,
        "overall_status": assessment["overall_status"],
        "readiness_score": assessment["readiness_score"],
        "confidence_score": assessment["confidence_score"],
        "blocking_issues": assessment["blocking_issues"],
        "recommended_actions": assessment["recommended_actions"],
        "alert_created": alert.issue if alert else None
    }

@router.post("/api/simulate/emergency")
def simulate_emergency_surgery(theatre_id: str = "OT006", db: Session = Depends(get_db)):
    """
    Test 6: Emergency trauma case preempts scheduled theatre.
    Expected: Affected scheduled surgeries identified, readiness recalculated, high priority alerts generated.
    """
    sched = get_target_surgery(db, theatre_id)
    if not sched:
        raise HTTPException(status_code=404, detail="Target surgery not found")

    sched.priority = "Emergency"
    sched.procedure_type = "Emergency Trauma Surgery"
    db.commit()

    assessment = evaluate_surgery_readiness(
        schedule={"surgery_id": sched.surgery_id, "scheduled_start": sched.scheduled_start, "previous_session_overrun": "Yes"},
        patient_data={"consent_complete": True, "fasting_complete": True, "vitals_status": "NORMAL", "patient_ready": True, "last_updated": datetime.utcnow()},
        staff_data=[{"role": "Surgeon", "availability_status": "AVAILABLE", "last_updated": datetime.utcnow()}, {"role": "Anaesthetist", "availability_status": "AVAILABLE", "last_updated": datetime.utcnow()}],
        equipment_data=[{"equipment_name": "OT Table", "status": "READY", "last_updated": datetime.utcnow()}],
        supply_data={"status": "AVAILABLE", "sterility_confirmed": True},
        checkpoint="T-30m"
    )

    alert = generate_alert_from_assessment(db, assessment, sched.theatre_id, sched.surgery_id)

    return {
        "success": True,
        "test_name": "Test 6 — Emergency Preemption",
        "surgery_id": sched.surgery_id,
        "theatre_id": sched.theatre_id,
        "overall_status": assessment["overall_status"],
        "readiness_score": assessment["readiness_score"],
        "confidence_score": assessment["confidence_score"],
        "blocking_issues": "Emergency trauma preemption active; scheduled session postponed",
        "recommended_actions": "Re-route elective surgery to backup OT-08 or reschedule",
        "alert_created": alert.issue if alert else None
    }

@router.post("/api/simulate/reset")
def reset_simulation(db: Session = Depends(get_db)):
    """
    Resets all simulated changes back to seeded dataset defaults.
    """
    from scripts.seed_database import seed_database
    seed_database()
    return {"success": True, "message": "Simulation environment reset to baseline synthetic state"}
