from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.auth import get_current_user
from database.session import get_db
from models.goal import GoalModel
from schemas.goal import GoalCreate, GoalResponse

router = APIRouter(prefix="/api/v1/goals", tags=["Goals"])


@router.post("/", response_model=GoalResponse, status_code=201)
def create_goal(goal: GoalCreate, db: Session = Depends(get_db), _: object = Depends(get_current_user)):
    model = GoalModel(**goal.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


@router.get("/", response_model=list[GoalResponse])
def list_goals(db: Session = Depends(get_db), _: object = Depends(get_current_user)):
    return db.query(GoalModel).all()
