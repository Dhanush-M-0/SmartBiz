from datetime import datetime
from typing import Optional, List

class Employee:
    """Employee model"""
    def __init__(self, id: Optional[int] = None, name: str = "", 
                 email: str = "", department: str = "", 
                 created_at: Optional[str] = None):
        self.id = id
        self.name = name
        self.email = email
        self.department = department
        self.created_at = created_at or datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'created_at': self.created_at
        }

class Task:
    """Task model"""
    def __init__(self, id: Optional[int] = None, title: str = "", 
                 description: str = "", assigned_to: int = None,
                 status: str = "pending", priority: str = "medium",
                 due_date: Optional[str] = None, created_at: Optional[str] = None,
                 updated_at: Optional[str] = None):
        self.id = id
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.status = status  # pending, in_progress, done
        self.priority = priority  # low, medium, high
        self.due_date = due_date
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'assigned_to': self.assigned_to,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Report:
    """Report model"""
    def __init__(self, id: Optional[int] = None, name: str = "",
                 report_type: str = "task_summary",
                 generated_at: Optional[str] = None,
                 file_path: str = ""):
        self.id = id
        self.name = name
        self.report_type = report_type  # task_summary, employee_performance, currency_rates
        self.generated_at = generated_at or datetime.utcnow().isoformat()
        self.file_path = file_path
    
    def to_dict(self):
        return {
            'name': self.name,
            'report_type': self.report_type,
            'generated_at': self.generated_at,
            'file_path': self.file_path
        }

class Notification:
    """Notification model"""
    def __init__(self, id: Optional[int] = None, recipient_email: str = "",
                 subject: str = "", body: str = "",
                 sent_at: Optional[str] = None, status: str = "pending"):
        self.id = id
        self.recipient_email = recipient_email
        self.subject = subject
        self.body = body
        self.sent_at = sent_at
        self.status = status  # pending, sent, failed
    
    def to_dict(self):
        return {
            'recipient_email': self.recipient_email,
            'subject': self.subject,
            'body': self.body,
            'sent_at': self.sent_at,
            'status': self.status
        }

# Supabase table schemas (for reference - create these manually in Supabase)
SUPABASE_SCHEMAS = {
    'employees': {
        'columns': [
            'id: int8 (PK)',
            'name: text',
            'email: text (unique)',
            'department: text',
            'created_at: timestamp'
        ]
    },
    'tasks': {
        'columns': [
            'id: int8 (PK)',
            'title: text',
            'description: text',
            'assigned_to: int8 (FK -> employees.id)',
            'status: text (pending|in_progress|done)',
            'priority: text (low|medium|high)',
            'due_date: date',
            'created_at: timestamp',
            'updated_at: timestamp'
        ]
    },
    'reports': {
        'columns': [
            'id: int8 (PK)',
            'name: text',
            'report_type: text',
            'generated_at: timestamp',
            'file_path: text'
        ]
    },
    'notifications': {
        'columns': [
            'id: int8 (PK)',
            'recipient_email: text',
            'subject: text',
            'body: text',
            'sent_at: timestamp',
            'status: text (pending|sent|failed)'
        ]
    }
}
