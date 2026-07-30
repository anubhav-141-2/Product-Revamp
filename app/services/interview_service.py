from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import InterviewRound, Application
from app.schemas import InterviewRoundCreate, InterviewRoundUpdate


def create_interview_round(db: Session, application_id: int, user_id: int, data: InterviewRoundCreate) -> InterviewRound:
    app = db.query(Application).filter(
        Application.application_id == application_id,
        Application.user_id == user_id
    ).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if app.status != "Interview":
        raise HTTPException(status_code=400, detail="Interview rounds can only be added when status is Interview")
    irc = InterviewRound(
        application_id=application_id,
        round_number=data.round_number,
        round_type=data.round_type,
        interview_date=data.interview_date,
        result=data.result or "Awaiting Result",
        notes=data.notes,
    )
    db.add(irc)
    db.flush()
    db.refresh(irc)
    return irc


def get_interview_rounds(db: Session, application_id: int, user_id: int):
    app = db.query(Application).filter(
        Application.application_id == application_id,
        Application.user_id == user_id
    ).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return db.query(InterviewRound).filter(
        InterviewRound.application_id == application_id
    ).order_by(InterviewRound.round_number).all()


def update_interview_round(db: Session, round_id: int, application_id: int, user_id: int, data: InterviewRoundUpdate) -> InterviewRound:
    app = db.query(Application).filter(
        Application.application_id == application_id,
        Application.user_id == user_id
    ).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    irc = db.query(InterviewRound).filter(
        InterviewRound.round_id == round_id,
        InterviewRound.application_id == application_id
    ).first()
    if not irc:
        raise HTTPException(status_code=404, detail="Interview round not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(irc, key, value)
    db.flush()
    db.refresh(irc)
    return irc


def delete_interview_round(db: Session, round_id: int, application_id: int, user_id: int):
    app = db.query(Application).filter(
        Application.application_id == application_id,
        Application.user_id == user_id
    ).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    irc = db.query(InterviewRound).filter(
        InterviewRound.round_id == round_id,
        InterviewRound.application_id == application_id
    ).first()
    if not irc:
        raise HTTPException(status_code=404, detail="Interview round not found")
    db.delete(irc)
    db.flush()