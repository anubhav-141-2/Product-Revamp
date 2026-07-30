import os
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import get_current_user
from app.services.resume_service import upload_resume, get_user_resumes, get_resume, get_resume_file_path, delete_resume
from app.schemas import ResumeOut

router = APIRouter()
security = HTTPBearer()


def get_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    return get_current_user(db, credentials.credentials)


@router.post("/upload")
def upload(user=Depends(get_user), db: Session = Depends(get_db), file: UploadFile = File(...)):
    resume = upload_resume(db, user.user_id, file)
    return ResumeOut.model_validate(resume)


@router.get("")
def list_resumes(user=Depends(get_user), db: Session = Depends(get_db)):
    resumes = get_user_resumes(db, user.user_id)
    return [ResumeOut.model_validate(r) for r in resumes]


@router.get("/{resume_id}/download")
def download(resume_id: int, user=Depends(get_user), db: Session = Depends(get_db)):
    resume = get_resume(db, resume_id, user.user_id)
    file_path = get_resume_file_path(resume)
    if not os.path.exists(file_path):
        from fastapi import HTTPException as HE
        raise HE(status_code=404, detail="File not found on disk")
    return FileResponse(file_path, filename=resume.original_name, media_type="application/octet-stream")


@router.delete("/{resume_id}")
def remove(resume_id: int, user=Depends(get_user), db: Session = Depends(get_db)):
    delete_resume(db, resume_id, user.user_id)
    return {"message": "Resume deleted successfully"}
