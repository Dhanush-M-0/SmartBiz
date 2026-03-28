import React from 'react'

const SuccessIcon = () => (
  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
  </svg>
)

const ErrorIcon = () => (
  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
  </svg>
)

export function Toast({ message, type = 'success' }) {
  const styles = {
    success: 'bg-secondary-500 dark:bg-secondary-600',
    error: 'bg-danger-500 dark:bg-danger-600',
    info: 'bg-primary-500 dark:bg-primary-600',
  }

  return (
    <div className={`fixed top-4 right-4 ${styles[type] || styles.info} text-white px-5 py-3 rounded-lg shadow-xl flex items-center gap-3 animate-slide-in z-50`}>
      {type === 'success' ? <SuccessIcon /> : <ErrorIcon />}
      <span className="font-medium">{message}</span>
    </div>
  )
}
