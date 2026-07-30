from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from app.models import Application
from app.schemas import ApplicationCreate, ApplicationUpdate


def create_application(db: Session, user_id: int, data: ApplicationCreate) -> Application:
    app = Application(
        user_id=user_id,
        company_name=data.company_name,
        role=data.role,
        application_date=data.application_date,
        source=data.source,
        status=data.status or "Applied",
        notes=data.notes,
    )
    db.add(app)
    db.flush()
    db.refresh(app)
    return app


def get_user_applications(db: Session, user_id: int, search: Optional[str] = None, status_filter: Optional[str] = None):
    query = db.query(Application).filter(Application.user_id == user_id)
    if search:
        query = query.filter(Application.company_name.ilike(f"%{search}%"))
    if status_filter:
        query = query.filter(Application.status == status_filter)
    return query.order_by(Application.updated_at.desc()).all()


def get_application(db: Session, application_id: int, user_id: int) -> Application:
    app = db.query(Application).filter(
        Application.application_id == application_id,
        Application.user_id == user_id
    ).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


def update_application(db: Session, application_id: int, user_id: int, data: ApplicationUpdate) -> Application:
    app = get_application(db, application_id, user_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(app, key, value)
    db.flush()
    db.refresh(app)
    return app


def delete_application(db: Session, application_id: int, user_id: int):
    app = get_application(db, application_id, user_id)
    db.delete(app)
    db.flush()


def get_dashboard_stats(db: Session, user_id: int) -> dict:
    total = db.query(Application).filter(Application.user_id == user_id).count()
    in_interview = db.query(Application).filter(
        Application.user_id == user_id, Application.status == "Interview"
    ).count()
    offers = db.query(Application).filter(
        Application.user_id == user_id, Application.status == "Offer"
    ).count()
    rejections = db.query(Application).filter(
        Application.user_id == user_id, Application.status == "Rejected"
    ).count()
    return {
        "total_applications": total,
        "in_interview": in_interview,
        "offers": offers,
        "rejections": rejections,
    }