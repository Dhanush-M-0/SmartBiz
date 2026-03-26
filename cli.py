#!/usr/bin/env python3
"""
SmartBiz CLI - Command Line Interface for task management
"""

import click
import logging
from datetime import datetime
from database import get_db
from models import Employee, Task
from reports import get_report_generator
from notifications import get_notifier

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """SmartBiz Business Automation CLI"""
    pass

# ============== EMPLOYEE COMMANDS ==============

@cli.group()
def employee():
    """Manage employees"""
    pass

@employee.command()
@click.option('--name', prompt='Employee name', help='Full name of employee')
@click.option('--email', prompt='Email', help='Email address')
@click.option('--department', prompt='Department', help='Department name')
def add(name, email, department):
    """Add a new employee"""
    try:
        db = get_db()
        emp = Employee(name=name, email=email, department=department)
        
        result = db.table('employees').insert(emp.to_dict()).execute()
        click.echo(f"✓ Employee '{name}' added successfully!")
        logger.info(f"Added employee: {name}")
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        logger.error(f"Failed to add employee: {str(e)}")

@employee.command()
def list():
    """List all employees"""
    try:
        db = get_db()
        response = db.table('employees').select('*').execute()
        employees = response.data
        
        if not employees:
            click.echo("No employees found.")
            return
        
        click.echo("\n" + "="*60)
        click.echo("EMPLOYEES")
        click.echo("="*60)
        for emp in employees:
            click.echo(f"ID: {emp['id']} | Name: {emp['name']}")
            click.echo(f"   Email: {emp['email']} | Dept: {emp['department']}")
        click.echo("="*60 + "\n")
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        logger.error(f"Failed to list employees: {str(e)}")

# ============== TASK COMMANDS ==============

@cli.group()
def task():
    """Manage tasks"""
    pass

@task.command()
@click.option('--title', prompt='Task title', help='Task title')
@click.option('--description', prompt='Description', help='Task description', default='')
@click.option('--assigned-to', prompt='Assigned to (employee ID)', type=int, help='Employee ID')
@click.option('--priority', type=click.Choice(['low', 'medium', 'high']), default='medium')
@click.option('--due-date', prompt='Due date (YYYY-MM-DD)', help='Due date')
def create(title, description, assigned_to, priority, due_date):
    """Create a new task"""
    try:
        db = get_db()
        task = Task(
            title=title,
            description=description,
            assigned_to=assigned_to,
            priority=priority,
            due_date=due_date,
            status='pending'
        )
        
        result = db.table('tasks').insert(task.to_dict()).execute()
        click.echo(f"✓ Task '{title}' created successfully!")
        logger.info(f"Created task: {title}")
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        logger.error(f"Failed to create task: {str(e)}")

@task.command()
@click.option('--status', type=click.Choice(['pending', 'in_progress', 'done']), help='Filter by status')
def list(status):
    """List all tasks"""
    try:
        db = get_db()
        
        if status:
            response = db.table('tasks').select('*').eq('status', status).execute()
        else:
            response = db.table('tasks').select('*').execute()
        
        tasks = response.data
        
        if not tasks:
            click.echo(f"No tasks found {f'with status {status}' if status else ''}.")
            return
        
        click.echo("\n" + "="*80)
        click.echo("TASKS")
        click.echo("="*80)
        for task in tasks:
            click.echo(f"ID: {task['id']} | {task['title']}")
            click.echo(f"   Status: {task['status']} | Priority: {task['priority']}")
            click.echo(f"   Assigned to: {task['assigned_to']} | Due: {task['due_date']}")
        click.echo("="*80 + "\n")
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        logger.error(f"Failed to list tasks: {str(e)}")

@task.command()
@click.option('--id', prompt='Task ID', type=int, help='Task ID')
@click.option('--status', type=click.Choice(['pending', 'in_progress', 'done']), 
              prompt='New status', help='New status')
def update_status(id, status):
    """Update task status"""
    try:
        db = get_db()
        db.table('tasks').update({
            'status': status,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('id', id).execute()
        click.echo(f"✓ Task {id} status updated to '{status}'")
        logger.info(f"Updated task {id} status to {status}")
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        logger.error(f"Failed to update task: {str(e)}")

# ============== REPORT COMMANDS ==============

@cli.group()
def report():
    """Generate reports"""
    pass

@report.command()
def tasks_summary():
    """Generate task summary report"""
    try:
        generator = get_report_generator()
        filepath = generator.generate_task_summary_report()
        if filepath:
            click.echo(f"✓ Report generated: {filepath}")
        else:
            click.echo("✗ Failed to generate report", err=True)
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)

@report.command()
def employee_performance():
    """Generate employee performance report"""
    try:
        generator = get_report_generator()
        filepath = generator.generate_employee_performance_report()
        if filepath:
            click.echo(f"✓ Report generated: {filepath}")
        else:
            click.echo("✗ Failed to generate report", err=True)
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)

@report.command()
@click.option('--currency', default='USD', help='Base currency code')
def currency_rates(currency):
    """Generate currency rates report"""
    try:
        generator = get_report_generator()
        filepath = generator.generate_currency_rates_report(currency)
        if filepath:
            click.echo(f"✓ Report generated: {filepath}")
        else:
            click.echo("✗ Failed to generate report", err=True)
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)

@report.command()
def list():
    """List all generated reports"""
    try:
        generator = get_report_generator()
        reports = generator.list_reports()
        
        if not reports:
            click.echo("No reports found.")
            return
        
        click.echo("\n" + "="*50)
        click.echo("GENERATED REPORTS")
        click.echo("="*50)
        for i, report in enumerate(reports, 1):
            click.echo(f"{i}. {report}")
        click.echo("="*50 + "\n")
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)

# ============== UTILITY COMMANDS ==============

@cli.command()
def health():
    """Check system health"""
    try:
        db = get_db()
        is_healthy = db.health_check()
        
        if is_healthy:
            click.echo("✓ System is healthy - Database connection OK")
        else:
            click.echo("✗ System health check failed", err=True)
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)

@cli.command()
def setup():
    """Setup Supabase tables (run this first!)"""
    click.echo("To set up SmartBiz, create these tables in Supabase:\n")
    
    tables = {
        'employees': """
        CREATE TABLE employees (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """,
        'tasks': """
        CREATE TABLE tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            assigned_to INTEGER REFERENCES employees(id),
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'medium',
            due_date DATE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        """,
        'reports': """
        CREATE TABLE reports (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            report_type TEXT,
            generated_at TIMESTAMP DEFAULT NOW(),
            file_path TEXT
        );
        """,
        'notifications': """
        CREATE TABLE notifications (
            id SERIAL PRIMARY KEY,
            recipient_email TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT,
            sent_at TIMESTAMP,
            status TEXT DEFAULT 'pending'
        );
        """
    }
    
    for table_name, sql in tables.items():
        click.echo(f"\n{table_name.upper()}:")
        click.echo("-" * 50)
        click.echo(sql)

if __name__ == '__main__':
    cli()
