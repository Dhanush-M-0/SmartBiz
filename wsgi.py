"""
Production WSGI entry point for Gunicorn.
Use this to run the application in production:
  gunicorn wsgi:app
"""

import os
import sys

# Ensure the app module is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    # This should not be used in production
    # For development, use: python run.py
    # For production, use: gunicorn wsgi:app
    print("WARNING: Running Flask development server. Use 'gunicorn wsgi:app' in production.")
    app.run(debug=app.config["DEBUG"], port=5000)
