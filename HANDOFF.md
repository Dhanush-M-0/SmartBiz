# 🚀 SmartBiz Project Handoff Guide

## Current Status: MVP Built ✅

**Project:** React SPA + Flask REST API for employee & task management
**Started:** March 26, 2026
**Status:** MVP complete, testing phase with integration issues
**Environment:** GitHub Codespaces

---

## 📊 What's Been Built

### ✅ Backend (Flask REST API)
- **Directory:** `/app/`
- **Entry Point:** `run.py` (dev), `wsgi.py` (production)
- **Framework:** Flask 3.0 with Blueprints
- **Database:** Supabase PostgreSQL (direct REST API client)

**API Endpoints Created:**
```
GET  /api/employees              - List employees
POST /api/employees              - Create employee
PUT  /api/employees/:id          - Update employee
DELETE /api/employees/:id        - Delete employee

GET  /api/tasks                  - List tasks (with status filter)
POST /api/tasks                  - Create task
PUT  /api/tasks/:id              - Update task
DELETE /api/tasks/:id            - Delete task

GET  /health                     - Liveness check
GET  /ready                      - Readiness check
```

**Key Files:**
- `app/api/employees.py` - Employee endpoints (CRUD working)
- `app/api/tasks.py` - Task endpoints (CRUD working)
- `app/database.py` - **CUSTOM REST client** (NOT official SDK)
- `app/models.py` - Data operations (simplified queries)
- `app/config.py` - Environment configuration
- `app/__init__.py` - App factory with Blueprints

**Important:** Database client was switched to **custom REST API client** because official Supabase SDK rejected the anon key. Custom client directly uses Supabase REST API endpoints.

### ✅ Frontend (React SPA with Vite)
- **Directory:** `/frontend/`
- **Build Tool:** Vite (fast HMR)
- **Framework:** React 18
- **Styling:** Tailwind CSS v3
- **State:** Context API + React Hooks
- **Auth:** Supabase Auth

**5 Pages Built:**
1. **LoginPage** - Email/password Supabase login
2. **SignupPage** - User registration
3. **DashboardPage** - Stats, recent tasks (NOT WORKING - data not loading)
4. **EmployeesPage** - Employee CRUD operations
5. **TasksPage** - Task management with status filter

**Key Files:**
- `src/App.jsx` - Main app with routing
- `src/context/AuthContext.jsx` - Supabase auth state
- `src/context/AppContext.jsx` - Global app state (employees, tasks)
- `src/api/client.js` - **Axios instance with AUTO JWT injection**
- `src/api/employees.js` - Employee API calls
- `src/api/tasks.js` - Task API calls
- `src/components/` - Reusable UI components (Button, Input, Card, Toast, Layout, ProtectedRoute)
- `src/pages/` - Page components

---

## ⚠️ Current Issues (BLOCKING)

### Issue 1: Frontend Data Not Loading ❌
**Symptom:** Dashboard shows 0 employees (should show 4), dropdown empty
**Root Cause:** API URL config issue or network communication problem
**Files Involved:**
- `frontend/.env` - Check `VITE_API_URL`
- `src/api/client.js` - Axios baseURL logic

**Last Status:**
- Backend API working: `curl http://localhost:5000/api/employees` returns 4 employees ✅
- Frontend not fetching data ❌
- Updated `.env` to use Codespaces URL but never verified it worked after restart

### Issue 2: Supabase Query URL Encoding ⚠️
**Symptom:** Sometimes "400 Bad Request" errors for SELECT queries
**Root Cause:** URL encoding of special characters (%, commas, etc.) in query strings
**Files:** `app/database.py` line 80-125

**Previous Fix:** Removed nested `employees(name, email, department)` joins from queries - now select just `*` and merge data in application layer

### Issue 3: RLS Policies Might Be Blocking Inserts ❌
**Last Action:** Created INSERT policies but never verified they work
**Supabase Dashboard Action Needed:**
```sql
-- Check current policies
SELECT * FROM pg_policies WHERE tablename IN ('employees', 'tasks');

-- If INSERT failing, ensure policies allow anon key
CREATE POLICY "employees_insert_all" ON public.employees
  FOR INSERT
  WITH CHECK (true);
```

---

## 🔧 Configuration Details

### Backend Setup
**File:** `.env`
```env
SUPABASE_URL=https://dasuomsluytkgcjondne.supabase.co
SUPABASE_KEY=sb_publishable_KNbhCjeN41koQYpxm3AnSg_8ZXzt3zG
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=smartbiz-dev-secret-key-2026
```

**Database Client:**
- Custom REST client at `app/database.py` lines 1-133
- **NOT using** official `supabase-py` SDK (it rejects the key)
- **USING** direct HTTP requests with `requests` library
- Headers: `apikey` and `Content-Type: application/json`
- Base URL: `https://dasuomsluytkgcjondne.supabase.co/rest/v1`

### Frontend Setup
**File:** `frontend/.env`
```env
VITE_SUPABASE_URL=https://dasuomsluytkgcjondne.supabase.co
VITE_SUPABASE_KEY=sb_publishable_KNbhCjeN41koQYpxm3AnSg_8ZXzt3zG
VITE_API_URL=https://fictional-space-barnacle-jjw94vjjwp4jhj569-5000.app.github.dev/api
```

