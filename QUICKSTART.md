# SmartBiz - Quick Start Guide

## 📋 Prerequisites

Before running SmartBiz, ensure you have:
- Python 3.8+ installed
- A Supabase account (free tier works)
- A Gmail account (for email notifications, optional)

---

## 🔧 Step 1: Configure Supabase

### Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Sign up / Log in
3. Create a new project
4. Wait for it to be ready
5. Go to **Settings → API** and copy:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon public** key (under API Keys)

### Create Database Tables

In Supabase Dashboard, go to **SQL Editor** and run these commands:

```sql
-- Create employees table
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    assigned_to INTEGER REFERENCES employees(id) ON DELETE CASCADE,
    status TEXT CHECK (status IN ('pending', 'in_progress', 'done')) DEFAULT 'pending',
    priority TEXT CHECK (priority IN ('low', 'medium', 'high')) DEFAULT 'medium',
    due_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create reports table
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    report_type TEXT,
    generated_at TIMESTAMP DEFAULT NOW(),
    file_path TEXT
);

-- Create notifications table
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    recipient_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT,
    sent_at TIMESTAMP,
    status TEXT CHECK (status IN ('pending', 'sent', 'failed')) DEFAULT 'pending'
);

-- Create indexes for better performance
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_employees_email ON employees(email);
```

---

## ⚙️ Step 2: Configure Environment Variables

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` and fill in:

```
# Required - Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=generate-a-random-string-here

# Optional - Email notifications (Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password  # NOT your main password!
```

### ℹ️ Getting Gmail App Password
1. Enable 2FA on your Google account
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Generate an app password
4. Use that password in `.env`

---

## 🚀 Step 3: Install & Run

### Option A: Using the startup script
```bash
chmod +x run.sh
./run.sh
```

### Option B: Manual setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python main.py
```

---

## 🌐 Access the Application

Once running, open your browser:

**Web Dashboard:** http://localhost:5000

Features available:
- 📊 Dashboard with statistics
- 👥 Employee management
- ✅ Task creation & tracking
- 📈 Report generation
- ⚙️ System settings & email testing

---

## 🖥️ Using the CLI

In another terminal, you can use the command-line interface:

```bash
# Employee commands
python cli.py employee add --name "John Doe" --email "john@example.com" --department "Engineering"
python cli.py employee list

# Task commands
python cli.py task create --title "Design UI" --assigned-to 1 --due-date 2026-04-01
python cli.py task list
python cli.py task update-status --id 1 --status done

# Report commands
python cli.py report tasks-summary
python cli.py report employee-performance
python cli.py report list

# Utilities
python cli.py health
python cli.py setup
```

---

## 🧪 Test the System

1. **Add an Employee** (Web)
   - Go to Employees tab
   - Fill form and click "Add Employee"

2. **Create a Task** (Web)
   - Go to Tasks tab
   - Assign it to the employee you just created
   - Set a due date

3. **Generate a Report** (Web)
   - Go to Reports tab
   - Click "Generate Report"
   - Download the Excel file

4. **Test Email** (Web)
   - Go to Settings tab
   - Enter an email address
   - Click "Send Test Email"

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `SUPABASE_URL not found` | Check `.env` file exists and has correct URL |
| `Database connection failed` | Verify Supabase URL and key are correct |
| `SMTP authentication failed` | Use [app-specific Gmail password](https://support.google.com/accounts/answer/185833) |
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` |
| `Port 5000 already in use` | Run on different port: `flask run --port 5001` |

---

## 📚 Project Structure

```
SmartBiz/
├── main.py              # Flask web app
├── cli.py               # Command-line interface
├── config.py            # Configuration
├── database.py          # Supabase connection
├── models.py            # Data models
├── api_integration.py   # External APIs
├── notifications.py     # Email system
├── reports.py           # Report generation
├── scheduler.py         # Background jobs
├── templates/
│   └── dashboard.html   # Web UI
├── reports/             # Generated reports (auto-created)
├── requirements.txt     # Dependencies
├── .env.example         # Example config
└── run.sh              # Startup script
```

---

## 🎯 Next Steps

1. ✅ Configure Supabase
2. ✅ Set up `.env` file
3. ✅ Run `python main.py`
4. ✅ Access http://localhost:5000
5. ✅ Add employees & tasks
6. ✅ Generate reports
7. ✅ Deploy to Heroku/Railway/Render

---

## 🆘 Need Help?

- Check Flask logs for error messages
- Verify `.env` file has all required variables
- Test Supabase connection: `python -c "from database import db; print(db.health_check())"`
- Review the full README.md for detailed documentation

---

**Ready to automate your business? Let's go! 🚀**
