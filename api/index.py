import sys
import os

# Ensure the parent directory is in the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
except Exception as e:
    print(f"Failed to import app: {e}")
    # Return a simple error app if import fails
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return jsonify({"error": "Application initialization failed", "details": str(e)}), 500
