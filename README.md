# SmartBiz - Business Automation System 🚀

A complete, production-ready **end-to-end business automation platform** built with Flask, Supabase, and Python. Manage employees, automate tasks, generate reports, and send notifications—all integrated into one powerful system.

**⭐ Project 8 from RISE Internship Program - End-to-End Business App**

## 🎯 Overview

SmartBiz solves the problem: *Small businesses struggle to track employee tasks, deadlines, and performance manually.*

**Solution:** A unified system with CLI + Web dashboard that automates business workflows, generates insights, and keeps teams synchronized.

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 👥 **Employee Management** | Add, update, delete employees with departments |
| ✅ **Task Assignment** | Create, assign tasks with priorities and due dates |
| 📊 **Task Tracking** | Monitor status: Pending → In Progress → Done |
| 📈 **Auto Reports** | Generate Excel/CSV reports instantly |
| 📧 **Email Alerts** | Reminders for upcoming/overdue tasks |
| 💱 **Currency API** | Fetch live exchange rates for payroll |
| 🔄 **Background Jobs** | Automated scheduling (reminders, reports, alerts) |
| 🌐 **Web Dashboard** | Beautiful, responsive HTML5 interface |
| 🖥️ **CLI Tool** | Command-line power user interface |

---

## 🏗️ Architecture

```
SmartBiz (End-to-End Application)
├── Backend Layer
│   ├── Flask API (REST endpoints)
│   ├── Supabase PostgreSQL (data persistence)
│   └── Background Scheduler (automation)
│
├── Frontend Layer
│   ├── Responsive Dashboard (HTML5/JS)
│   └── CLI Interface (Python Click)
│
└── Integration Layer
    ├── Email Notifications (SMTP)
    ├── Exchange Rate API (currency)
    └── Report Generation (Pandas/Excel)
```

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Flask 2.3.3 REST API |
| **Database** | Supabase (PostgreSQL) with realtime |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Data Processing** | Pandas, OpenPyXL |
| **Automation** | Schedule library, Threading |
| **Email** | SMTP (Gmail/Outlook/SendGrid) |
| **External APIs** | ExchangeRate API |
| **Deployment Ready** | Heroku, Railway, Render support |

---

## 📋 Quick Start

### 1️⃣ Prerequisites
- Python 3.8+
- Supabase account (free tier)
- Gmail account (optional, for notifications)

### 2️⃣ Clone & Setup
```bash
cd SmartBiz
pip install -r requirements.txt
cp .env.example .env
```

### 3️⃣ Configure Supabase
See [QUICKSTART.md](QUICKSTART.md) for detailed setup

### 4️⃣ Run the Application
```bash
# Web Dashboard
python main.py
# Access: http://localhost:5000

# OR use CLI
python cli.py --help
```

**👉 [See QUICKSTART.md for complete setup guide](QUICKSTART.md)**

---

## 📊 Database Schema

### Employees Table
```sql
employees (
    id, name, email (unique), department, created_at
)
```

### Tasks Table  
```sql
tasks (
    id, title, description, assigned_to (FK),
    status (pending|in_progress|done),
    priority (low|medium|high),
    due_date, created_at, updated_at
)
```

### Reports Table
```sql
reports (
    id, name, report_type, generated_at, file_path
)
```

### Notifications Table
```sql
notifications (
    id, recipient_email, subject, body,
    sent_at, status (pending|sent|failed)
)
```

---

## 🌐 Web API Endpoints

### Employees
```
GET    /api/employees              → List all
POST   /api/employees              → Create new
GET    /api/employees/<id>         → Get one
PUT    /api/employees/<id>         → Update
DELETE /api/employees/<id>         → Delete
```

### Tasks
```
GET    /api/tasks?status=pending   → List (filterable)
POST   /api/tasks                  → Create new
GET    /api/tasks/<id>             → Get one
PUT    /api/tasks/<id>             → Update
DELETE /api/tasks/<id>             → Delete
```

### Reports
```
POST   /api/reports/task-summary   → Generate summary
POST   /api/reports/performance    → Generate performance
POST   /api/reports/currency       → Generate currency rates
GET    /api/reports/list           → List all reports
GET    /reports/<filename>         → Download file
```

### System
```
GET    /health                     → Health check
POST   /api/notifications/test     → Test email
```

---

## 🖥️ CLI Commands

```bash
# Employee Management
python cli.py employee add --name "John Doe" --email "john@example.com" --department "Engineering"
python cli.py employee list

# Task Management
python cli.py task create --title "Design UI" --assigned-to 1 --due-date 2026-04-01
python cli.py task list --status pending
python cli.py task update-status --id 1 --status done

# Report Generation
python cli.py report tasks-summary
python cli.py report employee-performance
python cli.py report currency-rates

# Utilities
python cli.py health
python cli.py setup
```

