import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET", "dev")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "sri1")
    DB_NAME = os.getenv("DB_NAME", "edusync")
    YT_API_KEY = os.getenv("YT_API_KEY", "AIzaSyBx7msMyucu5ATutlMT91Ace7RaYuF-aWM")
