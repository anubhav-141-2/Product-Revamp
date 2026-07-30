from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services.auth_service import get_current_user
from app.services.application_service import (
    create_application, get_user_applications, get_application,
    update_application, delete_application, get_dashboard_stats
)
from app.schemas import ApplicationCreate, ApplicationUpdate, ApplicationOut, DashboardStats

router = APIRouter()
security = HTTPBearer()


def get_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    return get_current_user(db, credentials.credentials)


@router.post("")
def add_application(data: ApplicationCreate, user=Depends(get_user), db: Session = Depends(get_db)):
    app = create_application(db, user.user_id, data)
    return ApplicationOut.model_validate(app)


@router.get("")
def list_applications(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    user=Depends(get_user),
    db: Session = Depends(get_db)
):
    apps = get_user_applications(db, user.user_id, search, status)
    return [ApplicationOut.model_validate(a) for a in apps]


@router.get("/dashboard")
def dashboard(user=Depends(get_user), db: Session = Depends(get_db)):
    return get_dashboard_stats(db, user.user_id)


@router.get("/{application_id}")
def view_application(application_id: int, user=Depends(get_user), db: Session = Depends(get_db)):
    app = get_application(db, application_id, user.user_id)
    return ApplicationOut.model_validate(app)


@router.put("/{application_id}")
def edit_application(application_id: int, data: ApplicationUpdate, user=Depends(get_user), db: Session = Depends(get_db)):
    app = update_application(db, application_id, user.user_id, data)
    return ApplicationOut.model_validate(app)


@router.delete("/{application_id}")
def remove_application(application_id: int, user=Depends(get_user), db: Session = Depends(get_db)):
    delete_application(db, application_id, user.user_id)
    return {"message": "Application deleted successfully"}