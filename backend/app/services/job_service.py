# backend/app/services/job_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import Job, User
from app.schemas.job import JobCreate, JobInDB
from app.utils.logging import logger

class JobService:
    def __init__(self, db: Session):
        self.db = db

    def create_job(self, job: JobCreate, hiring_manager_id: int) -> JobInDB:
        try:
            db_job = Job(
                **job.dict(exclude_unset=True),
                hiring_manager_id=hiring_manager_id
            )
            self.db.add(db_job)
            self.db.commit()
            self.db.refresh(db_job)
            logger.info(f"Created new job ID {db_job.id} by manager {hiring_manager_id}")
            return db_job
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create job: {str(e)}")
            raise

    def get_job(self, job_id: int) -> Optional[JobInDB]:
        return self.db.query(Job).filter(Job.id == job_id).first()

    def get_jobs_by_manager(self, manager_id: int, limit: int = 100) -> List[JobInDB]:
        return (
            self.db.query(Job)
            .filter(Job.hiring_manager_id == manager_id)
            .order_by(desc(Job.created_at))
            .limit(limit)
            .all()
        )
