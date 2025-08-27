import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: str = os.getenv("DB_PORT", "5432")
    db_name: str = os.getenv("DB_NAME", "sentinel_one_lite")
    db_user: str = os.getenv("DB_USER", "solite_user")
    db_password: str = os.getenv("DB_PASSWORD", "password")
    collect_interval_sec: int = int(os.getenv("COLLECT_INTERVAL_SEC", "10"))

settings = Settings()
