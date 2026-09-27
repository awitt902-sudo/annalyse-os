from fastapi import FastAPI
from database.base import Base
from database.session import engine

# Import every model before create_all so all tables are registered.
import models  # noqa: F401
from api.routers import auth, scholarships, notes, projects, mission_control, tasks, goals

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AnnalyseOS Mission Control API",
    description="Secure workflow and portfolio tracker for scholarships, notes, goals, tasks, and engineering projects.",
    version="2.0.0",
    contact={"name": "AnnalyseOS Engineering", "url": "https://github.com/awitt902-sudo"},
    openapi_tags=[
        {"name": "Authentication", "description": "User registration and JWT login."},
        {"name": "Scholarships", "description": "Track scholarship opportunities and deadlines."},
        {"name": "Notes", "description": "Save technical notes and knowledge snippets."},
        {"name": "Projects", "description": "Track software projects and portfolio work."},
        {"name": "Tasks", "description": "Manage active tasks and priorities."},
        {"name": "Goals", "description": "Track personal and professional goals."},
        {"name": "Mission Control", "description": "Overview metrics and dashboard aggregation."},
    ],
)

app.include_router(auth.router)
app.include_router(scholarships.router)
app.include_router(notes.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(goals.router)
app.include_router(mission_control.router)


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "service": "annalyseos-api"}


@app.get("/", tags=["System"])
def root():
    return {"system": "AnnalyseOS", "status": "online"}
