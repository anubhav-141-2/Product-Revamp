import os
import uuid
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.models import Resume

UPLOAD_DIR = "uploads/resumes"


def _ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_resume(db: Session, user_id: int, file: UploadFile) -> Resume:
    _ensure_upload_dir()
    filename = file.filename or "resume"
    ext = os.path.splitext(filename)[1] if "." in filename else ""
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    content = file.file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    resume = Resume(user_id=user_id, filename=unique_name, original_name=filename)
    db.add(resume)
    db.flush()
    db.refresh(resume)
    return resume


def get_user_resumes(db: Session, user_id: int):
    return db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.uploaded_at.desc()).all()


def get_resume(db: Session, resume_id: int, user_id: int) -> Resume:
    resume = db.query(Resume).filter(Resume.resume_id == resume_id, Resume.user_id == user_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


def get_resume_file_path(resume: Resume) -> str:
    return os.path.join(UPLOAD_DIR, resume.filename)


def delete_resume(db: Session, resume_id: int, user_id: int):
    resume = get_resume(db, resume_id, user_id)
    file_path = get_resume_file_path(resume)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.delete(resume)
    db.flush()
