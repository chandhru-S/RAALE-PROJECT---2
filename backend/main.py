import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, Base, SessionLocal
from backend.models.models import TheatreSchedule
from backend.routes import health, theatres, surgeries, readiness, alerts, analytics, experiments, simulate
from scripts.generate_data import generate_datasets
from scripts.seed_database import seed_database

app = FastAPI(
    title="Operating Room Readiness Synchroniser (ORRS) API",
    description="Full-stack clinical operations engine for operating theatre synchronisation and delay prevention.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router)
app.include_router(theatres.router)
app.include_router(surgeries.router)
app.include_router(readiness.router)
app.include_router(alerts.router)
app.include_router(analytics.router)
app.include_router(experiments.router)
app.include_router(simulate.router)

@app.on_event("startup")
def startup_event():
    """
    On startup: Ensures synthetic CSV files exist, creates database tables, and seeds database if empty.
    """
    data_raw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
    csv_file = os.path.join(data_raw_dir, "theatre_schedule.csv")

    if not os.path.exists(csv_file):
        print("Generating synthetic datasets...")
        generate_datasets(320)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        count = db.query(TheatreSchedule).count()
        if count == 0:
            print("Database empty. Seeding initial hospital data...")
            seed_database()
        else:
            print(f"Database ready with {count} operating sessions.")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
