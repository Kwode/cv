from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()



class CVExtraction(BaseModel):
    skills: List[str] = Field(description="Technical and professional skills")
    experience_summary: List[str] = Field(description="2–3 sentence summaries of each job experience")
    projects: List[str] = Field(description="Notable projects (empty list if none)")



embeddings = OpenAIEmbeddings()

job_db = Chroma(
    collection_name="job_collection",
    persist_directory="./job_collection",
    embedding_function=embeddings
)


def build_cv_text(response: CVExtraction) -> str:
    skills = response.skills or []
    experience = response.experience_summary or []
    projects = response.projects or []

    return f"""
        Skills: {", ".join(skills)}

        Experience:
        {" ".join(experience)}

        Projects:
        {" ".join(projects)}
        """.strip()



def extract_cv_structured(text: str) -> CVExtraction:
    prompt = f"""
        You are a strict JSON generator.

        Extract structured data from the CV.

        Return ONLY valid JSON matching this schema:

        {{
            "skills": ["string"],
            "experience_summary": ["string"],
            "projects": ["string"]
        }}

        Rules:
        - No extra text
        - No explanations
        - No markdown

        CV:
        {text}
        """

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3
    ).with_structured_output(CVExtraction)

    response = llm.invoke(prompt)

    # Safety guard (prevents malformed outputs)
    if not isinstance(response, CVExtraction):
        response = CVExtraction(**response)

    return response



def recommend_jobs_for_cv(cv_text: str, top_k: int = 10):
    if job_db is None:
        raise RuntimeError("Job DB not initialized")

    results = job_db.similarity_search_with_score(
        query=cv_text,
        k=top_k
    )

    recommendations = []
    for doc, score in results:
        recommendations.append({
            "job_id": doc.metadata.get("job_id"),
            "company_id": doc.metadata.get("company_id"),
            "score": float(score),
            "job_text": doc.page_content
        })

    return recommendations


def rag_pdf(pages: str):
    structured = extract_cv_structured(pages)
    cv_text = build_cv_text(structured)
    return recommend_jobs_for_cv(cv_text)


def rag_doc(text: str):
    structured = extract_cv_structured(text)
    cv_text = build_cv_text(structured)
    return recommend_jobs_for_cv(cv_text)