from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model (runs once)
model = SentenceTransformer('all-MiniLM-L6-v2')


# 🔹 Match Score using embeddings
def calculate_match(resume, job_desc):
    embeddings = model.encode([resume, job_desc])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(round(score * 100, 2))


# 🔹 ATS Score (keyword-based simple logic)
def calculate_ats_score(resume, job_desc):
    resume_words = set(resume.lower().split())
    job_words = set(job_desc.lower().split())

    matched = resume_words.intersection(job_words)

    if len(job_words) == 0:
        return 0

    score = len(matched) / len(job_words) * 100
    return float(round(score, 2))


# 🔹 AI Resume Feedback (rule-based for now)
def get_resume_feedback(resume):
    suggestions = []

    resume_lower = resume.lower()

    if "project" not in resume_lower:
        suggestions.append("Add projects to showcase practical experience.")

    if "experience" not in resume_lower:
        suggestions.append("Mention work experience or internships.")

    if "skills" not in resume_lower:
        suggestions.append("Include a dedicated skills section.")

    if len(resume.split()) < 50:
        suggestions.append("Resume is too short. Add more details.")

    if "python" not in resume_lower:
        suggestions.append("Consider adding Python if relevant.")

    if "machine learning" not in resume_lower:
        suggestions.append("Add Machine Learning if applying for AI roles.")

    if not suggestions:
        suggestions.append("Your resume looks strong! 🚀")

    return suggestions