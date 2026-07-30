from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import get_current_user
from app.services.interview_service import (
    create_interview_round, get_interview_rounds,
    update_interview_round, delete_interview_round
)
from app.schemas import InterviewRoundCreate, InterviewRoundUpdate, InterviewRoundOut

router = APIRouter()
security = HTTPBearer()


def get_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    return get_current_user(db, credentials.credentials)


@router.post("/{application_id}")
def add_interview_round(
    application_id: int, data: InterviewRoundCreate,
    user=Depends(get_user), db: Session = Depends(get_db)
):
    irc = create_interview_round(db, application_id, user.user_id, data)
    return InterviewRoundOut.model_validate(irc)


@router.get("/{application_id}")
def list_interview_rounds(application_id: int, user=Depends(get_user), db: Session = Depends(get_db)):
    rounds = get_interview_rounds(db, application_id, user.user_id)
    return [InterviewRoundOut.model_validate(r) for r in rounds]


@router.put("/{application_id}/{round_id}")
def edit_interview_round(
    application_id: int, round_id: int, data: InterviewRoundUpdate,
    user=Depends(get_user), db: Session = Depends(get_db)
):
    irc = update_interview_round(db, round_id, application_id, user.user_id, data)
    return InterviewRoundOut.model_validate(irc)


@router.delete("/{application_id}/{round_id}")
def remove_interview_round(
    application_id: int, round_id: int,
    user=Depends(get_user), db: Session = Depends(get_db)
):
    delete_interview_round(db, round_id, application_id, user.user_id)
    return {"message": "Interview round deleted successfully"}