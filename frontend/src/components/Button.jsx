import React from 'react'

export function Button({ children, variant = 'primary', size = 'md', className = '', ...props }) {
  const baseClass = 'rounded-lg font-medium transition-all duration-200 flex items-center justify-center gap-2 focus:outline-none focus:ring-2 focus:ring-offset-2 dark:focus:ring-offset-gray-800'
  
  const sizeClass = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg',
  }[size]
  
  const variantClass = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500 disabled:bg-primary-300 dark:disabled:bg-primary-800',
    secondary: 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600 focus:ring-gray-500 disabled:bg-gray-100 dark:disabled:bg-gray-800',
    danger: 'bg-danger-600 text-white hover:bg-danger-700 focus:ring-danger-500 disabled:bg-danger-300',
    ghost: 'bg-transparent text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 focus:ring-gray-500',
  }[variant]

  return (
    <button className={`${baseClass} ${sizeClass} ${variantClass} ${className}`} {...props}>
      {children}
    </button>
  )
}
