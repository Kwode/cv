from sqlalchemy.orm import Session
from company.schemas import CompanyRegister, JobCreate
from company.models import Company, Job
from auth_service import hash_password
from company.services.company_ai_service import store_job_in_vector_db


def register_company(db: Session, company: CompanyRegister):
    new_company = Company(
        name = company.name,
        email = company.email,
        cac = company.cac,
        location = company.location,
        industry = company.industry,
        description = company.description,
        password = hash_password(company.password)
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company

def create_job(db: Session, job: JobCreate, company_id: str):
    new_job = Job(
        role = job.role,
        required_skills = job.required_skills,
        responsibilities = job.responsibilities,
        preferred_skills = job.preferred_skills,
        experience_level = job.experience_level,
        company_id = company_id
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    store_job_in_vector_db(
        job=new_job,
        job_id=new_job.id,
        company_id=company_id
    )

    return new_job

def get_companies(db: Session):
    return db.query(Company).all()

def get_company(db: Session, cac: str):
    return db.query(Company).filter(Company.cac == cac).first()

def delete_company(db: Session, cac: str):
    company = db.query(Company).filter(Company.cac == cac).first()
    db.delete(company)
    db.commit()
    return company

def get_jobs(db: Session):
    return db.query(Job).all()

def get_job(db: Session, id: str):
    return db.query(Job).filter(Job.id == id).first()

def delete_job(db: Session, id: str):
    job = db.query(Job).filter(Job.id == id).first()
    db.delete(job)
    db.commit()
    return job