from sqlalchemy import String, Column, Text, ARRAY, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import uuid

CompanyBase = declarative_base()


class Company(CompanyBase):
    __tablename__ = "company"

    cac = Column(String, primary_key=True, index=True)

    name = Column(String, nullable=False, index=True)

    email = Column(String, nullable=False, index=True)

    location = Column(String, nullable=False)

    industry = Column(String, nullable=True)

    password = Column(String, nullable=False)

    description = Column(Text, nullable=True)

    jobs = relationship("Job", back_populates="company")


class Job(CompanyBase):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    company_id = Column(String, ForeignKey("company.cac"), index=True, nullable=False)

    role = Column(String, nullable=False)

    required_skills = Column(ARRAY(String), nullable=False)

    preferred_skills = Column(ARRAY(String), nullable=True)

    responsibilities = Column(ARRAY(String), nullable=False)

    experience_level = Column(String, nullable=False)

    company = relationship("Company", back_populates="jobs")