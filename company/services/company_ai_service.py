from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
from typing import List

load_dotenv()

# =========================
# VECTOR DB
# =========================

embeddings = OpenAIEmbeddings()

vectorstore = Chroma(
    collection_name="job_collection",
    persist_directory="./job_collection",
    embedding_function=embeddings
)

# =========================
# HELPERS
# =========================

def safe_join(value):
    if not value:
        return ""
    if isinstance(value, list):
        return ", ".join(map(str, value))
    return str(value)


def format_job_text(job) -> str:
    return f"""
Role: {job.role}

Required Skills: {safe_join(job.required_skills)}

Preferred Skills: {safe_join(job.preferred_skills)}

Responsibilities: {safe_join(job.responsibilities)}

Experience Level: {job.experience_level}
""".strip()


# =========================
# STORE JOB
# =========================

def store_job_in_vector_db(job, job_id: str, company_id: str):

    job_text = format_job_text(job)

    vectorstore.add_texts(
        texts=[job_text],
        metadatas=[{
            "job_id": str(job_id),
            "company_id": str(company_id)
        }]
    )

    return {
        "status": "success",
        "job_id": job_id
    }