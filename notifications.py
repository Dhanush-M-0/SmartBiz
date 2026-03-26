import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
from database import get_db

logger = logging.getLogger(__name__)

class EmailNotifier:
    """Handle email notifications"""
    
    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.sender_email = Config.EMAIL_ADDRESS
        self.sender_password = Config.EMAIL_PASSWORD
    
    def send_email(self, recipient_email: str, subject: str, body: str, 
                   is_html: bool = False) -> bool:
        """
        Send an email notification
        
        Args:
            recipient_email: Recipient's email address
            subject: Email subject
            body: Email body content
            is_html: Whether body is HTML formatted
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Create email message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = recipient_email
            
            # Attach body
            mime_type = 'html' if is_html else 'plain'
            message.attach(MIMEText(body, mime_type))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            logger.info(f"✓ Email sent to {recipient_email}: {subject}")
            return True
        
        except Exception as e:
            logger.error(f"✗ Failed to send email to {recipient_email}: {str(e)}")
            return False
    
    def send_task_reminder(self, employee_email: str, employee_name: str, 
                          task_title: str, due_date: str) -> bool:
        """Send task reminder email"""
        subject = f"🔔 Task Reminder: {task_title}"
        body = f"""
        Hi {employee_name},
        
        This is a reminder that you have a task coming up:
        
        Task: {task_title}
        Due Date: {due_date}
        
        Please ensure it's completed on time.
        
        Best regards,
        SmartBiz Automation System
        """
        return self.send_email(employee_email, subject, body)
    
    def send_overdue_alert(self, employee_email: str, employee_name: str,
                          task_title: str) -> bool:
        """Send overdue task alert email"""
        subject = f"⚠️  Overdue Task Alert: {task_title}"
        body = f"""
        Hi {employee_name},
        
        The following task is now overdue:
        
        Task: {task_title}
        
        Please complete it as soon as possible.
        
        Best regards,
        SmartBiz Automation System
        """
        return self.send_email(employee_email, subject, body)
    
    def send_report_ready(self, recipient_email: str, report_name: str) -> bool:
        """Send report ready notification email"""
        subject = f"📊 Report Ready: {report_name}"
        body = f"""
        Hi,
        
        Your requested report has been generated and is ready for download:
        
        Report: {report_name}
        
        You can access it from the SmartBiz dashboard.
        
        Best regards,
        SmartBiz Automation System
        """
        return self.send_email(recipient_email, subject, body)
    
    def log_notification(self, recipient_email: str, subject: str, 
                        body: str, status: str = 'sent') -> bool:
        """Log notification to database"""
        try:
            db = get_db()
            db.table('notifications').insert({
                'recipient_email': recipient_email,
                'subject': subject,
                'body': body[:200],  # Store truncated body
                'status': status,
                'sent_at': None if status == 'pending' else 'now()'
            }).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to log notification: {str(e)}")
            return False

email_notifier = EmailNotifier()

def get_notifier():
    """Get email notifier instance"""
    return email_notifier
