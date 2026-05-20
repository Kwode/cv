from sqlalchemy.orm import Session
from company.models import Job

def get_jobs_by_company(db: Session, company_id: str):
    return db.query(Job).filter(Job.company_id == company_id).all()