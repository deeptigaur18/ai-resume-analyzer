from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from model import (
    calculate_match,
    calculate_ats_score,
    get_resume_feedback,
    get_matched_keywords
)
from data.jobs import jobs
import pdfplumber

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class ResumeRequest(BaseModel):
    resume: str


# Root route
@app.get("/")
def home():
    return {"message": "AI Resume Analyzer Running"}


# Core processing logic (used by both APIs)
def process_resume(text: str):
    results = []

    for job in jobs:
        job_text = (
            job["title"] + " " +
            job["description"] + " " +
            " ".join(job["skills"])
        )

        match_score = calculate_match(text, job_text)
        ats_score = calculate_ats_score(text, job_text)
        matched_keywords = get_matched_keywords(text, job_text)

        results.append({
            "job_title": job["title"],
            "match_score": match_score,
            "ats_score": ats_score,
            "matched_keywords": matched_keywords
        })

    # Sort and keep top 3 matches
    results = sorted(results, key=lambda x: x["match_score"], reverse=True)[:3]

    suggestions = get_resume_feedback(text)

    return {
        "results": results,
        "suggestions": suggestions
    }


# Text input endpoint
@app.post("/analyze")
def analyze_resume(req: ResumeRequest):
    if not req.resume or not req.resume.strip():
        return {"error": "Resume cannot be empty"}

    return process_resume(req.resume)


# PDF upload endpoint
@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    text = ""

    try:
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
    except Exception:
        return {"error": "Failed to read PDF"}

    if not text.strip():
        return {"error": "No text found in PDF"}

    return process_resume(text)
    }
