"""
WSGI entry point for Vercel deployment.
This file can be used instead of api/index.py if needed.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app
try:
    from app import app
    
    # For Vercel, we need to export the app object directly
    application = app  # Some servers look for 'application' instead of 'app'
    
except Exception as e:
    import traceback
    print(f"ERROR: Failed to import app: {e}")
    traceback.print_exc()
    
    # Fallback error app
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    application = app
    
    @app.route('/')
    def error():
        return jsonify({
            "error": "Application initialization failed",
            "details": str(e)
        }), 500
    
    @app.route('/health')
    def health():
        return jsonify({
            "status": "error",
            "error": "App not initialized",
            "details": str(e)
        }), 503


if __name__ == '__main__':
    app.run()
