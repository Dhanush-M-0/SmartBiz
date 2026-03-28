"""
run.py — Entry point for SmartBiz Web Application.
Starts the Flask server and background scheduler.
"""

from app import create_app
from app.scheduler import start_scheduler

app = create_app()

if __name__ == "__main__":
    start_scheduler()
    print("🚀 SmartBiz Web App running at http://127.0.0.1:5000")
    app.run(debug=app.config["DEBUG"], port=5000)
