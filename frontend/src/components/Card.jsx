import React from 'react'

export function Card({ children, className = '', ...props }) {
  return (
    <div 
      className={`bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6 transition-colors duration-200 ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}
