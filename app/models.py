from sqlalchemy import Column, Integer, String, Date, Text, Enum, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship as orm_relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    applications = orm_relationship("Application", back_populates="user", cascade="all, delete-orphan")
    resumes = orm_relationship("Resume", back_populates="user", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"

    application_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    company_name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    application_date = Column(Date, nullable=False)
    source = Column(String(255))
    status = Column(Enum("Applied", "OA Scheduled", "OA Completed", "Interview", "Offer", "Rejected", "Withdrawn"), default="Applied")
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = orm_relationship("User", back_populates="applications")
    interview_rounds = orm_relationship("InterviewRound", back_populates="application", cascade="all, delete-orphan")
    referrals = orm_relationship("Referral", back_populates="application", cascade="all, delete-orphan")


class InterviewRound(Base):
    __tablename__ = "interview_rounds"

    round_id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("applications.application_id", ondelete="CASCADE"), nullable=False)
    round_number = Column(Integer, nullable=False)
    round_type = Column(String(255))
    interview_date = Column(Date)
    result = Column(Enum("Selected", "Rejected", "Awaiting Result", "On Hold"), default="Awaiting Result")
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    application = orm_relationship("Application", back_populates="interview_rounds")


class Resume(Base):
    __tablename__ = "resumes"

    resume_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    user = orm_relationship("User", back_populates="resumes")


class Referral(Base):
    __tablename__ = "referrals"

    referral_id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("applications.application_id", ondelete="CASCADE"), nullable=False)
    referrer_name = Column(String(255), nullable=False)
    referrer_email = Column(String(255))
    relationship = Column(String(255))
    date_referred = Column(Date)
    status = Column(Enum("Pending", "Confirmed", "Not Responded", "Declined"), default="Pending")
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    application = orm_relationship("Application", back_populates="referrals")