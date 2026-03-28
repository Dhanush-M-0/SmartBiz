"""
routes.py — HTML web routes for SmartBiz (legacy, kept for compatibility).
For React SPA, use the /api/* endpoints instead.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from . import models
from .reports import generate_task_report, generate_employee_performance_report
from .api_service import get_exchange_rates, convert_currency
from .notifier import notify_overdue_tasks

main = Blueprint("main", __name__)


# ─── API INFO (DEFAULT ROUTE) ─────────────────────────────────

@main.route("/")
def index():
    """API info endpoint - describes available endpoints"""
    return jsonify({
        "name": "SmartBiz API",
        "version": "1.0.0",
        "description": "Employee and Task Management REST API",
        "endpoints": {
            "employees": {
                "GET /api/employees": "List all employees",
                "POST /api/employees": "Create employee",
                "GET /api/employees/:id": "Get one employee",
                "PUT /api/employees/:id": "Update employee",
                "DELETE /api/employees/:id": "Delete employee"
            },
            "tasks": {
                "GET /api/tasks": "List all tasks (optional ?status=filter)",
                "POST /api/tasks": "Create task",
                "GET /api/tasks/:id": "Get one task",
                "PUT /api/tasks/:id": "Update task",
                "DELETE /api/tasks/:id": "Delete task"
            },
            "health": {
                "GET /health": "Liveness check",
                "GET /ready": "Readiness check"
            },
            "currency": {
                "GET /api/currency/rates": "Get exchange rates",
                "GET /api/currency/convert": "Convert currency"
            }
        },
        "frontend": "Use the React SPA on port 5173"
    })


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

@main.route("/api/currency/rates", methods=["GET"])
def currency_rates():
    """Get exchange rates for a base currency"""
    base = request.args.get("base", "USD")
    rates = get_exchange_rates(base)
    return jsonify({"success": True, "data": rates})

@main.route("/api/currency/convert", methods=["GET"])
def currency_convert():
    """Convert amount between currencies"""
    try:
        amount = float(request.args.get("amount", 1))
        from_currency = request.args.get("from", "USD")
        to_currency = request.args.get("to", "INR")
        result = convert_currency(amount, from_currency, to_currency)
        return jsonify({"success": True, "data": result})
    except ValueError:
        return jsonify({"success": False, "error": "Invalid amount"}), 400
