from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.database import get_db
from backend.models.models import TheatreSchedule, Equipment
from backend.services.readiness_engine import evaluate_surgery_readiness

router = APIRouter(tags=["Readiness"])

@router.get("/api/readiness")
def get_all_readiness_assessments(
    checkpoint: str = Query("T-30m", description="Checkpoint: T-60m, T-30m, T-15m, T-0m"),
    db: Session = Depends(get_db)
):
    """
    Evaluates readiness across all scheduled surgeries for a given checkpoint.
    """
    schedules = db.query(TheatreSchedule).all()
    results = []

    for sched in schedules:
        patient_rec = sched.patient_readiness
        patient_dict = {
            "consent_complete": patient_rec.consent_complete if patient_rec else False,
            "fasting_complete": patient_rec.fasting_complete if patient_rec else False,
            "vitals_status": patient_rec.vitals_status if patient_rec else "NORMAL",
            "patient_ready": patient_rec.patient_ready if patient_rec else False,
            "last_updated": patient_rec.last_updated if patient_rec else sched.scheduled_start
        } if patient_rec else None

        staff_list = [{
            "role": s.role,
            "availability_status": s.availability_status,
            "last_updated": s.last_updated
        } for s in sched.staff_members]

        eq_rec = db.query(Equipment).filter(Equipment.theatre_id == sched.theatre_id).all()
        eq_list = [{
            "equipment_name": eq.equipment_name,
            "status": eq.status,
            "last_updated": eq.last_updated
        } for eq in eq_rec] if eq_rec else [{
            "equipment_name": "OT Primary Equipment",
            "status": "READY",
            "last_updated": sched.scheduled_start
        }]

        sup_dict = {
            "status": sched.sterile_supply.status if sched.sterile_supply else "AVAILABLE",
            "sterility_confirmed": sched.sterile_supply.sterility_confirmed if sched.sterile_supply else True
        } if sched.sterile_supply else None

        assessment = evaluate_surgery_readiness(
            schedule={
                "surgery_id": sched.surgery_id,
                "scheduled_start": sched.scheduled_start,
                "previous_session_overrun": sched.previous_session_overrun
            },
            patient_data=patient_dict,
            staff_data=staff_list,
            equipment_data=eq_list,
            supply_data=sup_dict,
            checkpoint=checkpoint
        )

        # Attach metadata for table view
        assessment["theatre_id"] = sched.theatre_id
        assessment["department"] = sched.department
        assessment["procedure"] = sched.procedure_type
        assessment["patient_status"] = "READY" if (patient_rec and patient_rec.patient_ready) else "NOT_READY"
        assessment["staff_status"] = "READY" if (staff_list and all(s["availability_status"] == "AVAILABLE" for s in staff_list)) else "AT_RISK"
        assessment["equipment_status"] = "READY" if not any(e["status"] in ["FAULTY", "MAINTENANCE"] for e in eq_list) else "NOT_READY"
        assessment["supply_status"] = "READY" if (sup_dict and sup_dict["status"] == "AVAILABLE") else "AT_RISK"

        results.append(assessment)

    return results

@router.get("/api/readiness/{surgery_id}")
def get_readiness_by_surgery(
    surgery_id: str,
    checkpoint: str = Query("T-30m"),
    db: Session = Depends(get_db)
):
    sched = db.query(TheatreSchedule).filter(TheatreSchedule.surgery_id == surgery_id).first()
    if not sched:
        return {"error": f"Surgery {surgery_id} not found"}

    patient_rec = sched.patient_readiness
    patient_dict = {
        "consent_complete": patient_rec.consent_complete if patient_rec else False,
        "fasting_complete": patient_rec.fasting_complete if patient_rec else False,
        "vitals_status": patient_rec.vitals_status if patient_rec else "NORMAL",
        "patient_ready": patient_rec.patient_ready if patient_rec else False,
        "last_updated": patient_rec.last_updated if patient_rec else sched.scheduled_start
    } if patient_rec else None

    staff_list = [{
        "role": s.role,
        "availability_status": s.availability_status,
        "last_updated": s.last_updated
    } for s in sched.staff_members]

    eq_rec = db.query(Equipment).filter(Equipment.theatre_id == sched.theatre_id).all()
    eq_list = [{
        "equipment_name": eq.equipment_name,
        "status": eq.status,
        "last_updated": eq.last_updated
    } for eq in eq_rec] if eq_rec else [{
        "equipment_name": "OT Primary Equipment",
        "status": "READY",
        "last_updated": sched.scheduled_start
    }]

    sup_dict = {
        "status": sched.sterile_supply.status if sched.sterile_supply else "AVAILABLE",
        "sterility_confirmed": sched.sterile_supply.sterility_confirmed if sched.sterile_supply else True
    } if sched.sterile_supply else None

    return evaluate_surgery_readiness(
        schedule={
            "surgery_id": sched.surgery_id,
            "scheduled_start": sched.scheduled_start,
            "previous_session_overrun": sched.previous_session_overrun
        },
        patient_data=patient_dict,
        staff_data=staff_list,
        equipment_data=eq_list,
        supply_data=sup_dict,
        checkpoint=checkpoint
    )
