from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class TheatreScheduleBase(BaseModel):
    session_id: str
    surgery_id: str
    theatre_id: str
    department: str
    procedure_type: str
    scheduled_start: datetime
    scheduled_end: datetime
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    priority: str = "Normal"
    previous_session_overrun: str = "No"

    model_config = ConfigDict(from_attributes=True)

class StaffRosterBase(BaseModel):
    staff_id: str
    staff_name_alias: str
    role: str
    department: str
    shift_start: datetime
    shift_end: datetime
    availability_status: Optional[str] = "AVAILABLE"
    assigned_theatre: Optional[str] = None
    assigned_surgery: Optional[str] = None
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)

class EquipmentBase(BaseModel):
    equipment_id: str
    equipment_name: str
    theatre_id: str
    status: str
    maintenance_status: str
    last_maintenance_date: Optional[datetime] = None
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)

class PatientReadinessBase(BaseModel):
    patient_id: str
    surgery_id: str
    consent_complete: bool
    fasting_complete: bool
    preoperative_assessment: str
    vitals_status: str
    blood_available: str
    patient_ready: bool
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)

class SterileSupplyBase(BaseModel):
    supply_id: str
    surgery_id: str
    supply_name: str
    required_quantity: int
    available_quantity: int
    sterility_confirmed: bool
    status: str
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)

class DelayReasonBase(BaseModel):
    delay_id: str
    surgery_id: str
    delay_category: str
    delay_reason: str
    delay_minutes: int
    avoidable: bool
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class ReadinessAssessmentBase(BaseModel):
    id: Optional[int] = None
    surgery_id: str
    checkpoint: str
    overall_status: str
    readiness_score: float
    confidence_score: float
    patient_score: float
    staff_score: float
    equipment_score: float
    supply_score: float
    theatre_score: float
    blocking_issues: Optional[str] = None
    recommended_actions: Optional[str] = None
    assessed_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AlertBase(BaseModel):
    id: Optional[int] = None
    alert_id: str
    severity: str
    theatre_id: str
    surgery_id: str
    issue: str
    confidence_score: float
    recommended_action: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SurgeryDetailResponse(BaseModel):
    schedule: TheatreScheduleBase
    patient_readiness: Optional[PatientReadinessBase] = None
    sterile_supply: Optional[SterileSupplyBase] = None
    staff_members: List[StaffRosterBase] = []
    equipment: List[EquipmentBase] = []
    delay_reason: Optional[DelayReasonBase] = None
    latest_assessment: Optional[ReadinessAssessmentBase] = None
    alerts: List[AlertBase] = []

    model_config = ConfigDict(from_attributes=True)

class SimulationResponse(BaseModel):
    success: bool
    message: str
    surgery_id: str
    theatre_id: str
    new_status: str
    readiness_score: float
    confidence_score: float
    alerts_generated: int
