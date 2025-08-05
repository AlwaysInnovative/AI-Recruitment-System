# backend/app/schemas/job.py
from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel, validator, Field
from enum import Enum

class JobStatus(str, Enum):
    draft = "draft"
    open = "open"
    closed = "closed"

class JobBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=50)
    requirements: str = Field(..., min_length=50)
    location: str = Field(..., max_length=100)
    salary_range: Optional[Dict[str, float]] = None
    status: JobStatus = JobStatus.draft

class JobCreate(JobBase):
    @validator('salary_range')
    def validate_salary_range(cls, v):
        if v:
            if 'min' not in v or 'max' not in v:
                raise ValueError("Both min and max salary must be provided")
            if v['min'] > v['max']:
                raise ValueError("Minimum salary cannot be greater than maximum")
            if v['min'] < 0 or v['max'] < 0:
                raise ValueError("Salary values cannot be negative")
        return v

class JobInDB(JobBase):
    id: int
    hiring_manager_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
