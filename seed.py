from datetime import date
from app.database import SessionLocal, engine, Base
from app.models import User, Application, InterviewRound
from app.services.auth_service import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    existing = db.query(User).filter(User.email == "alice@example.com").first()
    if existing:
        print("Database already seeded.")
        exit(0)

    alice = User(name="Alice Johnson", email="alice@example.com", password=hash_password("password123"))
    bob = User(name="Bob Smith", email="bob@example.com", password=hash_password("password123"))
    db.add_all([alice, bob])
    db.flush()

    apps = [
        Application(user_id=alice.user_id, company_name="Google", role="Software Engineer Intern", application_date=date(2026, 6, 1), source="LinkedIn", status="Interview", notes="Referred by a friend."),
        Application(user_id=alice.user_id, company_name="Microsoft", role="SWE Intern", application_date=date(2026, 6, 5), source="Company site", status="OA Scheduled"),
        Application(user_id=alice.user_id, company_name="Amazon", role="SDE Intern", application_date=date(2026, 5, 20), source="Campus placement", status="Rejected", notes="Rejected after OA."),
        Application(user_id=alice.user_id, company_name="Stripe", role="Backend Intern", application_date=date(2026, 6, 10), source="LinkedIn", status="Applied"),
        Application(user_id=alice.user_id, company_name="Meta", role="Frontend Intern", application_date=date(2026, 6, 3), source="Referral", status="Offer", notes="Got the offer!"),
        Application(user_id=bob.user_id, company_name="Apple", role="ML Intern", application_date=date(2026, 6, 7), source="LinkedIn", status="Interview"),
        Application(user_id=bob.user_id, company_name="Netflix", role="Platform Eng Intern", application_date=date(2026, 5, 28), source="Company site", status="OA Completed"),
        Application(user_id=bob.user_id, company_name="Spotify", role="Data Eng Intern", application_date=date(2026, 6, 12), source="LinkedIn", status="Applied"),
    ]
    db.add_all(apps)
    db.flush()

    rounds = [
        InterviewRound(application_id=apps[0].application_id, round_number=1, round_type="Technical Phone Screen", interview_date=date(2026, 6, 15), result="Selected"),
        InterviewRound(application_id=apps[0].application_id, round_number=2, round_type="On-site (4 rounds)", interview_date=date(2026, 6, 22), result="Awaiting Result"),
        InterviewRound(application_id=apps[4].application_id, round_number=1, round_type="Technical Screen", interview_date=date(2026, 6, 12), result="Selected"),
        InterviewRound(application_id=apps[4].application_id, round_number=2, round_type="HM Round", interview_date=date(2026, 6, 18), result="Selected"),
        InterviewRound(application_id=apps[5].application_id, round_number=1, round_type="Phone Screen", interview_date=date(2026, 6, 20), result="Awaiting Result"),
    ]
    db.add_all(rounds)
    db.commit()

    print("Database seeded successfully!")
    print()
    print("Users:")
    print("  alice@example.com / password123")
    print("  bob@example.com   / password123")

finally:
    db.close()