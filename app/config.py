import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "careersprint")
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default-flask-secret-key")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")