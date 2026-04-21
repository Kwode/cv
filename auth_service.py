from passlib.context import CryptContext
import hashlib
from sqlalchemy.orm import Session
from student.schemas import StudentLogin
from company.schemas import CompanyLogin
from student.models import Student
from company.models import Company
from fastapi import HTTPException
from jwt_services import create_access_token

def prehash(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def hash_password(password: str):
    hashed = prehash(password)
    return pwd_context.hash(hashed)

def verify_password(plain_password: str, hashed_password: str):
    hashed_plain = prehash(plain_password)
    return pwd_context.verify(hashed_plain, hashed_password)

def student_login(db: Session, student: StudentLogin):
    existing_student = db.query(Student).filter(Student.email == student.email).first()

    if not existing_student: 
        raise HTTPException(status_code=400, detail="Invalid user or password")
    if not (verify_password(student.password, existing_student.password)):
        raise HTTPException(status_code=400, detail="Invalid user or password")
    
    token = create_access_token({
        'sub':str(existing_student.id),
        'email': existing_student.email,
        'role':'student'
    })
    
    return {
        'access_token':token,
        'token_type': 'bearer'
    }

def login_company(db: Session, company: CompanyLogin):
    existing_company = db.query(Company).filter(Company.email == company.email).first()

    if not existing_company: 
        raise HTTPException(status_code=400, detail="Invalid user or password")
    if not (verify_password(company.password, existing_company.password)):
        raise HTTPException(status_code=400, detail="Invalid user or password")
    
    token = create_access_token({
        'sub':str(existing_company.cac),
        'email': existing_company.email,
        'role':'company'
    })
    
    return {
        'access_token':token,
        'token_type': 'bearer'
    }