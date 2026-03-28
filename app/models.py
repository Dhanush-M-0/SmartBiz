"""
models.py — All Supabase DB operations for SmartBiz.
Covers Employees, Tasks, and Reports Log.
"""

from .database import get_client
from datetime import date


# ─── EMPLOYEES ────────────────────────────────────────────────

def get_all_employees():
    res = get_client().table("employees").select("*").order("created_at", desc=False).execute()
    return res.data

def get_employee_by_id(emp_id: str):
    res = get_client().table("employees").select("*").eq("id", emp_id).single().execute()
    return res.data

def add_employee(name: str, email: str, department: str):
    res = get_client().table("employees").insert({
        "name": name,
        "email": email,
        "department": department
    }).execute()
    return res.data

def delete_employee(emp_id: str):
    res = get_client().table("employees").delete().eq("id", emp_id).execute()
    return res.data


# ─── TASKS ────────────────────────────────────────────────────

def get_all_tasks():
    res = (
        get_client()
        .table("tasks")
        .select("*, employees(name, email, department)")
        .order("deadline", desc=False)
        .execute()
    )
    return res.data

def get_tasks_by_status(status: str):
    res = (
        get_client()
        .table("tasks")
        .select("*, employees(name, email, department)")
        .eq("status", status)
        .execute()
    )
    return res.data

def get_overdue_tasks():
    today = date.today().isoformat()
    res = (
        get_client()
        .table("tasks")
        .select("*, employees(name, email, department)")
        .lt("deadline", today)
        .neq("status", "Done")
        .execute()
    )
    return res.data

def add_task(title: str, description: str, assigned_to: str, priority: str, deadline: str):
    res = get_client().table("tasks").insert({
        "title": title,
        "description": description,
        "assigned_to": assigned_to,
        "priority": priority,
        "deadline": deadline,
        "status": "Pending"
    }).execute()
    return res.data

def update_task_status(task_id: str, status: str):
    res = get_client().table("tasks").update({"status": status}).eq("id", task_id).execute()
    return res.data

def delete_task(task_id: str):
    res = get_client().table("tasks").delete().eq("id", task_id).execute()
    return res.data


# ─── REPORTS LOG ──────────────────────────────────────────────

def log_report(report_type: str, file_name: str):
    res = get_client().table("reports_log").insert({
        "report_type": report_type,
        "file_name": file_name
    }).execute()
    return res.data

def get_reports_log():
    res = get_client().table("reports_log").select("*").order("generated_at", desc=True).execute()
    return res.data
