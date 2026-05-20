from fastapi import APIRouter, Depends
from dependencies.get_db import get_db
from sqlalchemy.orm import Session
from company.crud import get_companies


router = APIRouter()

@router.get('/company')
def get_companies_endpoint(db: Session = Depends(get_db)):
    return get_companies(db)

