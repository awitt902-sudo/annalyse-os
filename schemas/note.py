from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1)
    category: Optional[str] = "General"
    content: str = Field(..., min_length=1)
    tags: Optional[str] = None


class NoteCreate(NoteBase):
    pass


class NoteResponse(NoteBase):
    id: int
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None

    model_config = {"from_attributes": True}
