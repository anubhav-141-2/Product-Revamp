from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import register_user, authenticate_user, create_access_token, get_current_user
from app.schemas import UserCreate, UserLogin, UserOut

router = APIRouter()
security = HTTPBearer()


@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, data.name, data.email, data.password)
    token = create_access_token({"user_id": user.user_id, "email": user.email})
    return {"user": UserOut.model_validate(user), "token": token}


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    token = create_access_token({"user_id": user.user_id, "email": user.email})
    return {"user": UserOut.model_validate(user), "token": token}


@router.get("/me")
def get_me(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    user = get_current_user(db, credentials.credentials)
    return UserOut.model_validate(user)