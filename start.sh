#!/bin/bash
# Hugging Face Spaces startup script

# Set environment defaults if not already set
export FLASK_APP=${FLASK_APP:-app.py}
export FLASK_ENV=${FLASK_ENV:-production}
export PORT=${PORT:-7860}

# Install dependencies if needed
pip install --upgrade -r requirements.txt

# Run Flask with gunicorn for production
gunicorn --bind 0.0.0.0:${PORT} --workers 4 --worker-class sync --timeout 60 app:app
