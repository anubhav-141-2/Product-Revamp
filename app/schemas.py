from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    user_id: int
    name: str
    email: str

    model_config = {"from_attributes": True}


class ApplicationCreate(BaseModel):
    company_name: str
    role: str
    application_date: date
    source: Optional[str] = None
    status: Optional[str] = "Applied"
    notes: Optional[str] = None

    model_config = {"from_attributes": True}


class ApplicationUpdate(BaseModel):
    company_name: Optional[str] = None
    role: Optional[str] = None
    application_date: Optional[date] = None
    source: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class ApplicationOut(BaseModel):
    application_id: int
    user_id: int
    company_name: str
    role: str
    application_date: date
    source: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class InterviewRoundCreate(BaseModel):
    round_number: int
    round_type: Optional[str] = None
    interview_date: Optional[date] = None
    result: Optional[str] = "Awaiting Result"
    notes: Optional[str] = None

    model_config = {"from_attributes": True}


class InterviewRoundUpdate(BaseModel):
    round_number: Optional[int] = None
    round_type: Optional[str] = None
    interview_date: Optional[date] = None
    result: Optional[str] = None
    notes: Optional[str] = None


class InterviewRoundOut(BaseModel):
    round_id: int
    application_id: int
    round_number: int
    round_type: Optional[str] = None
    interview_date: Optional[date] = None
    result: str
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class DashboardStats(BaseModel):
    total_applications: int
    in_interview: int
    offers: int
    rejections: int