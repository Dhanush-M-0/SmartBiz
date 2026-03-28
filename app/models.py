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
        .select("*")
        .order("due_date", desc=False)
        .execute()
    )
    return res.data

def get_tasks_by_status(status: str):
    # Convert status to lowercase for Supabase check constraint
    status_lower = status.lower() if status else status
    res = (
        get_client()
        .table("tasks")
        .select("*")
        .eq("status", status_lower)
        .execute()
    )
    return res.data

def get_overdue_tasks():
    from datetime import date
    today = date.today().isoformat()
    res = (
        get_client()
        .table("tasks")
        .select("*")
        .lt("due_date", today)
        .neq("status", "done")
        .execute()
    )
    return res.data

def add_task(title: str, description: str, assigned_to: str, priority: str, deadline: str):
    # Convert status and priority to lowercase for Supabase check constraints
    priority_lower = priority.lower() if priority else "medium"
    
    # Build task data, excluding None/empty values for foreign keys
    task_data = {
        "title": title,
        "description": description or "",
        "priority": priority_lower,
        "status": "pending"
    }
    
    # Only include assigned_to if it's a valid value (not empty string or None)
    if assigned_to and assigned_to.strip():
        task_data["assigned_to"] = assigned_to
    
    # Only include due_date if provided
    if deadline and deadline.strip():
        task_data["due_date"] = deadline
    
    res = get_client().table("tasks").insert(task_data).execute()
    return res.data

def update_task_status(task_id: str, status: str):
    # Convert status to lowercase for Supabase check constraint
    status_lower = status.lower() if status else status
    res = get_client().table("tasks").update({"status": status_lower}).eq("id", task_id).execute()
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
