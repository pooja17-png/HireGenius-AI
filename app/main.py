from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.resume import router as resume_router
from app.routes.interview import router as interview_router
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HireGenius AI"
)

# Allow the Vite/React dev server (and any local origin) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    resume_router,
    tags=["Resume Upload"]
)

app.include_router(
    interview_router,
    tags=["Interview"]
)

@app.get("/")
def home():
    return{
        "message":"HireGenius AI running successfully"
    }
