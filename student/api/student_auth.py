from fastapi import APIRouter, Depends, HTTPException
from student.schemas import StudentRegister, StudentLogin, StudentResponse
from dependencies.get_db import get_db
from sqlalchemy.orm import Session
from student.crud import register_student
from auth_service import student_login
from student.models import Student


router = APIRouter()

@router.post('/register/student', response_model=StudentResponse)
def register(student: StudentRegister, db: Session = Depends(get_db)):
    existing_user = db.query(Student).filter(Student.email == student.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Student already exists")
    
    new_student = register_student(db, student)

    return new_student

@router.post('/login/student')
def login(student: StudentLogin, db: Session = Depends(get_db)):
    return student_login(db, student)