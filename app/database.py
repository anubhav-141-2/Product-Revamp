from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL, SQLITE_DATABASE_URL


def _create_engine():
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Connected to MySQL database.")
        return engine
    except Exception:
        print("MySQL database unavailable - falling back to SQLite.")
        return create_engine(
            SQLITE_DATABASE_URL,
            connect_args={"check_same_thread": False},
        )


engine = _create_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
