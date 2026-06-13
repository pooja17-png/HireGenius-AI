from fastapi import APIRouter, UploadFile, File
import os
from app.ai.parser import extract_text
from app.ai.skills import extract_skills, SKILLS
from app.ai.ats import calculate_ats

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract text from the uploaded resume
    resume_text = extract_text(file_path)
    skills = extract_skills(resume_text)
    ats_score = calculate_ats(skills)

    # Skills the candidate does not yet have (from our known catalogue)
    missing_skills = [s for s in SKILLS if s not in skills]

    return {
        "message": "Resume uploaded successfully",
        "file_name": file.filename,
        "extracted_text": resume_text,
        "skills": skills,
        "all_skills": SKILLS,
        "missing_skills": missing_skills,
        "ats_score": ats_score,
    }
