web: gunicorn wsgi:app
worker: python -c "from app import create_app; from app.scheduler import start_scheduler; app = create_app(); start_scheduler(); import time; [time.sleep(1) for _ in iter(int, 1)]"
