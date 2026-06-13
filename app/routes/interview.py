from fastapi import APIRouter
from pydantic import BaseModel
from app.ai.interview_generator import generate_questions

router = APIRouter()


class InterviewRequest(BaseModel):
    resume_text: str
    job_description: str = ""
    limit: int = 10


@router.post("/generate_questions")
def generate_interview_questions(payload: InterviewRequest):
    questions = generate_questions(
        payload.resume_text,
        payload.job_description,
        payload.limit,
    )
    return {
        "count": len(questions),
        "questions": questions,
    }
