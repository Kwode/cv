from fastapi import FastAPI
from student.api import student_auth, file_upload
from company.api import company_auth, job_openings
from student.models import StudentBase
from company.models import CompanyBase
from database_config import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
def startup():
    StudentBase.metadata.create_all(bind = engine)
    CompanyBase.metadata.create_all(bind = engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(student_auth.router)
app.include_router(company_auth.router)
app.include_router(job_openings.router)
app.include_router(file_upload.router)
