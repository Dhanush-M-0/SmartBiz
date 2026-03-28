# SmartBiz — Employee Task & Report Automation System

A full-stack Python business automation application built for the **RISE Internship Program** by Tamizhan Skills.

---

## 🚀 Features

- **Employee Management** — Add, view, and remove employees
- **Task Management** — Assign tasks with priority, deadlines, and status tracking
- **Automated Reports** — Auto-generate Excel & CSV reports for tasks and performance
- **Live Currency API** — Real-time exchange rates via Frankfurter API (no key needed)
- **Email Notifications** — Automated overdue task alerts via Gmail SMTP
- **Background Scheduler** — Daily overdue checks + weekly auto-reports
- **Web Dashboard** — Clean Flask UI with full CRUD
- **CLI Interface** — Full command-line access to all features

---

## 🛠️ Tech Stack

| Layer       | Technology                     |
|-------------|-------------------------------|
| Language    | Python 3.10+                  |
| Database    | Supabase (PostgreSQL)         |
| Web         | Flask 3.x + Jinja2 templates  |
| CLI         | Click + Tabulate              |
| Reports     | Pandas + openpyxl             |
| API         | Frankfurter (currency rates)  |
| Email       | smtplib (Gmail SMTP)          |
| Scheduler   | schedule + threading          |
| Version Ctrl| Git                           |

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/smartbiz.git
cd smartbiz
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your Supabase database
- Go to your [Supabase project](https://supabase.com)
- Open the **SQL Editor**
- Paste and run the contents of `supabase_schema.sql`

### 5. Configure your environment
```bash
cp .env.example .env
```
Edit `.env` and fill in:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key
FLASK_SECRET_KEY=any-random-string
EMAIL_SENDER=your-gmail@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
```

> 💡 For Gmail, use an **App Password** (not your main password).
> Go to: Google Account → Security → 2-Step Verification → App Passwords

### 6. Run the Web App
```bash
python run.py
```
Open: **http://127.0.0.1:5000**

---

## 💻 CLI Usage

```bash
# Employees
python cli.py employee list
python cli.py employee add

# Tasks
python cli.py task list
python cli.py task list --status "In Progress"
python cli.py task add
python cli.py task overdue

# Reports
python cli.py report tasks
python cli.py report performance

# Currency
python cli.py currency rates --base USD
python cli.py currency convert

# Alerts
python cli.py send-alerts
```

---

## 📁 Project Structure

```
smartbiz/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── database.py          # Supabase client
│   ├── models.py            # All DB operations
│   ├── routes.py            # Flask routes
│   ├── api_service.py       # Currency API
│   ├── reports.py           # Excel/CSV generation
│   ├── notifier.py          # Email alerts
│   ├── scheduler.py         # Background jobs
│   └── templates/           # HTML templates
│       ├── base.html
│       ├── dashboard.html
│       ├── employees.html
│       ├── tasks.html
│       ├── reports.html
│       └── currency.html
├── reports_output/          # Auto-generated reports saved here
├── cli.py                   # CLI entry point
├── run.py                   # Web app entry point
├── config.py                # Config from .env
├── requirements.txt
├── supabase_schema.sql      # Run this in Supabase SQL Editor
├── .env.example
└── README.md
```

---

## 📋 RISE Internship Requirements Checklist

| Requirement                        | Status |
|------------------------------------|--------|
| Business problem identification    | ✅     |
| Modular Python application design  | ✅     |
| Integration with APIs              | ✅     |
| Integration with databases         | ✅     |
| Automation of business logic       | ✅     |
| Error handling and logging         | ✅     |
| Basic UI (Web + CLI)               | ✅     |
| Deployment-ready structure         | ✅     |
| Complete project documentation     | ✅     |

---

## 👨‍💻 Author

Built as part of the **RISE Internship Program — Python Programming Domain**
Tamizhan Skills | rise@tamizhanskills.com
