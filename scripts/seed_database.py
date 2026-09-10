#!/usr/bin/env python3
"""
Database Seeder Script for ORRS.
Reads generated CSV files from data/raw/ and populates SQLite database tables.
Also calculates initial readiness assessments and alerts.
"""

import os
import pandas as pd
from datetime import datetime
from backend.database import engine, Base, SessionLocal
from backend.models import (
    TheatreSchedule,
    StaffRoster,
    Equipment,
    PatientReadiness,
    SterileSupply,
    DelayReason
)
from backend.services.readiness_engine import evaluate_surgery_readiness
from backend.services.alert_engine import generate_alert_from_assessment

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")

def parse_dt(val):
    if pd.isna(val) or not val:
        return None
    if isinstance(val, str):
        return datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
    return val

def seed_database():
    print("Re-creating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("Seeding Theatre Schedules...")
        sched_df = pd.read_csv(os.path.join(DATA_DIR, "theatre_schedule.csv"))
        for _, row in sched_df.iterrows():
            db.add(TheatreSchedule(
                session_id=row["session_id"],
                surgery_id=row["surgery_id"],
                theatre_id=row["theatre_id"],
                department=row["department"],
                procedure_type=row["procedure_type"],
                scheduled_start=parse_dt(row["scheduled_start"]),
                scheduled_end=parse_dt(row["scheduled_end"]),
                actual_start=parse_dt(row["actual_start"]),
                actual_end=parse_dt(row["actual_end"]),
                priority=row["priority"],
                previous_session_overrun=row["previous_session_overrun"]
            ))
        db.commit()

        print("Seeding Staff Rosters...")
        staff_df = pd.read_csv(os.path.join(DATA_DIR, "staff_roster.csv"))
        for _, row in staff_df.iterrows():
            avail = row["availability_status"]
            if pd.isna(avail) or str(avail).upper() in ["NAN", "NULL", "NONE"]:
                avail = None
            db.add(StaffRoster(
                staff_id=row["staff_id"],
                staff_name_alias=row["staff_name_alias"],
                role=row["role"],
                department=row["department"],
                shift_start=parse_dt(row["shift_start"]),
                shift_end=parse_dt(row["shift_end"]),
                availability_status=avail,
                assigned_theatre=row["assigned_theatre"],
                assigned_surgery=row["assigned_surgery"],
                last_updated=parse_dt(row["last_updated"])
            ))
        db.commit()

        print("Seeding Equipment Status...")
        eq_df = pd.read_csv(os.path.join(DATA_DIR, "equipment_status.csv"))
        for _, row in eq_df.iterrows():
            db.add(Equipment(
                equipment_id=row["equipment_id"],
                equipment_name=row["equipment_name"],
                theatre_id=row["theatre_id"],
                status=row["status"],
                maintenance_status=row["maintenance_status"],
                last_maintenance_date=datetime.strptime(row["last_maintenance_date"], "%Y-%m-%d") if pd.notna(row["last_maintenance_date"]) else None,
                last_updated=parse_dt(row["last_updated"])
            ))
        db.commit()

        print("Seeding Patient Readiness...")
        pat_df = pd.read_csv(os.path.join(DATA_DIR, "patient_readiness.csv"))
        for _, row in pat_df.iterrows():
            db.add(PatientReadiness(
                patient_id=row["patient_id"],
                surgery_id=row["surgery_id"],
                consent_complete=bool(row["consent_complete"]),
                fasting_complete=bool(row["fasting_complete"]),
                preoperative_assessment=str(row["preoperative_assessment"]),
                vitals_status=str(row["vitals_status"]),
                blood_available=str(row["blood_available"]),
                patient_ready=bool(row["patient_ready"]),
                last_updated=parse_dt(row["last_updated"])
            ))
        db.commit()

        print("Seeding Sterile Supplies...")
        sup_df = pd.read_csv(os.path.join(DATA_DIR, "sterile_supplies.csv"))
        for _, row in sup_df.iterrows():
            db.add(SterileSupply(
                supply_id=row["supply_id"],
                surgery_id=row["surgery_id"],
                supply_name=row["supply_name"],
                required_quantity=int(row["required_quantity"]),
                available_quantity=int(row["available_quantity"]),
                sterility_confirmed=bool(row["sterility_confirmed"]),
                status=row["status"],
                last_updated=parse_dt(row["last_updated"])
            ))
        db.commit()

        print("Seeding Delay Reasons...")
        del_df = pd.read_csv(os.path.join(DATA_DIR, "delay_reasons.csv"))
        for _, row in del_df.iterrows():
            db.add(DelayReason(
                delay_id=row["delay_id"],
                surgery_id=row["surgery_id"],
                delay_category=row["delay_category"],
                delay_reason=row["delay_reason"],
                delay_minutes=int(row["delay_minutes"]),
                avoidable=bool(row["avoidable"]),
                timestamp=parse_dt(row["timestamp"])
            ))
        db.commit()

        print("Calculating initial readiness assessments and alerts...")
        schedules = db.query(TheatreSchedule).all()
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

            eq_list = [{
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

            generate_alert_from_assessment(db, assessment, sched.theatre_id, sched.surgery_id)

        print("Database seeded successfully with initial data, assessments, and alerts!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
