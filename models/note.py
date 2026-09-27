from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text

from database.base import Base


class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), default="General")
    content = Column(Text, nullable=False)
    tags = Column(String(255), nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
