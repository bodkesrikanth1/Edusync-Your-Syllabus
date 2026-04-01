"""
Vercel handler for EdusyncYourSyllabus Flask application.
Serves as the entry point for serverless function deployment.
"""

import sys
import os

# Ensure parent directory is in Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects one of: app / application / handler at module top-level
application = app
handler = app
