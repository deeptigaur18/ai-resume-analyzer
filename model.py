from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

# ✅ Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')


# 🔹 Clean text (important for ATS)
def clean_text(text):
    return set(re.findall(r'\b\w+\b', text.lower()))


# 🔹 Match Score (semantic AI)
def calculate_match(resume, job_desc):
    embeddings = model.encode([resume, job_desc])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(round(score * 100, 2))


# 🔹 ATS Score (improved)
def calculate_ats_score(resume, job_desc):
    resume_words = clean_text(resume)
    job_words = clean_text(job_desc)

    matched = resume_words.intersection(job_words)

    if len(job_words) == 0:
        return 0

    score = (len(matched) / len(job_words)) * 100

    # 🔥 bonus for important keywords
    important_keywords = ["python", "machine", "learning", "fastapi", "api"]
    bonus = sum(1 for word in important_keywords if word in resume_words)

    score += bonus * 2

    return float(round(min(score, 100), 2))


# 🔹 Matched Keywords (NEW FEATURE 🔥)
def get_matched_keywords(resume, job_desc):
    resume_words = clean_text(resume)
    job_words = clean_text(job_desc)
    return list(resume_words.intersection(job_words))


# 🔹 Resume Feedback (improved)
def get_resume_feedback(resume):
    suggestions = []
    resume_lower = resume.lower()

    if "project" not in resume_lower:
        suggestions.append("Add 2–3 strong projects with technologies used.")

    if "experience" not in resume_lower:
        suggestions.append("Include internships or real-world experience.")

    if "skills" not in resume_lower:
        suggestions.append("Add a technical skills section.")

    if "github" not in resume_lower:
        suggestions.append("Include your GitHub or portfolio link.")

    if len(resume.split()) < 80:
        suggestions.append("Resume is too short. Add more details.")

    if "fastapi" not in resume_lower:
        suggestions.append("Mention backend frameworks like FastAPI.")

    if "machine learning" not in resume_lower:
        suggestions.append("Add Machine Learning if targeting AI roles.")

    if not suggestions:
        suggestions.append("Your resume looks strong! 🚀")

    return suggestions
