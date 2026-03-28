# SmartBiz - Management System

A modern employee and task management application built with **React SPA + Flask REST API**.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![React](https://img.shields.io/badge/React-18-61DAFB.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-000000.svg)
![Tailwind](https://img.shields.io/badge/Tailwind-3.0-38B2AC.svg)

## ✨ Features

- 📊 **Dashboard** - Real-time stats, recent tasks overview
- 👥 **Employee Management** - Full CRUD with search and department filtering
- 📋 **Task Management** - Create, assign, track tasks with status/priority
- 🌙 **Dark Mode** - System-aware theme with manual toggle
- 🔐 **Authentication** - Supabase Auth integration
- 📱 **Responsive** - Works on desktop and mobile

## 🎯 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Supabase account (free tier works)

### 1. Clone and Setup

```bash
git clone https://github.com/Dhanush-M-0/SmartBiz.git
cd SmartBiz
```

### 2. Backend Setup

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your Supabase credentials
```

### 3. Frontend Setup

```bash
cd frontend
npm install

# Copy and configure environment
cp .env.example .env
# Edit .env with your Supabase credentials
```

### 4. Run the Application

**Terminal 1 - Backend (Port 5000):**
```bash
python run.py
# Or for production: gunicorn wsgi:app --bind 0.0.0.0:5000
```

**Terminal 2 - Frontend (Port 5173):**
```bash
cd frontend
npm run dev
```

Visit: `http://localhost:5173`

## 🔧 Environment Variables

### Backend (.env)
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key
FLASK_SECRET_KEY=your-random-secret-key
FLASK_DEBUG=True
```

### Frontend (frontend/.env)
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_KEY=your-anon-public-key
```

## 📁 Project Structure

```
smartbiz/
├── app/                    # Flask Backend
│   ├── api/               # REST API endpoints
│   │   ├── employees.py   # Employee CRUD
│   │   └── tasks.py       # Task CRUD
│   ├── database.py        # Supabase REST client
│   ├── models.py          # Data operations
│   └── config.py          # Configuration
│
├── frontend/              # React SPA
│   ├── src/
│   │   ├── api/          # API client & functions
│   │   ├── context/      # React contexts (Auth, App, Theme)
│   │   ├── components/   # Reusable UI components
│   │   └── pages/        # Page components
│   └── package.json
│
├── run.py                 # Development entry
├── wsgi.py               # Production entry (Gunicorn)
└── requirements.txt      # Python dependencies
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/employees` | List all employees |
| POST | `/api/employees` | Create employee |
| PUT | `/api/employees/:id` | Update employee |
| DELETE | `/api/employees/:id` | Delete employee |
| GET | `/api/tasks` | List tasks (optional `?status=` filter) |
| POST | `/api/tasks` | Create task |
| PUT | `/api/tasks/:id` | Update task |
| DELETE | `/api/tasks/:id` | Delete task |
| GET | `/health` | Liveness check |
| GET | `/ready` | Readiness check |

## 🛠️ Tech Stack

**Frontend:**
- React 18 + Vite
- TailwindCSS 3 (dark mode support)
- React Router 6
- Axios
- Supabase Auth

**Backend:**
- Flask 3.0
- Flask-CORS
- Gunicorn (production)
- Custom Supabase REST client

**Database:**
- Supabase PostgreSQL
- Row Level Security enabled

## 🚀 Deployment

### Backend (Heroku/Railway/Render)
```bash
gunicorn wsgi:app --workers 4 --bind 0.0.0.0:$PORT
```

### Frontend (Vercel/Netlify)
```bash
cd frontend
npm run build
# Deploy the dist/ folder
```

## 🧪 Development

```bash
# Run backend with auto-reload
FLASK_DEBUG=True python run.py

# Run frontend with HMR
cd frontend && npm run dev
```

## 📝 Usage Guide

1. **Sign up** with email on the login page
2. **Dashboard** - View stats and recent tasks
3. **Employees** - Add, edit, delete, and search employees
4. **Tasks** - Create tasks, assign to employees, update status
5. **Dark Mode** - Click the sun/moon icon to toggle theme

## 🔐 Security Notes

- All tables have Row Level Security (RLS) enabled
- CORS configured for allowed origins
- Environment variables for all secrets
- HTTPS enforced in production

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ by SmartBiz Team | March 2026**
