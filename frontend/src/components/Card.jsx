import React from 'react'

export function Card({ children, ...props }) {
  return (
    <div className="card" {...props}>
      {children}
    </div>
  )
}
