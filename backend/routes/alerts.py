from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models.models import Alert
from backend.schemas.schemas import AlertBase
from backend.services.alert_engine import acknowledge_alert

router = APIRouter(tags=["Alerts"])

@router.get("/api/alerts", response_model=List[AlertBase])
def get_alerts(status: str = "ALL", db: Session = Depends(get_db)):
    """
    Returns alerts filtered by status (ACTIVE, ACKNOWLEDGED, RESOLVED, or ALL).
    """
    query = db.query(Alert)
    if status != "ALL":
        query = query.filter(Alert.status == status)
    return query.order_by(Alert.created_at.desc()).all()

@router.post("/api/alerts/{alert_id}/acknowledge")
def acknowledge_alert_endpoint(alert_id: str, db: Session = Depends(get_db)):
    """
    Acknowledges an active alert.
    """
    alert = acknowledge_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    return {
        "success": True,
        "message": f"Alert {alert_id} acknowledged by authorized staff",
        "alert": alert
    }
