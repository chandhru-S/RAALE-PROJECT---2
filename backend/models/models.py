from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class TheatreSchedule(Base):
    __tablename__ = "theatre_schedules"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    surgery_id = Column(String, unique=True, index=True)
    theatre_id = Column(String, index=True)
    department = Column(String, index=True)
    procedure_type = Column(String)
    scheduled_start = Column(DateTime)
    scheduled_end = Column(DateTime)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)
    priority = Column(String, default="Normal")  # Normal, High, Emergency
    previous_session_overrun = Column(String, default="No") # Yes / No

    patient_readiness = relationship("PatientReadiness", back_populates="schedule", uselist=False)
    sterile_supply = relationship("SterileSupply", back_populates="schedule", uselist=False)
    staff_members = relationship("StaffRoster", back_populates="schedule")
    delay_reason = relationship("DelayReason", back_populates="schedule", uselist=False)
    readiness_assessments = relationship("ReadinessAssessment", back_populates="schedule")
    alerts = relationship("Alert", back_populates="schedule")

class StaffRoster(Base):
    __tablename__ = "staff_rosters"

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(String, index=True)
    staff_name_alias = Column(String)
    role = Column(String)  # Surgeon, Anaesthetist, Nurse, Technician
    department = Column(String)
    shift_start = Column(DateTime)
    shift_end = Column(DateTime)
    availability_status = Column(String, nullable=True) # AVAILABLE, DELAYED, UNAVAILABLE, NULL
    assigned_theatre = Column(String, nullable=True)
    assigned_surgery = Column(String, ForeignKey("theatre_schedules.surgery_id"), nullable=True)
    last_updated = Column(DateTime)

    schedule = relationship("TheatreSchedule", back_populates="staff_members")

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(String, unique=True, index=True)
    equipment_name = Column(String)
    theatre_id = Column(String, index=True)
    status = Column(String, default="READY") # READY, IN_USE, MAINTENANCE, FAULTY, UNKNOWN
    maintenance_status = Column(String, default="OK")
    last_maintenance_date = Column(DateTime, nullable=True)
    last_updated = Column(DateTime)

class PatientReadiness(Base):
    __tablename__ = "patient_readiness"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    surgery_id = Column(String, ForeignKey("theatre_schedules.surgery_id"), unique=True)
    consent_complete = Column(Boolean, default=False)
    fasting_complete = Column(Boolean, default=False)
    preoperative_assessment = Column(String, default="PENDING")
    vitals_status = Column(String, default="NORMAL") # NORMAL, ELEVATED_BP, FEVER, ABNORMAL
    blood_available = Column(String, default="CONFIRMED")
    patient_ready = Column(Boolean, default=False)
    last_updated = Column(DateTime)

    schedule = relationship("TheatreSchedule", back_populates="patient_readiness")

class SterileSupply(Base):
    __tablename__ = "sterile_supplies"

    id = Column(Integer, primary_key=True, index=True)
    supply_id = Column(String, index=True)
    surgery_id = Column(String, ForeignKey("theatre_schedules.surgery_id"), unique=True)
    supply_name = Column(String)
    required_quantity = Column(Integer)
    available_quantity = Column(Integer)
    sterility_confirmed = Column(Boolean, default=False)
    status = Column(String, default="AVAILABLE") # AVAILABLE, PARTIAL, MISSING, STERILITY_PENDING
    last_updated = Column(DateTime)

    schedule = relationship("TheatreSchedule", back_populates="sterile_supply")

class DelayReason(Base):
    __tablename__ = "delay_reasons"

    id = Column(Integer, primary_key=True, index=True)
    delay_id = Column(String, index=True)
    surgery_id = Column(String, ForeignKey("theatre_schedules.surgery_id"), unique=True)
    delay_category = Column(String) # Patient, Staff, Equipment, Supplies, Theatre, Previous Surgery, Emergency
    delay_reason = Column(String)
    delay_minutes = Column(Integer, default=0)
    avoidable = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    schedule = relationship("TheatreSchedule", back_populates="delay_reason")

class ReadinessAssessment(Base):
    __tablename__ = "readiness_assessments"

    id = Column(Integer, primary_key=True, index=True)
    surgery_id = Column(String, ForeignKey("theatre_schedules.surgery_id"), index=True)
    checkpoint = Column(String) # T-60m, T-30m, T-15m, T-0m
    overall_status = Column(String) # READY, AT_RISK, NOT_READY, DATA_INCOMPLETE
    readiness_score = Column(Float) # 0 - 100
    confidence_score = Column(Float) # 0 - 100
    patient_score = Column(Float)
    staff_score = Column(Float)
    equipment_score = Column(Float)
    supply_score = Column(Float)
    theatre_score = Column(Float)
    blocking_issues = Column(String, nullable=True) # JSON or comma-separated
    recommended_actions = Column(String, nullable=True)
    assessed_at = Column(DateTime, default=datetime.utcnow)

    schedule = relationship("TheatreSchedule", back_populates="readiness_assessments")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String, unique=True, index=True)
    severity = Column(String) # HIGH, MEDIUM, LOW
    theatre_id = Column(String)
    surgery_id = Column(String, ForeignKey("theatre_schedules.surgery_id"))
    issue = Column(String)
    confidence_score = Column(Float)
    recommended_action = Column(String)
    status = Column(String, default="ACTIVE") # ACTIVE, ACKNOWLEDGED, RESOLVED
    created_at = Column(DateTime, default=datetime.utcnow)

    schedule = relationship("TheatreSchedule", back_populates="alerts")

class ExperimentResult(Base):
    __tablename__ = "experiment_results"

    id = Column(Integer, primary_key=True, index=True)
    total_sessions = Column(Integer)
    baseline_avg_idle_mins = Column(Float)
    baseline_median_idle_mins = Column(Float)
    baseline_total_idle_mins = Column(Float)
    prototype_avg_idle_mins = Column(Float)
    prototype_median_idle_mins = Column(Float)
    prototype_total_idle_mins = Column(Float)
    idle_time_reduction_pct = Column(Float)
    early_detection_rate = Column(Float)
    alert_precision = Column(Float)
    false_positive_rate = Column(Float)
    false_negative_rate = Column(Float)
    target_achieved = Column(Boolean)
    executed_at = Column(DateTime, default=datetime.utcnow)
