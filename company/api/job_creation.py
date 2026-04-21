from fastapi import APIRouter, Depends, HTTPException
from company.schemas import JobCreate, JobResponse
from dependencies.get_db import get_db
from dependencies.get_current_user import get_current_user
from sqlalchemy.orm import Session
from company.crud import create_job, delete_job
from company.models import Job


router = APIRouter()

@router.post('/job', response_model=JobResponse)
def create_job_endpoint(job: JobCreate, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_job = db.query(Job).filter(Job.role == job.role).first()

    if existing_job:
        raise HTTPException(status_code=400, detail="Job already exists")
    
    if user["role"] != "company":
        raise HTTPException(status_code=403, detail="Not Authorized")
    
    new_job = create_job(db, job, user['id'])

    return new_job

@router.delete('/job/{id}')
def delete_job_endpoint(id: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):

    if user["role"] != "company":
        raise HTTPException(status_code=403, detail="Not Authorized")
    
    return delete_job(db, id)

