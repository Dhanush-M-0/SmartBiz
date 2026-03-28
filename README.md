# SmartBiz - Management System

A modern employee and task management application built with **React SPA + Flask REST API**.

## 🎯 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Supabase account (free tier)

### Environment Setup

**Backend (.env):**
```env
SUPABASE_URL=https://dasuomsluytkgcjondne.supabase.co
SUPABASE_KEY=sb_publishable_KNbhCjeN41koQYpxm3AnSg_8ZXzt3zG
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=smartbiz-dev-secret-key-2026
```

**Frontend (.env):**
```env
VITE_SUPABASE_URL=https://dasuomsluytkgcjondne.supabase.co
VITE_SUPABASE_KEY=sb_publishable_KNbhCjeN41koQYpxm3AnSg_8ZXzt3zG
VITE_API_URL=https://fictional-space-barnacle-jjw94vjjwp4jhj569-5000.app.github.dev/api
```

### Running Locally

**Terminal 1 - Backend (Port 5000):**
```bash
python run.py
```

**Terminal 2 - Frontend (Port 5173):**
```bash
cd frontend
npm run dev
```

Visit: `http://localhost:5173`

### Running in Codespaces

**Frontend:** https://fictional-space-barnacle-jjw94vjjwp4jhj569-5173.app.github.dev/
**Backend:** https://fictional-space-barnacle-jjw94vjjwp4jhj569-5000.app.github.dev/

## 📁 Project Structure

```
smartbiz/
├── app/                          # Flask Backend
│   ├── api/                      # REST API Blueprints
│   │   ├── employees.py         # Employee CRUD endpoints
│   │   ├── tasks.py             # Task CRUD endpoints
│   │   └── __init__.py          # Blueprint registry
│   ├── __init__.py              # App factory
│   ├── config.py                # Configuration
│   ├── database.py              # Supabase REST client
│   ├── models.py                # Data operations
│   ├── routes.py                # HTML routes (old)
│   ├── scheduler.py             # Background jobs
│   ├── notifier.py              # Email notifications
│   ├── reports.py               # Report generation
│   └── api_service.py           # External APIs
│
├── frontend/                     # React SPA
│   ├── src/
│   │   ├── api/                 # API client & functions
│   │   ├── context/             # Global state (Auth, App)
│   │   ├── pages/               # Page components
│   │   ├── components/          # Reusable components
│   │   ├── App.jsx              # Main app with routing
│   │   ├── main.jsx             # React entry point
│   │   └── index.css            # Tailwind styles
│   ├── .env                     # Environment variables
│   ├── vite.config.js           # Vite config
│   ├── tailwind.config.js       # Tailwind config
│   └── package.json             # Dependencies
│
├── run.py                        # Development entry point
├── wsgi.py                       # Production entry point (Gunicorn)
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container image
├── docker-compose.yml           # Local dev containers
└── Procfile                     # Platform deployment
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/employees` | List all employees |
| POST | `/api/employees` | Create employee |
| PUT | `/api/employees/:id` | Update employee |
| DELETE | `/api/employees/:id` | Delete employee |
| GET | `/api/tasks` | List all tasks |
| GET | `/api/tasks?status=Pending` | Filter by status |
| POST | `/api/tasks` | Create task |
| PUT | `/api/tasks/:id` | Update task |
| DELETE | `/api/tasks/:id` | Delete task |
| GET | `/health` | Health check |
| GET | `/ready` | Readiness check |

## 🛠️ Tech Stack

**Frontend:**
- React 18 + Vite
- TailwindCSS
- React Router
- Axios
- Supabase Auth

**Backend:**
- Flask 3.0
- Flask-CORS
- Supabase (REST API directly)
- Pandas (reports)
- APScheduler (background jobs)

**Database:**
- Supabase PostgreSQL
- RLS Policies enabled

**Deployment:**
- Gunicorn (production WSGI)
- Docker/Docker Compose
- Heroku/Railway/Render compatible

## 🚀 Deployment

**Backend to Heroku/Railway:**
```bash
gunicorn wsgi:app --workers 4 --bind 0.0.0.0:5000
```

**Frontend to Vercel:**
```bash
npm run build
```

## 🔍 Current Status

✅ **MVP Complete**
- React SPA with 5 pages (Login, Signup, Dashboard, Employees, Tasks)
- Flask REST API with full CRUD
- Supabase integration working
- Authentication with Supabase Auth
- Tailwind CSS styling

⚠️ **Known Issues**
- Frontend not loading employee data on dashboard (API URL config issue in Codespaces)
- Need to verify RLS policies allow INSERT operations

❌ **Not Yet Implemented (Phase 2)**
- Kanban board for tasks
- Dashboard charts/graphs
- Report generation & downloads
- Currency converter
- Email notifications
- Advanced filtering/search

## 📝 Usage

1. **Sign up** with email at login page
2. **Dashboard** - View stats (employees, task counts)
3. **Employees** - Add/Edit/Delete employees
4. **Tasks** - Create tasks, assign to employees, change status
5. **Logout** - Clear auth session

## 🔐 Security

- RLS Policies enabled on all tables
- CORS configured for Codespaces URLs
- Environment variables for secrets
- HTTPS enforced in production
- Session cookies with security flags

## 📞 Support

For issues or questions, refer to:
- Backend logs: `python run.py` output
- Frontend console: Browser DevTools (F12)
- Network tab: Check API calls to backend

---

**Last Updated:** March 28, 2026
