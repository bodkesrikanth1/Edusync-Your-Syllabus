import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Use a default secret for local dev, but should be set in production
    SECRET_KEY = os.getenv("FLASK_SECRET", "dev-insecure-key-change-in-production")
    
    # Database configuration
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "edusync")
    
    # YouTube API key
    YT_API_KEY = os.getenv("YT_API_KEY", "")


