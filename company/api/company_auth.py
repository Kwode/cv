from fastapi import APIRouter, Depends, HTTPException
from company.schemas import CompanyRegister, CompanyLogin, CompanyResponse
from dependencies.get_db import get_db
from sqlalchemy.orm import Session
from company.crud import register_company
from auth_service import login_company
from company.models import Company


router = APIRouter()

@router.post('/register/company', response_model=CompanyResponse)
def register_company_endpoint(company: CompanyRegister, db: Session = Depends(get_db)):
    existing_user = db.query(Company).filter(Company.email == company.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Organization already exists")
    
    new_company = register_company(db, company)

    return new_company

@router.post('/login/company')
def login_company_endpoint(company: CompanyLogin, db: Session = Depends(get_db)):
    return login_company(db, company)

