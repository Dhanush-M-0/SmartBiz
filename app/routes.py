"""
routes.py — All Flask web routes for SmartBiz dashboard.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from . import models
from .reports import generate_task_report, generate_employee_performance_report
from .api_service import get_exchange_rates, convert_currency
from .notifier import notify_overdue_tasks

main = Blueprint("main", __name__)


# ─── DASHBOARD ───────────────────────────────────────────────

@main.route("/")
def dashboard():
    tasks     = models.get_all_tasks()
    employees = models.get_all_employees()
    overdue   = models.get_overdue_tasks()

    stats = {
        "total_tasks":    len(tasks),
        "pending":        sum(1 for t in tasks if t["status"] == "Pending"),
        "in_progress":    sum(1 for t in tasks if t["status"] == "In Progress"),
        "done":           sum(1 for t in tasks if t["status"] == "Done"),
        "total_employees": len(employees),
        "overdue":        len(overdue),
    }
    return render_template("dashboard.html", stats=stats, overdue=overdue, recent_tasks=tasks[:5])


# ─── EMPLOYEES ───────────────────────────────────────────────

@main.route("/employees")
def employees():
    all_employees = models.get_all_employees()
    return render_template("employees.html", employees=all_employees)

@main.route("/employees/add", methods=["POST"])
def add_employee():
    name       = request.form.get("name", "").strip()
    email      = request.form.get("email", "").strip()
    department = request.form.get("department", "").strip()
    if not name or not email or not department:
        flash("All fields are required.", "error")
        return redirect(url_for("main.employees"))
    try:
        models.add_employee(name, email, department)
        flash(f"Employee '{name}' added successfully.", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for("main.employees"))

@main.route("/employees/delete/<emp_id>", methods=["POST"])
def delete_employee(emp_id):
    models.delete_employee(emp_id)
    flash("Employee removed.", "success")
    return redirect(url_for("main.employees"))


# ─── TASKS ───────────────────────────────────────────────────

@main.route("/tasks")
def tasks():
    all_tasks  = models.get_all_tasks()
    employees  = models.get_all_employees()
    status_filter = request.args.get("status", "All")
    if status_filter != "All":
        all_tasks = [t for t in all_tasks if t["status"] == status_filter]
    return render_template("tasks.html", tasks=all_tasks, employees=employees, status_filter=status_filter)

@main.route("/tasks/add", methods=["POST"])
def add_task():
    title       = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    assigned_to = request.form.get("assigned_to")
    priority    = request.form.get("priority", "Medium")
    deadline    = request.form.get("deadline")
    if not title or not deadline:
        flash("Title and deadline are required.", "error")
        return redirect(url_for("main.tasks"))
    models.add_task(title, description, assigned_to, priority, deadline)
    flash(f"Task '{title}' created successfully.", "success")
    return redirect(url_for("main.tasks"))

@main.route("/tasks/update/<task_id>", methods=["POST"])
def update_task(task_id):
    status = request.form.get("status")
    models.update_task_status(task_id, status)
    flash("Task status updated.", "success")
    return redirect(url_for("main.tasks"))

@main.route("/tasks/delete/<task_id>", methods=["POST"])
def delete_task(task_id):
    models.delete_task(task_id)
    flash("Task deleted.", "success")
    return redirect(url_for("main.tasks"))


# ─── REPORTS ─────────────────────────────────────────────────

@main.route("/reports")
def reports():
    logs = models.get_reports_log()
    return render_template("reports.html", logs=logs)

@main.route("/reports/task", methods=["POST"])
def report_task():
    path = generate_task_report()
    if path:
        flash(f"Task report generated: {path}", "success")
    else:
        flash("No tasks found to report.", "error")
    return redirect(url_for("main.reports"))

@main.route("/reports/performance", methods=["POST"])
def report_performance():
    path = generate_employee_performance_report()
    flash(f"Performance report generated: {path}", "success")
    return redirect(url_for("main.reports"))

@main.route("/reports/send-overdue", methods=["POST"])
def send_overdue_alerts():
    overdue = models.get_overdue_tasks()
    if overdue:
        sent = notify_overdue_tasks(overdue)
        flash(f"Sent {sent} overdue alert email(s) for {len(overdue)} task(s).", "success")
    else:
        flash("No overdue tasks found!", "success")
    return redirect(url_for("main.reports"))


# ─── CURRENCY API ────────────────────────────────────────────

@main.route("/currency")
def currency():
    rates = get_exchange_rates("USD")
    return render_template("currency.html", rates=rates)

@main.route("/currency/convert", methods=["GET"])
def currency_convert():
    amount        = float(request.args.get("amount", 1))
    from_currency = request.args.get("from", "USD")
    to_currency   = request.args.get("to", "INR")
    result = convert_currency(amount, from_currency, to_currency)
    return jsonify(result)
