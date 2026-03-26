# 🚀 SmartBiz - Setup Instructions (WITH YOUR CREDENTIALS)

Your Supabase project is ready! Follow these steps to get SmartBiz running.

---

## ✅ Step 1: Create Database Tables (2 minutes)

1. **Open Supabase Dashboard:**
   - Go to https://app.supabase.com
   - Select your project: `dasuomsluytkgcjondne`

2. **Create Tables:**
   - Click **SQL Editor** (left sidebar)
   - Click **New Query**
   - Open [DATABASE_SETUP.sql](DATABASE_SETUP.sql) in this folder
   - Copy ALL the SQL code
   - Paste into the Supabase SQL Editor
   - Click **Run** (or Cmd+Enter)

3. **Verify:**
   - You should see: ✅ 4 tables created (employees, tasks, reports, notifications)
   - Plus 1 sample admin user

---

## ✅ Step 2: Install Python Dependencies (1-2 minutes)

**Option A: Automated Installer (Recommended)**
```bash
python install_deps.py
```
This automatically tries multiple installation methods until one works.

**Option B: Manual Installation**
```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --only-binary :all:
```

**Option C: If you get pandas build errors**
```bash
pip install -r requirements-minimal.txt
```

**What gets installed:**
- Flask (web framework)
- Supabase Python client
- Pandas & OpenPyXL (reports)
- Schedule (background jobs)
- Click (CLI)

---

## ✅ Step 3: Run the Application (30 seconds)

### Option A: Web Dashboard (Recommended)
```bash
python main.py
```
Then open: **http://localhost:5000** 🌐

### Option B: Command-Line Interface
```bash
python cli.py --help
python cli.py employee list
```

---

## 🎯 What You Can Do Now

### 📊 Web Dashboard (http://localhost:5000)
- ✅ Add employees
- ✅ Create and assign tasks
- ✅ Track task status
- ✅ Generate Excel reports
- ✅ Test email notifications
- ✅ Check system health

### 🖥️ CLI Commands
```bash
# Add employee
python cli.py employee add \
  --name "John Doe" \
  --email "john@example.com" \
  --department "Engineering"

# List all employees
python cli.py employee list

# Create a task
python cli.py task create \
  --title "Design homepage" \
  --assigned-to 1 \
  --due-date 2026-04-01 \
  --priority high

# List tasks
python cli.py task list

# Generate reports
python cli.py report tasks-summary
```

---

## 📧 (Optional) Enable Email Notifications

If you want to receive task reminders and alerts:

1. **Get Gmail App Password:**
   - Enable 2FA on your Google account
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated 16-character password

2. **Update .env file:**
   ```
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-16-char-password
   ```

3. **Test it:**
   - Go to http://localhost:5000
   - Click **Settings** tab
   - Scroll to "Test Email Notification"
   - Enter your email and click "Send Test Email"

---

## 🧪 Quick Test Workflow

**Try this to see everything working:**

1. **Add an employee** (Web)
   - Go to http://localhost:5000
   - Click **Employees** tab
   - Fill in: Name, Email, Department
   - Click "Add Employee"

2. **Create a task** (CLI)
   ```bash
   python cli.py task create \
     --title "Test Task" \
     --assigned-to 1 \
     --due-date 2026-03-31 \
     --priority high
   ```

3. **View tasks** (Web)
   - Click **Tasks** tab
   - See your task listed

4. **Generate report** (Web)
   - Click **Reports** tab
   - Click "Generate Report" → Task Summary
   - Download the Excel file

5. **Check status** (CLI)
   ```bash
   python cli.py health
   ```

---

## ⚠️ Troubleshooting

### "ModuleNotFoundError: flask"
```bash
pip install -r requirements.txt
```

### "Connection refused" 
- Flask server not running
- Run: `python main.py`
- Check port 5000 is available

### "Database connection failed"
- Check `.env` file has correct credentials
- Verify Supabase tables were created
- Try: `python -c "from database import db; print(db.health_check())"`

### "Port 5000 already in use"
```bash
lsof -i :5000  # Find what's using it
# Or run on different port
flask run --port 5001
```

---

## 📁 Project Files Overview

```
SmartBiz/
├── main.py                    # Start here → python main.py
├── cli.py                     # CLI commands
├── database.py                # Supabase connection
├── models.py                  # Data models
├── config.py                  # Settings
├── notifications.py           # Email system
├── reports.py                 # Report generation
├── scheduler.py               # Background jobs
├── templates/dashboard.html   # Web UI
├── .env                       # ✅ Your credentials (created)
├── DATABASE_SETUP.sql         # ✅ Copy this SQL to Supabase
└── requirements.txt           # Python dependencies
```

---

## 🎨 Web Dashboard Features

### 📊 Dashboard Tab
- Overview of your system
- Quick statistics
- Feature highlights

### 👥 Employees Tab
- Add/view/delete employees
- Manage departments

### ✅ Tasks Tab
- Create new tasks
- Assign to employees
- Filter by status
- Update task status
- Set priority and due dates

### 📈 Reports Tab
- Task Summary (Excel with stats)
- Employee Performance (completion rates)
- Currency Rates (for payroll)
- Download reports

### ⚙️ Settings Tab
- System info
- Database status
- Test email notifications

---

## 🔄 Automated Features

Once running, SmartBiz automatically:
- ✅ Checks for overdue tasks (every hour)
- ✅ Sends task reminders (every 30 min)
- ✅ Generates daily reports (every 24 hours)

(Only if email is configured)

---

## 🚀 You're Ready!

**Next command to run:**

```bash
python main.py
```

Then open: **http://localhost:5000** 🌐

**Questions?** Check README.md or QUICKSTART.md

**Deadline reminder:** March 31 at 4:00 PM ⏰

---

**Happy building! 🎉**
