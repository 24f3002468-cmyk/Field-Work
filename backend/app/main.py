import os
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.models.models import PlannerDay, PlannerTask, Milestone, ProjectStage, ProjectChecklist
from app.api.v1 import (
    auth, planner, tasks, daily_logs, milestones, dsa, project, iitm,
    placement_points, applications, verification, export, analytics
)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="1.0.0"
)

# Enable CORS for local and production React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def seed_database_if_needed():
    db = SessionLocal()
    try:
        if db.query(PlannerDay).count() == 0:
            json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "planner", "planner_data.json")
            if not os.path.exists(json_path):
                json_path = os.path.join(os.getcwd(), "planner", "planner_data.json")

            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Seed Milestones
                for m in data.get("milestones", []):
                    db.add(Milestone(
                        id=m["id"],
                        name=m["name"],
                        target_day=m["target_day"],
                        target_date=m["target_date"],
                        description=m.get("description"),
                        critical=m.get("critical", False),
                        part=m.get("part", 1),
                        phase=m.get("phase")
                    ))

                # Seed Project Stages
                for ps in data.get("project_stages", []):
                    db.add(ProjectStage(
                        id=ps["id"],
                        stage_number=ps["id"],
                        name=ps["name"],
                        description=ps.get("description")
                    ))

                # Seed Project Checklist
                for pc in data.get("project_checklist", []):
                    db.add(ProjectChecklist(
                        id=pc["id"],
                        title=pc["title"],
                        verified=pc.get("verified", False)
                    ))

                # Seed Planner Days and Tasks
                for day in data.get("days", []):
                    p_day = PlannerDay(
                        day_number=day["day_number"],
                        date=day["date"],
                        weekday=day["weekday"],
                        part=day["part"],
                        phase=day["phase"],
                        sub_phase=day.get("sub_phase"),
                        primary_technology=day.get("primary_technology"),
                        total_planned_minutes=day["total_planned_minutes"],
                        milestone_name=day.get("milestone")
                    )
                    db.add(p_day)

                    for t in day.get("tasks", []):
                        db.add(PlannerTask(
                            id=t["id"],
                            day_number=t["day_number"],
                            category=t["category"],
                            name=t["name"],
                            description=t.get("description"),
                            planned_start=t.get("planned_start"),
                            planned_end=t.get("planned_end"),
                            planned_minutes=t["planned_minutes"],
                            priority=t.get("priority", "MEDIUM"),
                            is_critical=t.get("is_critical", False)
                        ))

                db.commit()
                print("Database successfully seeded with 200 planner days.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    seed_database_if_needed()

# Include API Routers under /api/v1
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(planner.router, prefix=settings.API_V1_STR)
app.include_router(tasks.router, prefix=settings.API_V1_STR)
app.include_router(daily_logs.router, prefix=settings.API_V1_STR)
app.include_router(milestones.router, prefix=settings.API_V1_STR)
app.include_router(dsa.router, prefix=settings.API_V1_STR)
app.include_router(project.router, prefix=settings.API_V1_STR)
app.include_router(iitm.router, prefix=settings.API_V1_STR)
app.include_router(placement_points.router, prefix=settings.API_V1_STR)
app.include_router(applications.router, prefix=settings.API_V1_STR)
app.include_router(verification.router, prefix=settings.API_V1_STR)
app.include_router(export.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)

@app.get("/api/health")
def root_health():
    return {"message": "200-Day ML Systems Execution Dashboard API", "docs": "/docs"}

# Single-Service SPA Frontend static serving fallback
frontend_dist = os.path.join(os.getcwd(), "frontend", "dist")
if not os.path.exists(frontend_dist):
    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")

if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return None
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
