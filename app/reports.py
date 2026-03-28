"""
reports.py — Auto-generates Excel and CSV reports
for task performance and employee summaries.
"""

import os
import pandas as pd
from datetime import datetime
from .models import get_all_tasks, get_all_employees, log_report
from .config import Config


def _ensure_output_dir():
    os.makedirs(Config.REPORTS_OUTPUT_DIR, exist_ok=True)


def generate_task_report() -> str:
    """Generate an Excel report of all tasks with employee info."""
    _ensure_output_dir()
    tasks = get_all_tasks()
    if not tasks:
        return None

    rows = []
    for t in tasks:
        emp = t.get("employees") or {}
        rows.append({
            "Task Title":    t["title"],
            "Description":   t.get("description", ""),
            "Assigned To":   emp.get("name", "Unassigned"),
            "Department":    emp.get("department", "—"),
            "Priority":      t["priority"],
            "Status":        t["status"],
            "Deadline":      t["deadline"],
            "Created At":    t["created_at"][:10],
        })

    df = pd.DataFrame(rows)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"task_report_{timestamp}.xlsx"
    file_path = os.path.join(Config.REPORTS_OUTPUT_DIR, file_name)

    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="All Tasks")

        # Summary sheet
        summary = df.groupby("Status").size().reset_index(name="Count")
        summary.to_excel(writer, index=False, sheet_name="Status Summary")

        # Priority breakdown
        priority = df.groupby("Priority").size().reset_index(name="Count")
        priority.to_excel(writer, index=False, sheet_name="Priority Breakdown")

    log_report("Task Report", file_name)
    return file_path


def generate_employee_performance_report() -> str:
    """Generate a CSV report showing task completion per employee."""
    _ensure_output_dir()
    tasks = get_all_tasks()
    employees = get_all_employees()

    emp_map = {e["id"]: e["name"] for e in employees}
    rows = []

    for emp in employees:
        emp_tasks = [t for t in tasks if t.get("assigned_to") == emp["id"]]
        total = len(emp_tasks)
        done = sum(1 for t in emp_tasks if t["status"] == "Done")
        pending = sum(1 for t in emp_tasks if t["status"] == "Pending")
        in_progress = sum(1 for t in emp_tasks if t["status"] == "In Progress")
        completion_rate = round((done / total * 100), 1) if total > 0 else 0.0

        rows.append({
            "Employee":          emp["name"],
            "Department":        emp["department"],
            "Total Tasks":       total,
            "Done":              done,
            "In Progress":       in_progress,
            "Pending":           pending,
            "Completion Rate %": completion_rate,
        })

    df = pd.DataFrame(rows).sort_values("Completion Rate %", ascending=False)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"employee_performance_{timestamp}.csv"
    file_path = os.path.join(Config.REPORTS_OUTPUT_DIR, file_name)
    df.to_csv(file_path, index=False)

    log_report("Employee Performance", file_name)
    return file_path
