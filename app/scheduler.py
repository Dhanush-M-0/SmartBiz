"""
scheduler.py — Runs background jobs automatically:
  • Every day: check overdue tasks and send alerts
  • Every Monday: auto-generate weekly reports
"""

import schedule
import time
import threading
from .models import get_overdue_tasks
from .notifier import notify_overdue_tasks
from .reports import generate_task_report, generate_employee_performance_report


def job_check_overdue():
    print("[Scheduler] Checking for overdue tasks...")
    overdue = get_overdue_tasks()
    if overdue:
        sent = notify_overdue_tasks(overdue)
        print(f"[Scheduler] Found {len(overdue)} overdue tasks. Sent {sent} alert(s).")
    else:
        print("[Scheduler] No overdue tasks. All good!")


def job_weekly_report():
    print("[Scheduler] Generating weekly reports...")
    task_file = generate_task_report()
    perf_file = generate_employee_performance_report()
    print(f"[Scheduler] Reports saved: {task_file}, {perf_file}")


def start_scheduler():
    """Set up scheduled jobs and run in a background thread."""
    schedule.every().day.at("09:00").do(job_check_overdue)
    schedule.every().monday.at("08:00").do(job_weekly_report)

    def run():
        print("[Scheduler] Background scheduler started.")
        while True:
            schedule.run_pending()
            time.sleep(60)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
