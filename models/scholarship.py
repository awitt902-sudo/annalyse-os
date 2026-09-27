from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from database.base import Base


class ScholarshipModel(Base):
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    organization = Column(String(255), nullable=True)
    deadline = Column(DateTime, nullable=True)
    amount = Column(Float, nullable=True)
    eligibility_criteria = Column(Text, nullable=True)
    application_link = Column(String(500), nullable=True)
    status = Column(String(50), default="pending")
    notes = Column(Text, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
