from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text

from database.base import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    tech_stack = Column(String(255), nullable=True)
    repository_url = Column(String(500), nullable=True)
    status = Column(String(50), default="active")
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
