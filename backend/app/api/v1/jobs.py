# backend/app/api/v1/jobs.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from app.schemas.job import JobCreate, JobInDB, JobStatus
from app.services.job_service import JobService
from app.api.dependencies import get_db, get_current_active_user
from app.models import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/", response_model=JobInDB, status_code=status.HTTP_201_CREATED)
async def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "hiring_manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only hiring managers can create jobs"
        )
    
    try:
        return JobService(db).create_job(job, current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

@router.get("/my-jobs", response_model=List[JobInDB])
async def get_my_jobs(
    status: JobStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "hiring_manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only hiring managers can view jobs"
        )
    
    query = JobService(db).get_jobs_by_manager(current_user.id)
    if status:
        query = [job for job in query if job.status == status]
    return query
