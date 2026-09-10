from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.models import ExperimentResult
from backend.services.experiment_engine import run_experiment

router = APIRouter(tags=["Experiments"])

@router.get("/api/experiments")
def get_latest_experiment(db: Session = Depends(get_db)):
    """
    Returns the results of the latest baseline vs prototype evaluation experiment.
    """
    exp = db.query(ExperimentResult).order_by(ExperimentResult.executed_at.desc()).first()
    if not exp:
        # Run experiment on the fly if not run yet
        return run_experiment(db)
    return exp

@router.post("/api/run-experiment")
def execute_experiment(db: Session = Depends(get_db)):
    """
    Triggers a fresh programmatic execution of the 300+ session experiment.
    """
    results = run_experiment(db)
    return {
        "success": True,
        "message": "Experiment executed successfully across 300+ operating sessions",
        "results": results
    }
