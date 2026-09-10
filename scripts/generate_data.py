#!/usr/bin/env python3
"""
Synthetic Data Generator for Operating Room Readiness Synchroniser (ORRS)
Generates >300 synthetic operating sessions across 6 CSV files in data/raw/
All patient, staff, and hospital IDs are 100% synthetic.
"""

import os
import random
import pandas as pd
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
os.makedirs(DATA_DIR, exist_ok=True)

random.seed(42)

DEPARTMENTS = ["Orthopaedics", "Cardiology", "General Surgery", "Neurology", "Urology", "Obstetrics & Gynaecology", "ENT", "Plastic Surgery"]
PROCEDURES = {
    "Orthopaedics": ["Knee Replacement", "Hip Arthroplasty", "Fracture Fixation", "ACL Reconstruction"],
    "Cardiology": ["CABG", "Angioplasty", "Valve Replacement", "Pacemaker Implantation"],
    "General Surgery": ["Laparoscopic Cholecystectomy", "Appendectomy", "Hernia Repair", "Colectomy"],
    "Neurology": ["Craniotomy", "Spinal Fusion", "Microdiscectomy", "Brain Tumor Resection"],
    "Urology": ["Prostatectomy", "Nephrectomy", "Kidney Stone Removal", "TURP"],
    "Obstetrics & Gynaecology": ["Cesarean Section", "Hysterectomy", "Ovarian Cystectomy", "Myomectomy"],
    "ENT": ["Tonsillectomy", "Septoplasty", "Tympanoplasty", "Sinus Surgery"],
    "Plastic Surgery": ["Reconstructive Surgery", "Skin Grafting", "Rhinoplasty", "Burn Debridement"]
}
THEATRES = [f"OT{i:03d}" for i in range(1, 9)]  # OT001 to OT008

EQUIPMENT_TYPES = ["Anesthesia Workstation", "C-Arm Fluoroscopy", "Surgical Diathermy", "Patient Monitor", "Laparoscopic Tower", "Heart-Lung Machine", "Operating Microscope", "Surgical Table"]
STAFF_ROLES = ["Surgeon", "Anaesthetist", "Nurse", "Technician"]

BASE_DATE = datetime(2026, 9, 10, 8, 0, 0)

