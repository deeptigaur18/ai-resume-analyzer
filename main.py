from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from model import calculate_match, calculate_ats_score, get_resume_feedback
from data.jobs import jobs
import pdfplumber

app = FastAPI()

# ✅ CORS FIX (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request schema
class ResumeRequest(BaseModel):
    resume: str


# ✅ Home route
@app.get("/")
def home():
    return {"message": "AI Resume Analyzer Running 🚀"}


# 🔹 TEXT INPUT API
@app.post("/analyze")
def analyze_resume(req: ResumeRequest):

    if not req.resume.strip():
        return {"error": "Resume cannot be empty"}

    results = []

    for job in jobs:
        match_score = calculate_match(req.resume, job)
        ats_score = calculate_ats_score(req.resume, job)

        results.append({
            "job": job,
            "match_score": match_score,
            "ats_score": ats_score
        })

    # 🔥 Show only TOP 3
    results = sorted(results, key=lambda x: x["match_score"], reverse=True)[:3]

    suggestions = get_resume_feedback(req.resume)

    return {
        "results": results,
        "suggestions": suggestions
    }


# 🔹 PDF UPLOAD API
@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    text = ""

    try:
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception:
        return {"error": "Failed to read PDF"}

    if not text.strip():
        return {"error": "No text found in PDF"}

    results = []

    for job in jobs:
        match_score = calculate_match(text, job)
        ats_score = calculate_ats_score(text, job)

        results.append({
            "job": job,
            "match_score": match_score,
            "ats_score": ats_score
        })

    # 🔥 Show only TOP 3
    results = sorted(results, key=lambda x: x["match_score"], reverse=True)[:3]

    suggestions = get_resume_feedback(text)

    return {
        "results": results,
        "suggestions": suggestions
    }