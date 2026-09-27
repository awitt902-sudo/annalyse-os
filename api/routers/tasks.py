from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.auth import get_current_user
from database.session import get_db
from models.task import TaskModel
from schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db), _: object = Depends(get_current_user)):
    model = TaskModel(**task.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


@router.get("/", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db), _: object = Depends(get_current_user)):
    return db.query(TaskModel).all()
