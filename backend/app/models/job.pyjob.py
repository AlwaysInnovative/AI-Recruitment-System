from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from datetime import datetime

from app.models.base import Base

class JobStatus(str, Enum):
    draft = "draft"
    open = "open"
    closed = "closed"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(5000), nullable=False)
    requirements = Column(String(5000), nullable=False)
    location = Column(String(100), nullable=False)
    salary_range = Column(JSON)  # {"min": 50000, "max": 90000}
    status = Column(Enum(JobStatus), default=JobStatus.draft, nullable=False)
    hiring_manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Job {self.id}: {self.title}>"
