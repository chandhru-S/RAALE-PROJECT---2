from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.database import get_db
from backend.models.models import TheatreSchedule, PatientReadiness, SterileSupply, StaffRoster, Equipment, DelayReason, Alert
from backend.schemas.schemas import TheatreScheduleBase, SurgeryDetailResponse
from backend.services.readiness_engine import evaluate_surgery_readiness

router = APIRouter(tags=["Surgeries"])

@router.get("/api/surgeries", response_model=List[TheatreScheduleBase])
def get_all_surgeries(db: Session = Depends(get_db)):
    """
    Returns list of all scheduled operating sessions.
    """
    return db.query(TheatreSchedule).order_by(TheatreSchedule.scheduled_start).all()

@router.get("/api/surgeries/{surgery_id}")
def get_surgery_by_id(surgery_id: str, db: Session = Depends(get_db)):
    """
    Returns complete breakdown of a specific surgery including patient, staff, equipment, supply status, assessment score, and active alerts.
    """
    sched = db.query(TheatreSchedule).filter(TheatreSchedule.surgery_id == surgery_id).first()
    if not sched:
        raise HTTPException(status_code=404, detail=f"Surgery ID {surgery_id} not found")

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
        checkpoint="T-30m"
    )

    alerts = db.query(Alert).filter(Alert.surgery_id == surgery_id).all()

    return {
        "schedule": sched,
        "patient_readiness": sched.patient_readiness,
        "sterile_supply": sched.sterile_supply,
        "staff_members": sched.staff_members,
        "equipment": eq_rec,
        "delay_reason": sched.delay_reason,
        "latest_assessment": assessment,
        "alerts": alerts
    }
