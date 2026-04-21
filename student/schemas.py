from pydantic import BaseModel, Field

class StudentRegister(BaseModel):
    name: str
    id: str
    email: str
    location: str
    institution: str
    password: str = Field(min_length=8, max_length=128)

class StudentLogin(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)

class StudentResponse(BaseModel):
    id: str
    name: str
    email: str

    class Config:
        from_attributes = True