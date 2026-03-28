import React from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTheme } from '../context/ThemeContext'
import { useApp } from '../context/AppContext'
import { Button } from './Button'
import { Toast } from './Toast'

// Icons as simple SVG components
const SunIcon = () => (
  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
  </svg>
)

const MoonIcon = () => (
  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
  </svg>
)

export function Layout({ children }) {
  const { user, logout } = useAuth()
  const { darkMode, toggleTheme } = useTheme()
  const { toast } = useApp()
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  if (!user) {
    return <>{children}</>
  }

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/employees', label: 'Employees', icon: '👥' },
    { path: '/tasks', label: 'Tasks', icon: '📋' },
  ]

  const isActive = (path) => location.pathname === path

  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900 transition-colors duration-200">
      {/* Sidebar */}
      <div className="w-64 bg-gradient-to-b from-primary-600 to-primary-800 dark:from-gray-800 dark:to-gray-900 text-white shadow-xl flex flex-col">
        <div className="p-6 border-b border-primary-500 dark:border-gray-700">
          <h1 className="text-2xl font-bold tracking-tight">Smart<span className="text-primary-200 dark:text-primary-400">Biz</span></h1>
          <p className="text-primary-200 dark:text-gray-400 text-sm mt-1">Management System</p>
        </div>

        <nav className="flex-1 mt-6 px-3 space-y-1">
          {navItems.map(({ path, label, icon }) => (
            <Link
              key={path}
              to={path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                isActive(path)
                  ? 'bg-white/20 dark:bg-gray-700 shadow-lg'
                  : 'hover:bg-white/10 dark:hover:bg-gray-700/50'
              }`}
            >
              <span className="text-xl">{icon}</span>
              <span className="font-medium">{label}</span>
            </Link>
          ))}
        </nav>

        <div className="p-4 border-t border-primary-500 dark:border-gray-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-full bg-primary-400 dark:bg-gray-600 flex items-center justify-center">
              <span className="text-lg">👤</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{user.email?.split('@')[0]}</p>
              <p className="text-xs text-primary-200 dark:text-gray-400 truncate">{user.email}</p>
            </div>
          </div>
          <Button onClick={handleLogout} variant="secondary" size="sm" className="w-full">
            Sign Out
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white dark:bg-gray-800 shadow-sm px-6 py-4 flex items-center justify-between transition-colors duration-200">
          <div>
            <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
              {navItems.find(item => item.path === location.pathname)?.label || 'SmartBiz'}
            </h2>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
            </p>
          </div>
          
          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors duration-200"
            aria-label="Toggle theme"
          >
            {darkMode ? <SunIcon /> : <MoonIcon />}
          </button>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 overflow-auto p-6 bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
          {children}
        </main>
      </div>

      {/* Toast Notifications */}
      {toast && <Toast message={toast.message} type={toast.type} />}
    </div>
  )
}