**Note on VITE_API_URL:** Must be Codespaces public URL (https://...) NOT localhost:5000

---

## 🎯 What the Next Session Should Fix

### Priority 1: Frontend Data Loading (CRITICAL)
1. **Verify Frontend can reach Backend:**
   ```bash
   curl https://fictional-space-barnacle-jjw94vjjwp4jhj569-5000.app.github.dev/api/employees
   ```

2. **Debug Frontend API calls:**
   - Open browser DevTools (F12)
   - Go to Network tab
   - Refresh dashboard page
   - Check if API calls are being made
   - Check response status and body

3. **Check Axios Client:**
   - Verify `VITE_API_URL` is loaded correctly
   - Check if auth headers are attached
   - Verify response format matches expected `{ success, data }`

4. **Fix Data Binding:**
   - Ensure `AppContext.fetchEmployees()` is called on DashboardPage mount
   - Verify state is being set correctly
   - Check React DevTools to see state values

### Priority 2: Test Employee Add/Edit/Delete
- Try adding an employee in frontend
- Verify it shows in list immediately
- Verify backend saved to Supabase
- Test edit and delete

### Priority 3: Test Task Creation
- Go to Tasks page
- Create a new task
- Verify employee dropdown populated
- Verify task appears in list
- Test status updates

### Priority 4: Full Integration Test
- Dashboard stats should update when adding employees/tasks
- Logout should clear session
- Re-login should load data
- All CRUD operations working end-to-end

---

## 🗂️ Supabase Schema

**Tables Created:** 3

### employees
```sql
id (UUID, PK)          -- Auto generated
name (TEXT, NOT NULL)  -- Employee name
email (TEXT, UNIQUE)   -- Email address
department (TEXT)      -- Department name
created_at (TIMESTAMP) -- Auto timestamp
```

### tasks
```sql
id (UUID, PK)                     -- Auto generated
title (TEXT, NOT NULL)            -- Task title
description (TEXT)                -- Task description
assigned_to (UUID, FK)            -- Reference to employees
status (TEXT, DEFAULT 'Pending')  -- Pending/In Progress/Done
priority (TEXT, DEFAULT 'Medium') -- Low/Medium/High
deadline (DATE, NOT NULL)         -- Deadline date
created_at (TIMESTAMP)            -- Auto timestamp
```

### reports_log
```sql
id (UUID, PK)         -- Auto generated
report_type (TEXT)    -- Report type
file_name (TEXT)      -- File name
generated_at (TIMESTAMP) -- Auto timestamp
```

**RLS Status:** All enabled, policies created (but may need adjustment for INSERT)

---

## 💾 Dependencies Overview

**Python (requirements.txt):**
- flask==3.0.3
- flask-cors==4.0.0
- gunicorn==22.0.0
- supabase==2.4.6 *(installed but NOT used)*
- python-dotenv==1.0.1
- pandas==2.2.2
- openpyxl==3.1.2
- requests==2.31.0
- schedule==1.2.1
- PyJWT==2.8.1

**JavaScript (frontend/package.json):**
- react@latest
- react-dom@latest
- react-router-dom@latest
- @supabase/supabase-js@latest
- axios@latest
- tailwindcss@3
- vite@latest

---

## 🚀 How to Run for Next Session

**Terminal 1 - Backend:**
```bash
cd /workspaces/SmartBiz
python run.py
# Runs on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd /workspaces/SmartBiz/frontend
npm run dev
# Runs on http://localhost:5173 (local) or Codespaces URL
```

**Accessing in Codespaces:**
- Frontend: https://fictional-space-barnacle-jjw94vjjwp4jhj569-5173.app.github.dev/
- Backend: https://fictional-space-barnacle-jjw94vjjwp4jhj569-5000.app.github.dev/

---

## 🔑 Key Decisions Made

1. **Custom REST Client:** Official Supabase SDK rejected the anon key, so custom REST client built
2. **Context API:** No Redux/Zustand - simple Context API for state management
3. **Tailwind CSS v3:** Had to downgrade from v4 due to PostCSS plugin issues
4. **Vite over CRA:** Faster HMR and smaller bundle size
5. **Direct REST calls:** No ORM - direct Supabase REST API
6. **Simplified queries:** Removed joins/nested selects due to URL encoding issues

---

## 📋 Checklist for Next Session

- [ ] Verify backend API returning correct data
- [ ] Debug frontend network requests (DevTools)
- [ ] Fix API URL configuration if needed
- [ ] Test employee add/edit/delete
- [ ] Test task creation and status updates
- [ ] Test dashboard stats updating correctly
- [ ] Verify RLS policies allow all operations
- [ ] Full end-to-end test
- [ ] Document any additional issues found
- [ ] Plan Phase 2 features (Kanban, charts, reports)

---

## 📞 Emergency Contacts

**If Backend crashes:**
- Check logs: `tail -f /tmp/backend.log`
- Restart: `pkill -f 'python run.py'` then `python run.py`
- Verify Supabase: `curl https://dasuomsluytkgcjondne.supabase.co/rest/v1/employees?select=* -H "apikey: sb_publishable_KNbhCjeN41koQYpxm3AnSg_8ZXzt3zG"`

**If Frontend not loading:**
- Hard refresh: Ctrl+Shift+R
- Clear cache: DevTools → Application → Clear Site Data
- Rebuild: `cd frontend && npm run build`

**If API calls failing:**
- Check CORS: In browser DevTools check headers
- Check VITE_API_URL: Ensure it's correct Codespaces URL
- Check backend responding: `curl http://localhost:5000/health`

---

**Generation Date:** March 28, 2026
**Status:** Ready for next session with known issues documented
