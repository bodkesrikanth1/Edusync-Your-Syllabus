"""
Vercel handler for EdusyncYourSyllabus Flask application.
Serves as the entry point for serverless function deployment.
"""

import sys
import os
import traceback

# Ensure parent directory is in Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('vercel-handler')

try:
    logger.info("Attempting to import Flask app...")
    from app import app
    logger.info("✓ Flask app imported successfully")
    
except Exception as e:
    logger.error(f"✗ Failed to import Flask app: {e}")
    logger.error(traceback.format_exc())
    
    # Fallback: Create minimal error app
    from flask import Flask, jsonify, render_template_string
    
    app = Flask(__name__)
    error_message = str(e)
    error_trace = traceback.format_exc()
    
    @app.route('/')
    def error():
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Application Error</title>
            <style>
                body { font-family: Arial; background: #f5f5f5; margin: 0; padding: 20px; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
                h1 { color: #d32f2f; }
                .error-code { background: #f5f5f5; padding: 10px; border-radius: 4px; font-family: monospace; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>⚠️ Application Error</h1>
                <p>The application failed to initialize on Vercel.</p>
                <h3>Error Details:</h3>
                <div class="error-code">{{ error }}</div>
                <p><small>Check Vercel deployment logs for more information.</small></p>
            </div>
        </body>
        </html>
        ''', error=error_message)
    
    @app.route('/health')
    def health():
        return jsonify({
            "status": "error",
            "message": "Application initialization failed",
            "error": error_message
        }), 503
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found", "status": 404}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error", "status": 500}), 500


# Verify app is properly configured
@app.after_request
def set_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


logger.info("Handler initialization complete")

