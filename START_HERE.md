# 🎯 SmartBiz - Final Setup (Last 3 Steps!)

You're almost there! Follow these final steps to get SmartBiz running.

---

## ⚡ Step 1: Run the Auto-Installer (1 command!)

```bash
python main.py
```

**What happens:**
- ✅ Automatically checks for missing dependencies
- ✅ Installs them if needed (2-5 minutes)
- ✅ Starts the web server
- ✅ Displays: `🌐 Access at: http://localhost:5000`

**If it works:** Skip to Step 3 below!

**If you see database errors:** Go to Step 2.

---

## ⚡ Step 2: Setup Supabase Tables (2 minutes)

1. **Open Supabase Dashboard:**
   - Go to: https://app.supabase.com
   - Select your project: `dasuomsluytkgcjondne`

2. **Create Tables:**
   - Click **SQL Editor** (left sidebar)
   - Click **New Query**
   - Copy all SQL from [DATABASE_SETUP.sql](DATABASE_SETUP.sql)
   - Paste into the editor
   - Click **Run** button

3. **Verify:**
   - You should see: ✅ 4 tables created

---

## ⚡ Step 3: Run the App

In your terminal:

```bash
python main.py
```

Expected output:
```
✅ Checking dependencies...
✅ Flask
✅ Flask-CORS
✅ Supabase
... (all packages)
✅ All dependencies installed!

============================================================
🌐 SmartBiz Web Server
============================================================

✅ Starting server...
📍 Access at: http://localhost:5000
🔴 Press Ctrl+C to stop
```

---

## 🎮 Access SmartBiz

Open your browser:
### **http://localhost:5000** 🚀

You'll see:
- 📊 Dashboard with employee stats
- 👥 Employee management
- ✅ Task creation & tracking
- 📈 Report generation
- ⚙️ System settings

---

## 🧪 Quick Test (Try These!)

### 1. Add an Employee
- Click **Employees** tab
- Fill in: Name, Email, Department
- Click "Add Employee"

### 2. Create a Task
```bash
# In another terminal
python cli.py task create \
  --title "My First Task" \
  --assigned-to 1 \
  --due-date 2026-03-31 \
  --priority high
```

### 3. View Tasks
- Click **Tasks** tab in the web interface
- See your task listed

### 4. Generate Report
- Click **Reports** tab
- Click "Generate Report" → Task Summary
- Download the Excel file

### 5. Check Health
```bash
python cli.py health
```

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: flask" when running main.py
- This means auto-installer failed
- Try manually:
  ```bash
  pip install -r requirements.txt
  ```
- Or use minimal:
  ```bash
  pip install -r requirements-minimal.txt
  ```

### "Database connection failed"
- Supabase tables not created yet
- Follow Step 2 above

### "Port 5000 already in use"
```bash
# Find what's using it
lsof -i :5000

# Or use different port
flask run --port 5001
```

### App starts but dashboard won't load
- Make sure you created the Supabase tables (Step 2)
- Check .env file has your credentials

---

## 📋 Files Reference

```
SmartBiz/
├── main.py                    ← RUN THIS (auto-installs deps)
├── cli.py                     ← Command-line interface
├── DATABASE_SETUP.sql         ← Copy this to Supabase
├── requirements.txt           ← Python packages list
├── .env                       ← Your Supabase credentials
├── templates/dashboard.html   ← Web UI
└── [other backend files]
```

---

## 🎬 Quick Start Command Cheat Sheet

```bash
# Start the web server (auto-installs if needed)
python main.py

# List all employees
python cli.py employee list

# Add new employee
python cli.py employee add --name "John" --email "john@example.com" --department "Engineering"

# Create task
python cli.py task create --title "Task Name" --assigned-to 1 --due-date 2026-03-31

# List tasks
python cli.py task list

# Check system health
python cli.py health

# Generate reports
python cli.py report tasks-summary
```

---

## 📚 Need More Help?

- **Installation Issues?** → See INSTALL_HELP.md
- **Manual Commands?** → See MANUAL_COMMANDS.md
- **Full Documentation?** → See README.md
- **Supabase Setup?** → See SETUP_READY.md

---

## ✨ You're Ready!

**Just run:** `python main.py`

Then open: **http://localhost:5000**

That's it! 🎉

---

**Questions? Check the troubleshooting section above or read the referenced guide files.**

**Remember: Deadline is March 31 at 4:00 PM ⏰**
