from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class GoalBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: Optional[str] = "active"
    target_date: Optional[datetime] = None


class GoalCreate(GoalBase):
    pass


class GoalResponse(GoalBase):
    id: int
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None

    model_config = {"from_attributes": True}
