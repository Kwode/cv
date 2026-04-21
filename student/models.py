from sqlalchemy import String, Column
from sqlalchemy.orm import declarative_base

StudentBase = declarative_base()

class Student(StudentBase):
    __tablename__ = 'student'
    id = Column(String, index= True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    location = Column(String, nullable=False)
    institution = Column(String, nullable=False)
    password = Column(String, nullable=False)