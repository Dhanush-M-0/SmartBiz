import React from 'react'

export function Button({ children, variant = 'primary', size = 'md', ...props }) {
  const baseClass = 'rounded-lg font-medium transition duration-200 flex items-center gap-2'
  const sizeClass = {
    sm: 'px-2 py-1 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg',
  }[size]
  
  const variantClass = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 disabled:bg-blue-300',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 disabled:bg-gray-100',
    danger: 'bg-red-600 text-white hover:bg-red-700 disabled:bg-red-300',
  }[variant]

  return (
    <button className={`${baseClass} ${sizeClass} ${variantClass}`} {...props}>
      {children}
    </button>
  )
}
