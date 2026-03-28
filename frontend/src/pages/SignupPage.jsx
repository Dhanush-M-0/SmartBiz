import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTheme } from '../context/ThemeContext'
import { Button } from '../components/Button'
import { Input } from '../components/Input'

export function SignupPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [localError, setLocalError] = useState('')
  const [loading, setLoading] = useState(false)
  const { signup, error } = useAuth()
  const { darkMode, toggleTheme } = useTheme()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLocalError('')
    
    if (password !== confirmPassword) {
      setLocalError('Passwords do not match')
      return
    }
    
    if (password.length < 6) {
      setLocalError('Password must be at least 6 characters')
      return
    }
    
    setLoading(true)
    const success = await signup(email, password)
    if (success) {
      navigate('/login')
    }
    setLoading(false)
  }

  const displayError = localError || error

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-600 to-primary-900 dark:from-gray-800 dark:to-gray-900 transition-colors duration-300">
      {/* Theme Toggle */}
      <button
        onClick={toggleTheme}
        className="absolute top-4 right-4 p-2 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-colors"
        aria-label="Toggle theme"
      >
        {darkMode ? '☀️' : '🌙'}
      </button>

      <div className="w-full max-w-md px-4">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 transition-colors duration-300">
          {/* Logo */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold">
              <span className="text-primary-600 dark:text-primary-400">Smart</span>
              <span className="text-gray-800 dark:text-white">Biz</span>
            </h1>
            <p className="text-gray-500 dark:text-gray-400 mt-2">Create your account</p>
          </div>
          
          {displayError && (
            <div className="bg-danger-50 dark:bg-danger-900/30 text-danger-700 dark:text-danger-300 p-4 rounded-lg mb-6 text-sm">
              {displayError}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <Input
              label="Email Address"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <Input
              label="Password"
              type="password"
              placeholder="At least 6 characters"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <Input
              label="Confirm Password"
              type="password"
              placeholder="••••••••"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
            
            <Button type="submit" variant="primary" className="w-full py-3" disabled={loading}>
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
                  Creating account...
                </span>
              ) : 'Create Account'}
            </Button>
          </form>

          <div className="mt-8 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              Already have an account?{' '}
              <Link to="/login" className="text-primary-600 dark:text-primary-400 hover:underline font-medium">
                Sign in
              </Link>
            </p>
          </div>
        </div>
        
        <p className="text-center text-white/60 text-sm mt-6">
          © 2026 SmartBiz. Employee & Task Management.
        </p>
      </div>
    </div>
  )
}
