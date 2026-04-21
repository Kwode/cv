from pydantic import BaseModel, Field
from typing import Optional, List


class CompanyRegister(BaseModel):
    cac: str
    name: str
    email: str
    location: str
    industry: Optional[str] = None
    description: Optional[str] = None

    password: str = Field(min_length=8, max_length=128)

class CompanyLogin(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)

class CompanyResponse(BaseModel):
    cac: str
    name: str
    email: str
    location: str
    industry: Optional[str] = None
    description: Optional[str] = None

class JobCreate(BaseModel):
    role: str
    required_skills: List[str]
    preferred_skills: Optional[List[str]] = []
    responsibilities: List[str]
    experience_level: str

class JobResponse(BaseModel):
    id: str
    company_id: str
    role: str
    required_skills: List[str]
    preferred_skills: List[str]
    responsibilities: List[str]
    experience_level: str

    class Config:
        from_attributes = True