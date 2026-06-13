from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class Resume(Base):
    __tablename__="resume"

    id = Column(Integer, primary_key=True, index=True)

    candidate_name = Column(String)
    resume_path = Column(String)
    skills = Column(String)
    ats_score = Column(Float)

class Job(Base):

    __tablename__="job"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    description = Column(String)
    skills = Column(String)

class MatchResult(Base):

    __tablename__="match_result"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(Integer, ForeignKey("resume.id"))
    job_id = Column(Integer, ForeignKey("job.id"))
   
    match_score = Column(Float)