def generate_datasets(num_sessions=320):
    print(f"Generating synthetic datasets for {num_sessions} operating sessions...")
    
    schedules = []
    staff_rosters = []
    equipment_statuses = []
    patient_readinesses = []
    sterile_supplies = []
    delay_reasons = []

    # Pre-generate staff pool
    staff_pool = []
    staff_id_counter = 1
    for dept in DEPARTMENTS:
        for role in STAFF_ROLES:
            count = 4 if role in ["Surgeon", "Nurse"] else 2
            for idx in range(count):
                staff_pool.append({
                    "staff_id": f"STAFF{staff_id_counter:03d}",
                    "staff_name_alias": f"Dr./Nurse {dept[:3].upper()}_{role[:3].upper()}_{idx+1}",
                    "role": role,
                    "department": dept
                })
                staff_id_counter += 1

    eq_id_counter = 1

    for i in range(1, num_sessions + 1):
        session_id = f"SESSION{i:03d}"
        surgery_id = f"SURG{i:03d}"
        patient_id = f"PAT{i:03d}"
        ot = random.choice(THEATRES)
        dept = random.choice(DEPARTMENTS)
        procedure = random.choice(PROCEDURES[dept])
        
        # Schedule timings
        day_offset = (i - 1) // 32
        start_hour_offset = (i % 8) * 2
        sched_start = BASE_DATE + timedelta(days=day_offset, hours=start_hour_offset)
        duration_mins = random.choice([60, 90, 120, 150, 180])
        sched_end = sched_start + timedelta(minutes=duration_mins)

        # Inject delay scenario (~32% of cases)
        has_delay = random.random() < 0.32
        delay_category = None
        delay_minutes = 0
        avoidable = False
        delay_reason_text = ""
        prev_overrun = "No"

        consent_complete = True
        fasting_complete = True
        preop_assessment = "CLEAR"
        vitals_status = "NORMAL"
        blood_available = "CONFIRMED"
        patient_ready = True

        eq_status = "READY"
        eq_maint = "OK"

        supply_status = "AVAILABLE"
        supply_qty_req = random.randint(3, 10)
        supply_qty_avail = supply_qty_req
        sterility_confirmed = True

        staff_avail_status = "AVAILABLE"

        if has_delay:
            delay_type = random.choice(["PATIENT", "STAFF", "EQUIPMENT", "SUPPLIES", "OVERRUN", "EMERGENCY", "MISSING_DATA"])
            
            if delay_type == "PATIENT":
                consent_complete = random.choice([True, False])
                fasting_complete = random.choice([True, False])
                vitals_status = random.choice(["ELEVATED_BP", "FEVER", "NORMAL"])
                patient_ready = consent_complete and fasting_complete and vitals_status == "NORMAL"
                delay_category = "Patient"
                delay_reason_text = "Patient fasting/consent incomplete or unstable vitals"
                delay_minutes = random.randint(15, 45)
                avoidable = True
            
            elif delay_type == "STAFF":
                staff_avail_status = random.choice(["DELAYED_IN_PREV_SURGERY", "STUCK_IN_TRAFFIC", "UNAVAILABLE"])
                delay_category = "Staff"
                delay_reason_text = f"Key staff (Surgeon/Anaesthetist) {staff_avail_status}"
                delay_minutes = random.randint(20, 60)
                avoidable = True

            elif delay_type == "EQUIPMENT":
                eq_status = random.choice(["FAULTY", "MAINTENANCE"])
                eq_maint = "REQUIRED"
                delay_category = "Equipment"
                delay_reason_text = f"Primary equipment {eq_status.lower()}"
                delay_minutes = random.randint(30, 90)
                avoidable = True

            elif delay_type == "SUPPLIES":
                supply_status = random.choice(["MISSING", "STERILITY_PENDING", "PARTIAL"])
                if supply_status == "PARTIAL":
                    supply_qty_avail = random.randint(1, supply_qty_req - 1)
                sterility_confirmed = False if supply_status == "STERILITY_PENDING" else True
                delay_category = "Supplies"
                delay_reason_text = f"Surgical supplies status: {supply_status}"
                delay_minutes = random.randint(15, 40)
                avoidable = True

            elif delay_type == "OVERRUN":
                prev_overrun = "Yes"
                delay_category = "Previous Surgery"
                delay_reason_text = "Previous theatre session overrun"
                delay_minutes = random.randint(25, 50)
                avoidable = False

            elif delay_type == "EMERGENCY":
                delay_category = "Emergency"
                delay_reason_text = "Operating theatre preempted by emergency trauma surgery"
                delay_minutes = random.randint(45, 120)
                avoidable = False

            elif delay_type == "MISSING_DATA":
                delay_category = "Staff"
                delay_reason_text = "Staff roster data stale / unconfirmed"
                delay_minutes = random.randint(10, 30)
                avoidable = True

        actual_start = sched_start + timedelta(minutes=delay_minutes)
        actual_end = actual_start + timedelta(minutes=duration_mins)

        priority = "Emergency" if (has_delay and delay_category == "Emergency") else random.choice(["Normal", "Normal", "Normal", "High"])

        # 1. Theatre Schedule record
        schedules.append({
            "session_id": session_id,
            "surgery_id": surgery_id,
            "theatre_id": ot,
            "department": dept,
            "procedure_type": procedure,
            "scheduled_start": sched_start.strftime("%Y-%m-%d %H:%M:%S"),
            "scheduled_end": sched_end.strftime("%Y-%m-%d %H:%M:%S"),
            "actual_start": actual_start.strftime("%Y-%m-%d %H:%M:%S"),
            "actual_end": actual_end.strftime("%Y-%m-%d %H:%M:%S"),
            "priority": priority,
            "previous_session_overrun": prev_overrun
        })

        # 2. Staff Roster records
        dept_staff = [s for s in staff_pool if s["department"] == dept]
        if not dept_staff:
            dept_staff = staff_pool[:4]
        
        roles_needed = ["Surgeon", "Anaesthetist", "Nurse", "Technician"]
        assigned_staff_list = []
        for r in roles_needed:
            candidates = [s for s in dept_staff if s["role"] == r]
            if not candidates:
                candidates = [s for s in staff_pool if s["role"] == r]
            assigned_staff_list.append(random.choice(candidates))

        is_stale_staff = (has_delay and delay_category == "Staff" and random.random() < 0.3)
        staff_update_time = sched_start - timedelta(minutes=65 if is_stale_staff else 10)

        for s in assigned_staff_list:
            cur_avail = staff_avail_status if (s["role"] in ["Surgeon", "Anaesthetist"] and has_delay and delay_category == "Staff") else "AVAILABLE"
            if has_delay and delay_category == "Staff" and s["role"] == "Anaesthetist" and random.random() < 0.25:
                cur_avail = None

            staff_rosters.append({
                "staff_id": s["staff_id"],
                "staff_name_alias": s["staff_name_alias"],
                "role": s["role"],
                "department": s["department"],
                "shift_start": (sched_start - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                "shift_end": (sched_end + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                "availability_status": cur_avail,
                "assigned_theatre": ot,
                "assigned_surgery": surgery_id,
                "last_updated": staff_update_time.strftime("%Y-%m-%d %H:%M:%S") if cur_avail else (sched_start - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
            })

        # 3. Equipment Status record (Unique equipment_id per row)
        is_stale_eq = (has_delay and delay_category == "Equipment" and random.random() < 0.3)
        eq_update_time = sched_start - timedelta(minutes=75 if is_stale_eq else 15)
        
        cur_eq_status = eq_status
        if has_delay and delay_category == "Equipment" and random.random() < 0.2:
            cur_eq_status = "UNKNOWN"

        equipment_statuses.append({
            "equipment_id": f"EQ{eq_id_counter:04d}",
            "equipment_name": random.choice(EQUIPMENT_TYPES),
            "theatre_id": ot,
            "status": cur_eq_status,
            "maintenance_status": eq_maint,
            "last_maintenance_date": (sched_start - timedelta(days=15)).strftime("%Y-%m-%d"),
            "last_updated": eq_update_time.strftime("%Y-%m-%d %H:%M:%S")
        })
        eq_id_counter += 1

        # 4. Patient Readiness record
        patient_update_time = sched_start - timedelta(minutes=20)
        patient_readinesses.append({
            "patient_id": patient_id,
            "surgery_id": surgery_id,
            "consent_complete": consent_complete,
            "fasting_complete": fasting_complete,
            "preoperative_assessment": preop_assessment,
            "vitals_status": vitals_status,
            "blood_available": blood_available,
            "patient_ready": patient_ready,
            "last_updated": patient_update_time.strftime("%Y-%m-%d %H:%M:%S")
        })

        # 5. Sterile Supplies record
        supply_update_time = sched_start - timedelta(minutes=30)
        sterile_supplies.append({
            "supply_id": f"SUP{i:03d}",
            "surgery_id": surgery_id,
            "supply_name": f"{dept} Surgical Pack-{i%5+1}",
            "required_quantity": supply_qty_req,
            "available_quantity": supply_qty_avail,
            "sterility_confirmed": sterility_confirmed,
            "status": supply_status,
            "last_updated": supply_update_time.strftime("%Y-%m-%d %H:%M:%S")
        })

        # 6. Delay Reasons record (if delay occurred)
        if has_delay and delay_minutes > 0:
            delay_reasons.append({
                "delay_id": f"DELAY{i:03d}",
                "surgery_id": surgery_id,
                "delay_category": delay_category,
                "delay_reason": delay_reason_text,
                "delay_minutes": delay_minutes,
                "avoidable": avoidable,
                "timestamp": actual_start.strftime("%Y-%m-%d %H:%M:%S")
            })

    # Save to CSV files
    pd.DataFrame(schedules).to_csv(os.path.join(DATA_DIR, "theatre_schedule.csv"), index=False)
    pd.DataFrame(staff_rosters).to_csv(os.path.join(DATA_DIR, "staff_roster.csv"), index=False)
    pd.DataFrame(equipment_statuses).to_csv(os.path.join(DATA_DIR, "equipment_status.csv"), index=False)
    pd.DataFrame(patient_readinesses).to_csv(os.path.join(DATA_DIR, "patient_readiness.csv"), index=False)
    pd.DataFrame(sterile_supplies).to_csv(os.path.join(DATA_DIR, "sterile_supplies.csv"), index=False)
    pd.DataFrame(delay_reasons).to_csv(os.path.join(DATA_DIR, "delay_reasons.csv"), index=False)

    print(f"Successfully generated 6 CSV datasets in {DATA_DIR}:")
    print(f"  - theatre_schedule.csv ({len(schedules)} rows)")
    print(f"  - staff_roster.csv ({len(staff_rosters)} rows)")
    print(f"  - equipment_status.csv ({len(equipment_statuses)} rows)")
    print(f"  - patient_readiness.csv ({len(patient_readinesses)} rows)")
    print(f"  - sterile_supplies.csv ({len(sterile_supplies)} rows)")
    print(f"  - delay_reasons.csv ({len(delay_reasons)} rows)")

if __name__ == "__main__":
    generate_datasets(320)
