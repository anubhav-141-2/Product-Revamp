from fastapi import FastAPI
from app.database import engine, Base
from app.api import auth, applications, interviews

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CareerSprint API", version="1.0.0")

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(applications.router, prefix="/api/applications", tags=["Applications"])
app.include_router(interviews.router, prefix="/api/interviews", tags=["Interviews"])


@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "CareerSprint API is running"}