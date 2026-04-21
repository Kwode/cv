from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from PyPDF2 import PdfReader
from io import BytesIO
from docx import Document
from student.services.student_ai_service import rag_doc, rag_pdf
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.post('/upload')
async def upload_file(user: str = Depends(get_current_user), file: UploadFile = File(...)):

    if user["role"] != "student":
        raise HTTPException(status_code=403, detail="Not Authorized")

    if file.content_type == "application/pdf":

        file_bytes = await file.read()
        pdf = PdfReader(BytesIO(file_bytes))

        # Extract text from each page
        text_pages = " ".join([page.extract_text() for page in pdf.pages])

        return rag_pdf(text_pages)
    
    elif file.filename.endswith('.docx'):

        content = await file.read()
        
        docx = Document(BytesIO(content))

        docx_text = " ".join([para.text for para in docx.paragraphs])

        return {"doc": docx_text}
        
    raise HTTPException(status_code=415, detail='Upload docx or pdf files only')

# @router.post('/query/pdf')
# async def query_pdf(prompt: str = Form(...)):
#     return {"response": pdf_response(prompt)}

# @router.post('/query/doc')
# async def query_doc(prompt: str = Form(...)):
#     return {"response": doc_response(prompt)}



