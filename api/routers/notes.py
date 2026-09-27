from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from api.auth import get_current_user
from database.session import get_db
from models.note import NoteModel
from schemas.note import NoteCreate, NoteResponse

router = APIRouter(prefix="/api/v1/notes", tags=["Notes"])


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    model = NoteModel(**note.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


@router.get("/", response_model=List[NoteResponse])
def list_notes(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    query = db.query(NoteModel)
    if category:
        query = query.filter(NoteModel.category.ilike(f"%{category}%"))
    if q:
        query = query.filter((NoteModel.title.ilike(f"%{q}%")) | (NoteModel.content.ilike(f"%{q}%")))
    return query.offset(skip).limit(limit).all()
