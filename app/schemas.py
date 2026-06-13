from pydantic import BaseModel

class ResumeCreate(BaseModel):
    candidate_name: str
    resume_path: str
    skills: str
    ats_score: float


class JobCreate(BaseModel):
    title: str
    description: str
    skills: str


class MatchResultCreate(BaseModel):
    resume_id: int
    job_id: int
    match_score: float