"""
WSGI entry point for production deployment.
Use with Gunicorn: gunicorn wsgi:app
"""

from app import create_app
from app.scheduler import start_scheduler

app = create_app()

if __name__ == "__main__":
    start_scheduler()
    app.run()
