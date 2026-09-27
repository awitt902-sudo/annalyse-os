from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from api.auth import get_current_user
from database.session import get_db
from models.project import ProjectModel
from schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    model = ProjectModel(**project.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


@router.get("/", response_model=List[ProjectResponse])
def list_projects(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    query = db.query(ProjectModel)
    if status_filter:
        query = query.filter(ProjectModel.status == status_filter)
    if q:
        query = query.filter((ProjectModel.title.ilike(f"%{q}%")) | (ProjectModel.description.ilike(f"%{q}%")))
    return query.offset(skip).limit(limit).all()
