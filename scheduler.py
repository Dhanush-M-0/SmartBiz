import schedule
import logging
import threading
import time
from datetime import datetime, timedelta
from database import get_db
from notifications import get_notifier
from reports import get_report_generator

logger = logging.getLogger(__name__)

class TaskScheduler:
    """Handle scheduled background jobs"""
    
    def __init__(self):
        self.scheduler = schedule.Scheduler()
        self.running = False
        self.thread = None
    
    def schedule_job(self, job_func, interval: int, unit: str = 'minutes'):
        """
        Schedule a job to run at regular intervals
        
        Args:
            job_func: Function to execute
            interval: How often to run
            unit: 'minutes', 'hours', 'days'
        """
        try:
            if unit == 'minutes':
                self.scheduler.every(interval).minutes.do(job_func)
            elif unit == 'hours':
                self.scheduler.every(interval).hours.do(job_func)
            elif unit == 'days':
                self.scheduler.every(interval).days.do(job_func)
            
            logger.info(f"✓ Scheduled job: {job_func.__name__} every {interval} {unit}")
        except Exception as e:
            logger.error(f"✗ Failed to schedule job: {str(e)}")
    
    def check_overdue_tasks(self):
        """Check for overdue tasks and send alerts"""
        try:
            db = get_db()
            notifier = get_notifier()
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Fetch overdue tasks
            response = db.table('tasks').select(
                'id, title, assigned_to, due_date'
            ).lt('due_date', today).eq('status', 'pending').execute()
            
            overdue_tasks = response.data
            
            for task in overdue_tasks:
                # Fetch employee email
                emp_response = db.table('employees').select('name, email').eq(
                    'id', task['assigned_to']
                ).execute()
                
                if emp_response.data:
                    employee = emp_response.data[0]
                    notifier.send_overdue_alert(
                        employee['email'],
                        employee['name'],
                        task['title']
                    )
            
            if overdue_tasks:
                logger.info(f"✓ Checked overdue tasks: {len(overdue_tasks)} found")
        
        except Exception as e:
            logger.error(f"✗ Failed to check overdue tasks: {str(e)}")
    
    def send_task_reminders(self):
        """Send reminders for tasks due tomorrow or today"""
        try:
            db = get_db()
            notifier = get_notifier()
            
            # Calculate dates
            today = datetime.now().strftime('%Y-%m-%d')
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Fetch tasks due soon
            response = db.table('tasks').select(
                'id, title, assigned_to, due_date'
            ).filter('due_date', 'in', (today, tomorrow)).eq(
                'status', 'pending'
            ).execute()
            
            upcoming_tasks = response.data
            
            for task in upcoming_tasks:
                # Fetch employee email
                emp_response = db.table('employees').select('name, email').eq(
                    'id', task['assigned_to']
                ).execute()
                
                if emp_response.data:
                    employee = emp_response.data[0]
                    notifier.send_task_reminder(
                        employee['email'],
                        employee['name'],
                        task['title'],
                        task['due_date']
                    )
            
            if upcoming_tasks:
                logger.info(f"✓ Sent reminders: {len(upcoming_tasks)} tasks")
        
        except Exception as e:
            logger.error(f"✗ Failed to send task reminders: {str(e)}")
    
    def generate_daily_report(self):
        """Generate daily task summary report"""
        try:
            generator = get_report_generator()
            filepath = generator.generate_task_summary_report()
            
            if filepath:
                logger.info(f"✓ Daily report generated: {filepath}")
        
        except Exception as e:
            logger.error(f"✗ Failed to generate daily report: {str(e)}")
    
    def run_scheduler(self):
        """Run scheduler in background"""
        self.running = True
        logger.info("✓ Scheduler started")
        
        while self.running:
            self.scheduler.run_pending()
            time.sleep(1)
    
    def start(self):
        """Start scheduler in background thread"""
        if not self.running:
            # Schedule jobs
            self.schedule_job(self.check_overdue_tasks, 1, 'hours')
            self.schedule_job(self.send_task_reminders, 30, 'minutes')
            self.schedule_job(self.generate_daily_report, 1, 'days')
            
            # Start thread
            self.thread = threading.Thread(target=self.run_scheduler, daemon=True)
            self.thread.start()
            logger.info("✓ Scheduler thread started")
    
    def stop(self):
        """Stop scheduler"""
        self.running = False
        logger.info("✓ Scheduler stopped")

scheduler = TaskScheduler()

def get_scheduler():
    """Get task scheduler instance"""
    return scheduler
