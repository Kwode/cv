from sqlalchemy.orm import Session
from student.schemas import StudentRegister
from student.models import Student
from auth_service import hash_password


def register_student(db: Session, student: StudentRegister):
    new_student = Student(
        name = student.name,
        email = student.email,
        id = student.id,
        location = student.location,
        institution = student.institution,
        password = hash_password(student.password)
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def get_students(db: Session):
    return db.query(Student).all()

def get_student(db: Session, id: str, institution: str):
    return db.query(Student).filter(Student.id == id, Student.institution == institution).first()

def delete_student(db: Session, id: str):
    student = db.query(Student).filter(Student.id == id).first()
    db.delete(student)
    db.commit()
    return student