---

## 🔄 Automated Workflows

SmartBiz runs background jobs automatically:

| Job | Frequency | Action |
|-----|-----------|--------|
| **Overdue Check** | Every 1 hour | Check for overdue tasks, send alerts |
| **Task Reminders** | Every 30 minutes | Send reminders for tasks due today/tomorrow |
| **Daily Reports** | Every 24 hours | Auto-generate task summary report |

These run in a background thread and don't block the web server.

---

## 📈 Sample Workflow

### Scenario: Weekly Task Management

**Monday Morning:**
1. Manager adds 5 employees via Web UI
2. Creates 10 tasks in CLI (bulk via script)
3. Tasks auto-assigned with due dates

**Tuesday-Thursday:**
- System sends reminders 30 min before due times
- Dashboard shows real-time progress
- Manager can update task status anytime

**Friday Evening:**
- Auto-generated performance report (who completed what)
- Email sent with summary
- Currency rates fetched for payroll calculation

---

## 🔐 Security & Best Practices

✅ Environment variables for secrets  
✅ Supabase RLS policies (ready for production)  
✅ Email app-specific passwords (no main account)  
✅ CORS enabled for frontend  
✅ Input validation on all routes  
✅ Error logging & monitoring  
✅ `.gitignore` protects sensitive files  

---

## 🚀 Deployment

### Heroku
```bash
echo "web: gunicorn main:app" > Procfile
git push heroku main
```

### Railway / Render
1. Connect GitHub repository
2. Set environment variables
3. Auto-deploys on every push

### Self-Hosted (EC2/DigitalOcean)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

---

## 📚 Project Structure

```
SmartBiz/
├── main.py                 # Flask app & web routes
├── cli.py                  # Command-line interface
├── config.py               # Config management
├── database.py             # Supabase ORM
├── models.py               # Data models (Employee, Task, etc)
├── api_integration.py      # External APIs (currency)
├── notifications.py        # Email system
├── reports.py              # Report generation (Excel/CSV)
├── scheduler.py            # Background job scheduler
├── requirements.txt        # Python dependencies
├── .env.example            # Config template
├── .gitignore              # Git ignore rules
├── QUICKSTART.md           # Setup guide
├── run.sh                  # Start script
└── templates/
    └── dashboard.html      # Web UI (HTML5/JS)
```

---

## 🎓 Learning Outcomes

By building SmartBiz, you'll master:

✅ **Full-Stack Development** - Frontend + Backend integration  
✅ **API Design** - RESTful endpoints with proper status codes  
✅ **Database Design** - Relational schemas, foreign keys  
✅ **Authentication** - API key management  
✅ **Automation** - Background job scheduling  
✅ **Email Systems** - SMTP, notifications  
✅ **Data Processing** - Pandas, Excel generation  
✅ **Frontend Development** - Responsive HTML/CSS/JS  
✅ **DevOps** - Environment config, deployment  
✅ **Error Handling** - Graceful failures, logging  

---

## 🧪 Testing

### Unit Test Example
```python
from database import get_db

def test_create_employee():
    db = get_db()
    result = db.table('employees').insert({
        'name': 'Test User',
        'email': 'test@example.com',
        'department': 'Testing'
    }).execute()
    assert result.data[0]['id'] > 0
```

### Integration Test
```bash
python cli.py health  # Verify DB connection
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` |
| `SUPABASE_URL not set` | Check `.env` file exists |
| `Database connection failed` | Verify Supabase credentials |
| `SMTP authentication failed` | Use [Gmail app password](https://support.google.com/accounts/answer/185833) |
| `Port 5000 in use` | Run on different port: `flask run --port 5001` |

---

## 📞 Support

- **Setup Issues?** → See [QUICKSTART.md](QUICKSTART.md)
- **API Questions?** → Check endpoint docs above  
- **Database Help?** → Visit [Supabase Docs](https://supabase.com/docs)
- **Flask Tutorials?** → See [Flask Official Docs](https://flask.palletsprojects.com)

---

## 📈 Roadmap

- [ ] Admin dashboard with user roles
- [ ] Email digest summaries
- [ ] Task recurring/templates
- [ ] Slack integration
- [ ] Advanced analytics
- [ ] Mobile app (React Native)
- [ ] Multi-language support

---

## 📄 License

Built as part of **RISE Internship Program** - Python Projects

---

## 🎉 Credits

**Project Type:** End-to-End Business Application (Most Recommended)  
**Difficulty:** Intermediate → Advanced  
**Time to Complete:** 5-7 days  
**Portfolio Impact:** ⭐⭐⭐⭐⭐ Five stars  

---

**Ready to build? [Start with QUICKSTART.md →](QUICKSTART.md)**