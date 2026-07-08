import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "AI-First CRM HCP Module"
    # Note: Replace user:password@host:port/dbname with actual MySQL credentials
    DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:password@localhost:3306/hcp_db")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemma2-9b-it")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")

settings = Settings()
