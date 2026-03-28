import React from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Button } from './Button'

export function Layout({ children }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  if (!user) {
    return <>{children}</>
  }

  const isActive = (path) => location.pathname === path ? 'bg-blue-700' : 'hover:bg-blue-600'

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-blue-600 text-white shadow-lg">
        <div className="p-6">
          <h1 className="text-2xl font-bold">SmartBiz</h1>
          <p className="text-blue-200 text-sm">Management System</p>
        </div>

        <nav className="mt-8 space-y-2">
          <Link to="/" className={`block px-4 py-2 ${isActive('/')}`}>📊 Dashboard</Link>
          <Link to="/employees" className={`block px-4 py-2 ${isActive('/employees')}`}>👥 Employees</Link>
          <Link to="/tasks" className={`block px-4 py-2 ${isActive('/tasks')}`}>📋 Tasks</Link>
        </nav>

        <div className="absolute bottom-0 w-64 p-4 border-t border-blue-500">
          <p className="text-sm text-blue-200 mb-4">👤 {user.email}</p>
          <Button onClick={handleLogout} variant="secondary" size="sm" className="w-full">
            Logout
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="bg-white shadow p-6">
          <h2 className="text-2xl font-bold text-gray-800">
            {location.pathname === '/' && 'Dashboard'}
            {location.pathname === '/employees' && 'Employees'}
            {location.pathname === '/tasks' && 'Tasks'}
          </h2>
        </div>
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
