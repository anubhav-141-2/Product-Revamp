from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import get_current_user
from app.services.referral_service import create_referral, get_application_referrals, update_referral, delete_referral
from app.schemas import ReferralCreate, ReferralUpdate, ReferralOut

router = APIRouter()
security = HTTPBearer()


def get_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    return get_current_user(db, credentials.credentials)


@router.post("/{application_id}")
def add_referral(application_id: int, data: ReferralCreate, user=Depends(get_user), db: Session = Depends(get_db)):
    ref = create_referral(db, application_id, user.user_id, data)
    return ReferralOut.model_validate(ref)


@router.get("/{application_id}")
def list_referrals(application_id: int, user=Depends(get_user), db: Session = Depends(get_db)):
    refs = get_application_referrals(db, application_id, user.user_id)
    return [ReferralOut.model_validate(r) for r in refs]


@router.put("/{application_id}/{referral_id}")
def edit_referral(application_id: int, referral_id: int, data: ReferralUpdate, user=Depends(get_user), db: Session = Depends(get_db)):
    ref = update_referral(db, referral_id, application_id, user.user_id, data)
    return ReferralOut.model_validate(ref)


@router.delete("/{application_id}/{referral_id}")
def remove_referral(application_id: int, referral_id: int, user=Depends(get_user), db: Session = Depends(get_db)):
    delete_referral(db, referral_id, application_id, user.user_id)
    return {"message": "Referral deleted successfully"}
