from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from api.auth import get_current_user
from database.session import get_db
from models.scholarship import ScholarshipModel
from schemas.scholarship import ScholarshipCreate, ScholarshipResponse, ScholarshipUpdate

router = APIRouter(prefix="/api/v1/scholarships", tags=["Scholarships"])


@router.post("/", response_model=ScholarshipResponse, status_code=status.HTTP_201_CREATED)
def create_scholarship(
    scholarship: ScholarshipCreate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    model = ScholarshipModel(**scholarship.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


@router.get("/", response_model=List[ScholarshipResponse])
def list_scholarships(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    return db.query(ScholarshipModel).offset(skip).limit(limit).all()


@router.get("/{scholarship_id}", response_model=ScholarshipResponse)
def get_scholarship(
    scholarship_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    scholarship = db.query(ScholarshipModel).filter(ScholarshipModel.id == scholarship_id).first()
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return scholarship


@router.patch("/{scholarship_id}", response_model=ScholarshipResponse)
def update_scholarship(
    scholarship_id: int,
    scholarship_update: ScholarshipUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    scholarship = db.query(ScholarshipModel).filter(ScholarshipModel.id == scholarship_id).first()
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")

    update_data = scholarship_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(scholarship, key, value)

    db.commit()
    db.refresh(scholarship)
    return scholarship
