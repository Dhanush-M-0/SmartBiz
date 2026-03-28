"""
notifier.py — Sends email alerts via Gmail SMTP
for overdue tasks and report delivery.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import Config


def _send_email(to_email: str, subject: str, body: str) -> bool:
    """Core email sending function using Gmail SMTP."""
    if not Config.EMAIL_SENDER or not Config.EMAIL_PASSWORD:
        print("[Notifier] Email credentials not configured. Skipping.")
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = Config.EMAIL_SENDER
        msg["To"]      = to_email
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(Config.EMAIL_SENDER, Config.EMAIL_PASSWORD)
            smtp.sendmail(Config.EMAIL_SENDER, to_email, msg.as_string())
        print(f"[Notifier] Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"[Notifier] Failed to send email: {e}")
        return False


def notify_overdue_tasks(overdue_tasks: list) -> int:
    """
    Send overdue task alerts to each assigned employee.
    Returns the count of emails successfully sent.
    """
    sent = 0
    # Group tasks by employee email
    from collections import defaultdict
    grouped = defaultdict(list)
    for task in overdue_tasks:
        emp = task.get("employees")
        if emp and emp.get("email"):
            grouped[emp["email"]].append(task)

    for email, tasks in grouped.items():
        task_list_html = "".join(
            f"<li><b>{t['title']}</b> — Due: {t['deadline']} ({t['priority']} priority)</li>"
            for t in tasks
        )
        body = f"""
        <h2 style="color:#e53e3e;">⚠️ Overdue Task Alert — SmartBiz</h2>
        <p>Hi {tasks[0]['employees']['name']},</p>
        <p>You have <b>{len(tasks)}</b> overdue task(s) that need your immediate attention:</p>
        <ul>{task_list_html}</ul>
        <p>Please update your task status as soon as possible.</p>
        <br><p style="color:#718096;font-size:12px;">— SmartBiz Automation System</p>
        """
        if _send_email(email, "⚠️ You Have Overdue Tasks — SmartBiz", body):
            sent += 1
    return sent


def notify_report_ready(to_email: str, report_type: str, file_name: str) -> bool:
    """Notify a manager that a report has been generated."""
    body = f"""
    <h2 style="color:#3182ce;">📊 Report Ready — SmartBiz</h2>
    <p>Your <b>{report_type}</b> report has been generated successfully.</p>
    <p><b>File:</b> {file_name}</p>
    <p>You can find it in the <code>reports_output/</code> folder.</p>
    <br><p style="color:#718096;font-size:12px;">— SmartBiz Automation System</p>
    """
    return _send_email(to_email, f"📊 {report_type} Report Ready — SmartBiz", body)
