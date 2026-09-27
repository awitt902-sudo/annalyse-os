from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.auth import get_current_user
from database.session import get_db
from models.goal import GoalModel
from models.scholarship import ScholarshipModel
from models.task import TaskModel

router = APIRouter(prefix="/api/v1/mission-control", tags=["Mission Control"])


@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    pending_scholarships = db.query(ScholarshipModel).filter(ScholarshipModel.status == "pending").all()
    active_tasks = db.query(TaskModel).filter(TaskModel.status == "in_progress").all()
    active_goals = db.query(GoalModel).filter(GoalModel.status == "active").all()

    return {
        "system_status": "nominal",
        "metrics": {
            "pending_scholarships_count": len(pending_scholarships),
            "active_tasks_count": len(active_tasks),
            "active_goals_count": len(active_goals),
        },
        "highlights": {
            "pending_scholarships": [item.title for item in pending_scholarships[:5]],
            "immediate_tasks": [item.title for item in active_tasks[:5]],
        },
    }
