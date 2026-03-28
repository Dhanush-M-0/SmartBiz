import React, { useEffect } from 'react'
import { Card } from '../components/Card'
import { useApp } from '../context/AppContext'

function StatCard({ title, value, color, icon }) {
  const colorClasses = {
    blue: 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/30',
    yellow: 'text-yellow-600 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-900/30',
    green: 'text-secondary-600 dark:text-secondary-400 bg-secondary-50 dark:bg-secondary-900/30',
    purple: 'text-purple-600 dark:text-purple-400 bg-purple-50 dark:bg-purple-900/30',
  }
  
  return (
    <Card className="hover:shadow-md transition-shadow">
      <div className="flex items-center gap-4">
        <div className={`w-14 h-14 rounded-xl flex items-center justify-center ${colorClasses[color]}`}>
          <span className="text-2xl">{icon}</span>
        </div>
        <div>
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">{title}</p>
          <p className={`text-3xl font-bold ${colorClasses[color].split(' ')[0]}`}>{value}</p>
        </div>
      </div>
    </Card>
  )
}

export function DashboardPage() {
  const { employees, tasks, fetchEmployees, fetchTasks, loading } = useApp()

  useEffect(() => {
    fetchEmployees()
    fetchTasks()
  }, [])

  const totalTasks = tasks.length
  const pendingTasks = tasks.filter(t => t.status === 'Pending').length
  const inProgressTasks = tasks.filter(t => t.status === 'In Progress').length
  const doneTasks = tasks.filter(t => t.status === 'Done').length
  const totalEmployees = employees.length

  const getStatusBadge = (status) => {
    const styles = {
      'Done': 'bg-secondary-100 dark:bg-secondary-900/50 text-secondary-700 dark:text-secondary-300',
      'In Progress': 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-700 dark:text-yellow-300',
      'Pending': 'bg-primary-100 dark:bg-primary-900/50 text-primary-700 dark:text-primary-300',
    }
    return styles[status] || styles['Pending']
  }

  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Total Tasks" value={totalTasks} color="blue" icon="📋" />
        <StatCard title="Pending" value={pendingTasks} color="yellow" icon="⏳" />
        <StatCard title="Completed" value={doneTasks} color="green" icon="✅" />
        <StatCard title="Employees" value={totalEmployees} color="purple" icon="👥" />
      </div>

      {/* Recent Tasks */}
      <Card>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white">Recent Tasks</h3>
          {inProgressTasks > 0 && (
            <span className="px-3 py-1 text-xs font-medium rounded-full bg-yellow-100 dark:bg-yellow-900/50 text-yellow-700 dark:text-yellow-300">
              {inProgressTasks} in progress
            </span>
          )}
        </div>
        
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          </div>
        ) : tasks.length === 0 ? (
          <div className="text-center py-8">
            <span className="text-4xl mb-2 block">📝</span>
            <p className="text-gray-500 dark:text-gray-400">No tasks yet. Create your first task!</p>
          </div>
        ) : (
          <div className="space-y-3">
            {tasks.slice(0, 5).map(task => (
              <div 
                key={task.id} 
                className="flex justify-between items-center p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-800 dark:text-white truncate">{task.title}</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {task.deadline ? `Due: ${new Date(task.deadline).toLocaleDateString()}` : 'No deadline'}
                  </p>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusBadge(task.status)}`}>
                  {task.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}
