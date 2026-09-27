from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    tech_stack: Optional[str] = None
    repository_url: Optional[str] = None
    status: Optional[str] = "active"


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None

    model_config = {"from_attributes": True}
