import React, { useEffect } from 'react'
import { Card } from '../components/Card'
import { useApp } from '../context/AppContext'

export function DashboardPage() {
  const { employees, tasks, fetchEmployees, fetchTasks, loading } = useApp()

  useEffect(() => {
    fetchEmployees()
    fetchTasks()
  }, [])

  const totalTasks = tasks.length
  const pendingTasks = tasks.filter(t => t.status === 'Pending').length
  const doneTasks = tasks.filter(t => t.status === 'Done').length
  const totalEmployees = employees.length

  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <div className="text-center">
            <p className="text-gray-600 text-sm">Total Tasks</p>
            <p className="text-4xl font-bold text-blue-600">{totalTasks}</p>
          </div>
        </Card>
        <Card>
          <div className="text-center">
            <p className="text-gray-600 text-sm">Pending</p>
            <p className="text-4xl font-bold text-yellow-600">{pendingTasks}</p>
          </div>
        </Card>
        <Card>
          <div className="text-center">
            <p className="text-gray-600 text-sm">Completed</p>
            <p className="text-4xl font-bold text-green-600">{doneTasks}</p>
          </div>
        </Card>
        <Card>
          <div className="text-center">
            <p className="text-gray-600 text-sm">Employees</p>
            <p className="text-4xl font-bold text-purple-600">{totalEmployees}</p>
          </div>
        </Card>
      </div>

      {/* Recent Tasks */}
      <Card>
        <h3 className="text-xl font-bold mb-4 text-gray-800">Recent Tasks</h3>
        {loading ? (
          <p>Loading...</p>
        ) : tasks.length === 0 ? (
          <p className="text-gray-500">No tasks yet</p>
        ) : (
          <div className="space-y-2">
            {tasks.slice(0, 5).map(task => (
              <div key={task.id} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                <div>
                  <p className="font-medium text-gray-800">{task.title}</p>
                  <p className="text-sm text-gray-600">{task.employees?.name || 'Unassigned'}</p>
                </div>
                <span className={`px-2 py-1 rounded text-sm font-medium ${
                  task.status === 'Done' ? 'bg-green-100 text-green-800' :
                  task.status === 'In Progress' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-blue-100 text-blue-800'
                }`}>
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
