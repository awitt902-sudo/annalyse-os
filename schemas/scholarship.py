from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ScholarshipBase(BaseModel):
    title: str = Field(..., min_length=1)
    organization: Optional[str] = None
    deadline: Optional[datetime] = None
    amount: Optional[float] = None
    eligibility_criteria: Optional[str] = None
    application_link: Optional[str] = None
    status: Optional[str] = "pending"
    notes: Optional[str] = None


class ScholarshipCreate(ScholarshipBase):
    pass


class ScholarshipUpdate(BaseModel):
    title: Optional[str] = None
    organization: Optional[str] = None
    deadline: Optional[datetime] = None
    amount: Optional[float] = None
    eligibility_criteria: Optional[str] = None
    application_link: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class ScholarshipResponse(ScholarshipBase):
    id: int
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None

    model_config = {"from_attributes": True}
