from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from PyPDF2 import PdfReader
from io import BytesIO
from docx import Document
from student.services.student_ai_service import rag_pdf
from dependencies.get_current_user import get_current_user
from sqlalchemy.orm import Session
from dependencies.get_db import get_db

router = APIRouter()

@router.post('/upload')
async def upload_file_endpoint(db: Session = Depends(get_db),user: str = Depends(get_current_user), file: UploadFile = File(...)):

    if user["role"] != "student":
        raise HTTPException(status_code=403, detail="Not Authorized")

    if file.content_type == "application/pdf":

        file_bytes = await file.read()
        pdf = PdfReader(BytesIO(file_bytes))

        # Extract text from each page
        text_pages = " ".join([page.extract_text() for page in pdf.pages])

        return rag_pdf(db, text_pages)
        
    raise HTTPException(status_code=415, detail='Upload pdf files only')




