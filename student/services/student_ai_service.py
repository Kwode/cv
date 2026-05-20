from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
from sqlalchemy.orm import Session
from company.models import Company

load_dotenv()

# =========================
# MODELS
# =========================

class CVExtraction(BaseModel):
    skills: List[str]
    experience_summary: List[str]
    projects: List[str]


class JobExtraction(BaseModel):
    role: str
    required_skills: List[str]
    preferred_skills: List[str]
    responsibilities: List[str]
    experience_level: str


class SkillGap(BaseModel):
    missing_required: List[str]
    missing_preferred: List[str]
    recommendations: List[str]
    match_quality: str


# =========================
# EMBEDDINGS + VECTOR DB
# =========================

embeddings = OpenAIEmbeddings()

job_db = Chroma(
    collection_name="job_collection",
    persist_directory="./job_collection",
    embedding_function=embeddings
)

# =========================
# CV PROCESSING
# =========================

def build_cv_text(response: CVExtraction) -> str:
    return f"""
Skills: {", ".join(response.skills)}

Experience:
{" ".join(response.experience_summary)}

Projects:
{" ".join(response.projects)}
""".strip()


def extract_cv_structured(text: str) -> CVExtraction:

    prompt = f"""
Extract structured data from this CV.

Return JSON:
{{
  "skills": ["..."],
  "experience_summary": ["..."],
  "projects": ["..."]
}}

CV:
{text}
"""

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2
    ).with_structured_output(CVExtraction)

    return llm.invoke(prompt)


# =========================
# JOB GAP ANALYSIS (GPT)
# =========================

def analyze_skill_gap(cv_skills, required, preferred):

    prompt = f"""
You are a career advisor.

Compare CV skills with job requirements.

CV Skills:
{cv_skills}

Required Skills:
{required}

Preferred Skills:
{preferred}

Return:
- missing_required
- missing_preferred
- recommendations
- match_quality (Poor / Partial / Good / Excellent)
"""

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2
    ).with_structured_output(SkillGap)

    return llm.invoke(prompt)


# =========================
# JOB SEARCH
# =========================

def recommend_jobs_for_cv(db: Session, structured_cv: CVExtraction, cv_text: str, top_k: int = 10):

    results = job_db.similarity_search_with_score(
        query=cv_text,
        k=top_k
    )

    recommendations = []

    for doc, score in results:

        job_id = doc.metadata.get("job_id")
        company_id = doc.metadata.get("company_id")

        # company lookup
        company = db.query(Company).filter(
            Company.cac == company_id
        ).first()

        # job text parsing (light GPT-based extraction)
        job_prompt = f"""
Extract JSON:
{{
  "required_skills": [],
  "preferred_skills": []
}}

JOB:
{doc.page_content}
"""

        job_llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        ).with_structured_output(JobExtraction)

        job_structured = job_llm.invoke(job_prompt)

        # GAP ANALYSIS
        gap = analyze_skill_gap(
            structured_cv.skills,
            job_structured.required_skills,
            job_structured.preferred_skills
        )

        recommendations.append({
            "job_id": job_id,
            "score": float(score),
            "job_text": doc.page_content,

            "match_quality": gap.match_quality,
            "missing_required_skills": gap.missing_required,
            "missing_preferred_skills": gap.missing_preferred,
            "recommendations": gap.recommendations,

            "company": {
                "id": company.cac if company else None,
                "name": company.name if company else None,
                "location": company.location if company else None,
                "industry": company.industry if company else None
            }
        })

    return recommendations


# =========================
# PIPELINE ENTRYPOINT
# =========================

def rag_pdf(db: Session, pages: str):

    structured = extract_cv_structured(pages)

    cv_text = build_cv_text(structured)

    return recommend_jobs_for_cv(db, structured, cv_text)