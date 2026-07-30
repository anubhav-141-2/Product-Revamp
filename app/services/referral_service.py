from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Referral, Application
from app.schemas import ReferralCreate, ReferralUpdate


def create_referral(db: Session, application_id: int, user_id: int, data: ReferralCreate) -> Referral:
    app = db.query(Application).filter(Application.application_id == application_id, Application.user_id == user_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    ref = Referral(
        application_id=application_id,
        referrer_name=data.referrer_name,
        referrer_email=data.referrer_email,
        relationship=data.relationship,
        date_referred=data.date_referred,
        status=data.status or "Pending",
        notes=data.notes,
    )
    db.add(ref)
    db.flush()
    db.refresh(ref)
    return ref


def get_application_referrals(db: Session, application_id: int, user_id: int):
    app = db.query(Application).filter(Application.application_id == application_id, Application.user_id == user_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return db.query(Referral).filter(Referral.application_id == application_id).order_by(Referral.created_at.desc()).all()


def get_referral(db: Session, referral_id: int, application_id: int, user_id: int) -> Referral:
    app = db.query(Application).filter(Application.application_id == application_id, Application.user_id == user_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    ref = db.query(Referral).filter(Referral.referral_id == referral_id, Referral.application_id == application_id).first()
    if not ref:
        raise HTTPException(status_code=404, detail="Referral not found")
    return ref


def update_referral(db: Session, referral_id: int, application_id: int, user_id: int, data: ReferralUpdate) -> Referral:
    ref = get_referral(db, referral_id, application_id, user_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ref, key, value)
    db.flush()
    db.refresh(ref)
    return ref


def delete_referral(db: Session, referral_id: int, application_id: int, user_id: int):
    ref = get_referral(db, referral_id, application_id, user_id)
    db.delete(ref)
    db.flush()
