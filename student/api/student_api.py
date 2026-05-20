from fastapi import APIRouter, Depends
from dependencies.get_db import get_db
from sqlalchemy.orm import Session
from student.crud import get_students


router = APIRouter()

@router.get('/students')
def get_students_endpoint(db: Session = Depends(get_db)):
    return get_students(db)