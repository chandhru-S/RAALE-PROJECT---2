from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Operating Room Readiness Synchroniser API",
        "version": "1.0.0"
    }
