"""
cli.py — SmartBiz Command Line Interface
Run with: python cli.py --help
"""

import click
from tabulate import tabulate
from . import models
from .reports import generate_task_report, generate_employee_performance_report
from .api_service import get_exchange_rates, convert_currency
from .notifier import notify_overdue_tasks


@click.group()
def cli():
    """SmartBiz CLI — Business Automation System"""
    pass


# ─── EMPLOYEES ───────────────────────────────────────────────

@cli.group()
def employee():
    """Manage employees."""
    pass

@employee.command("list")
def list_employees():
    """List all employees."""
    data = models.get_all_employees()
    if not data:
        click.echo("No employees found.")
        return
    rows = [[e["name"], e["email"], e["department"], e["created_at"][:10]] for e in data]
    click.echo(tabulate(rows, headers=["Name", "Email", "Department", "Joined"], tablefmt="rounded_outline"))

@employee.command("add")
@click.option("--name", prompt="Full name", help="Employee's full name")
@click.option("--email", prompt="Email", help="Employee's email")
@click.option("--department", prompt="Department", help="Department name")
def add_employee(name, email, department):
    """Add a new employee."""
    models.add_employee(name, email, department)
    click.secho(f"✅ Employee '{name}' added successfully.", fg="green")


# ─── TASKS ───────────────────────────────────────────────────

@cli.group()
def task():
    """Manage tasks."""
    pass

@task.command("list")
@click.option("--status", default="All", help="Filter: Pending | In Progress | Done | All")
def list_tasks(status):
    """List all tasks."""
    data = models.get_all_tasks()
    if status != "All":
        data = [t for t in data if t["status"] == status]
    if not data:
        click.echo("No tasks found.")
        return
    rows = [
        [t["title"], t["employees"]["name"] if t["employees"] else "—",
         t["priority"], t["status"], t["deadline"]]
        for t in data
    ]
    click.echo(tabulate(rows, headers=["Title", "Assigned To", "Priority", "Status", "Deadline"], tablefmt="rounded_outline"))

@task.command("add")
@click.option("--title", prompt="Task title")
@click.option("--description", default="", prompt="Description (optional)")
@click.option("--priority", type=click.Choice(["Low","Medium","High"]), default="Medium", prompt="Priority")
@click.option("--deadline", prompt="Deadline (YYYY-MM-DD)")
def add_task(title, description, priority, deadline):
    """Add a new task."""
    employees = models.get_all_employees()
    if employees:
        click.echo("\nAvailable Employees:")
        for i, e in enumerate(employees):
            click.echo(f"  [{i+1}] {e['name']} ({e['department']})")
        idx = click.prompt("Assign to (number, or 0 for unassigned)", type=int, default=0)
        assigned_to = employees[idx-1]["id"] if 1 <= idx <= len(employees) else None
    else:
        assigned_to = None
    models.add_task(title, description, assigned_to, priority, deadline)
    click.secho(f"✅ Task '{title}' created.", fg="green")

@task.command("update")
@click.argument("task_id")
@click.option("--status", type=click.Choice(["Pending","In Progress","Done"]), prompt="New status")
def update_task(task_id, status):
    """Update task status by ID."""
    models.update_task_status(task_id, status)
    click.secho(f"✅ Task updated to '{status}'.", fg="green")

@task.command("overdue")
def show_overdue():
    """Show all overdue tasks."""
    data = models.get_overdue_tasks()
    if not data:
        click.secho("✅ No overdue tasks!", fg="green")
        return
    rows = [[t["title"], t["employees"]["name"] if t["employees"] else "—", t["deadline"]] for t in data]
    click.secho(f"\n⚠️  {len(data)} Overdue Task(s):", fg="red", bold=True)
    click.echo(tabulate(rows, headers=["Title", "Assigned To", "Deadline"], tablefmt="rounded_outline"))


# ─── REPORTS ─────────────────────────────────────────────────

@cli.group()
def report():
    """Generate reports."""
    pass

@report.command("tasks")
def report_tasks():
    """Generate Excel task report."""
    click.echo("Generating task report...")
    path = generate_task_report()
    if path:
        click.secho(f"✅ Report saved: {path}", fg="green")
    else:
        click.secho("No tasks to report.", fg="yellow")

@report.command("performance")
def report_performance():
    """Generate employee performance CSV."""
    click.echo("Generating performance report...")
    path = generate_employee_performance_report()
    click.secho(f"✅ Report saved: {path}", fg="green")


# ─── CURRENCY ────────────────────────────────────────────────

@cli.group()
def currency():
    """Live currency tools."""
    pass

@currency.command("rates")
@click.option("--base", default="USD", help="Base currency code")
def rates(base):
    """Show live exchange rates."""
    click.echo(f"Fetching rates for {base}...")
    data = get_exchange_rates(base)
    if "error" in data:
        click.secho(f"❌ {data['error']}", fg="red")
        return
    rows = [[code, rate] for code, rate in list(data["rates"].items())[:15]]
    click.echo(f"\n📈 Rates as of {data['date']} (Base: {data['base']})")
    click.echo(tabulate(rows, headers=["Currency", "Rate"], tablefmt="rounded_outline"))

@currency.command("convert")
@click.option("--amount", prompt="Amount", type=float)
@click.option("--from-currency", prompt="From currency (e.g. USD)")
@click.option("--to-currency", prompt="To currency (e.g. INR)")
def convert(amount, from_currency, to_currency):
    """Convert between currencies."""
    result = convert_currency(amount, from_currency.upper(), to_currency.upper())
    if "error" in result:
        click.secho(f"❌ {result['error']}", fg="red")
    else:
        click.secho(
            f"\n💱 {amount} {result['from']} = {result['converted_amount']} {result['to']}  (as of {result['date']})",
            fg="cyan", bold=True
        )


# ─── ALERTS ──────────────────────────────────────────────────

@cli.command("send-alerts")
def send_alerts():
    """Send overdue task email alerts to employees."""
    overdue = models.get_overdue_tasks()
    if not overdue:
        click.secho("✅ No overdue tasks. No alerts needed.", fg="green")
        return
    click.echo(f"Sending alerts for {len(overdue)} overdue task(s)...")
    sent = notify_overdue_tasks(overdue)
    click.secho(f"✅ Sent {sent} email alert(s).", fg="green")


if __name__ == "__main__":
    cli()
