from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.auth import get_current_user
from database.session import get_db
from models.scholarship import ScholarshipModel

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.get("/stats")
def admin_stats(db: Session = Depends(get_db), _: object = Depends(get_current_user)):
    return {
        "total_scholarships": db.query(ScholarshipModel).count(),
        "status": "admin-access-ok",
    }
