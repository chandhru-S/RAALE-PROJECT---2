import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.models.models import Alert

def generate_alert_from_assessment(
    db: Session,
    assessment_data: Dict[str, Any],
    theatre_id: str,
    surgery_id: str
) -> Optional[Alert]:
    """
    Creates an alert record in DB if assessment status is NOT_READY, AT_RISK, or DATA_INCOMPLETE.
    """
    status = assessment_data.get("overall_status")
    if status == "READY":
        return None

    score = assessment_data.get("readiness_score", 0.0)
    confidence = assessment_data.get("confidence_score", 100.0)
    issue = assessment_data.get("blocking_issues", "Readiness check warning")
    action = assessment_data.get("recommended_actions", "Manual verification required")

    if status == "NOT_READY":
        severity = "HIGH"
    elif status == "DATA_INCOMPLETE":
        severity = "HIGH" if confidence < 50.0 else "MEDIUM"
    else: # AT_RISK
        severity = "MEDIUM" if score < 75.0 else "LOW"

    # Check if active alert already exists for surgery
    existing = db.query(Alert).filter(Alert.surgery_id == surgery_id, Alert.status == "ACTIVE").first()
    if existing:
        existing.severity = severity
        existing.issue = issue
        existing.confidence_score = confidence
        existing.recommended_action = action
        db.commit()
        db.refresh(existing)
        return existing

    alert = Alert(
        alert_id=f"ALT_{uuid.uuid4().hex[:8].upper()}",
        severity=severity,
        theatre_id=theatre_id,
        surgery_id=surgery_id,
        issue=issue,
        confidence_score=confidence,
        recommended_action=action,
        status="ACTIVE",
        created_at=datetime.utcnow()
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

def acknowledge_alert(db: Session, alert_id: str) -> Optional[Alert]:
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if alert:
        alert.status = "ACKNOWLEDGED"
        db.commit()
        db.refresh(alert)
    return alert
