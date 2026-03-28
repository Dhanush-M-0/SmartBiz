import React, { useEffect, useState } from 'react'
import { Card } from '../components/Card'
import { Button } from '../components/Button'
import { Input, Select } from '../components/Input'
import { useApp } from '../context/AppContext'

const STATUS_OPTIONS = ['Pending', 'In Progress', 'Done']
const PRIORITY_OPTIONS = ['Low', 'Medium', 'High']

export function TasksPage() {
  const { tasks, employees, loading, fetchTasks, fetchEmployees, addTask, updateTaskStatus, deleteTask } = useApp()
  const [showForm, setShowForm] = useState(false)
  const [statusFilter, setStatusFilter] = useState('All')
  const [formData, setFormData] = useState({ title: '', description: '', assigned_to: '', priority: 'Medium', deadline: '' })

  useEffect(() => {
    fetchTasks()
    fetchEmployees()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    await addTask(formData.title, formData.description, formData.assigned_to, formData.priority, formData.deadline)
    setFormData({ title: '', description: '', assigned_to: '', priority: 'Medium', deadline: '' })
    setShowForm(false)
  }

  const filteredTasks = statusFilter === 'All' ? tasks : tasks.filter(t => t.status === statusFilter)

  const getStatusColor = (status) => {
    const colors = {
      'Done': 'bg-secondary-100 dark:bg-secondary-900/50 text-secondary-700 dark:text-secondary-300 border-secondary-200 dark:border-secondary-800',
      'In Progress': 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-700 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800',
      'Pending': 'bg-primary-100 dark:bg-primary-900/50 text-primary-700 dark:text-primary-300 border-primary-200 dark:border-primary-800',
    }
    return colors[status] || colors['Pending']
  }

  const getPriorityColor = (priority) => {
    const colors = {
      'High': 'text-danger-600 dark:text-danger-400',
      'Medium': 'text-yellow-600 dark:text-yellow-400',
      'Low': 'text-gray-500 dark:text-gray-400',
    }
    return colors[priority] || colors['Medium']
  }

  const getPriorityIcon = (priority) => {
    const icons = { 'High': '🔴', 'Medium': '🟡', 'Low': '🟢' }
    return icons[priority] || '🟡'
  }

  return (
    <div className="space-y-6">
      {/* Header Actions */}
      <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
        <Button onClick={() => setShowForm(true)} variant="primary">
          <span>➕</span> New Task
        </Button>
        
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500 dark:text-gray-400">Filter:</span>
          <div className="flex rounded-lg overflow-hidden border border-gray-300 dark:border-gray-600">
            {['All', ...STATUS_OPTIONS].map((status) => (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                className={`px-4 py-2 text-sm font-medium transition-colors ${
                  statusFilter === status
                    ? 'bg-primary-600 text-white'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                {status}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Form Modal */}
      {showForm && (
        <Card>
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-6">
            ➕ Create New Task
          </h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Task Title"
              placeholder="e.g., Complete project documentation"
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              required
            />
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                Description
              </label>
              <textarea
                className="w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
                rows="3"
                placeholder="Add details about this task..."
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
              />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Select
                label="Assign To"
                value={formData.assigned_to}
                onChange={(e) => setFormData({...formData, assigned_to: e.target.value})}
              >
                <option value="">Unassigned</option>
                {employees.map(emp => (
                  <option key={emp.id} value={emp.id}>{emp.name}</option>
                ))}
              </Select>
              
              <Select
                label="Priority"
                value={formData.priority}
                onChange={(e) => setFormData({...formData, priority: e.target.value})}
              >
                {PRIORITY_OPTIONS.map(p => (
                  <option key={p} value={p}>{p}</option>
                ))}
              </Select>
              
              <Input
                label="Deadline"
                type="date"
                value={formData.deadline}
                onChange={(e) => setFormData({...formData, deadline: e.target.value})}
                required
              />
            </div>
            
            <div className="flex gap-3 pt-2">
              <Button type="submit" variant="primary" disabled={loading}>
                {loading ? 'Creating...' : 'Create Task'}
              </Button>
              <Button type="button" variant="ghost" onClick={() => setShowForm(false)}>
                Cancel
              </Button>
            </div>
          </form>
        </Card>
      )}

      {/* Tasks List */}
      <Card>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white">
            Tasks ({filteredTasks.length})
          </h3>
        </div>
        
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          </div>
        ) : filteredTasks.length === 0 ? (
          <div className="text-center py-8">
            <span className="text-4xl mb-2 block">📋</span>
            <p className="text-gray-500 dark:text-gray-400">
              {statusFilter !== 'All' ? `No ${statusFilter.toLowerCase()} tasks` : 'No tasks yet. Create your first task!'}
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredTasks.map(task => (
              <div 
                key={task.id} 
                className={`p-4 rounded-lg border-l-4 bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors ${getStatusColor(task.status)}`}
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="text-sm">{getPriorityIcon(task.priority)}</span>
                      <h4 className="font-medium text-gray-800 dark:text-white">{task.title}</h4>
                    </div>
                    {task.description && (
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{task.description}</p>
                    )}
                    <div className="flex flex-wrap items-center gap-4 mt-2 text-xs text-gray-500 dark:text-gray-400">
                      <span>📅 {task.deadline ? new Date(task.deadline).toLocaleDateString() : 'No deadline'}</span>
                      <span className={getPriorityColor(task.priority)}>⚡ {task.priority}</span>
                      {task.assigned_to && (
                        <span>👤 {employees.find(e => e.id === task.assigned_to)?.name || 'Assigned'}</span>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <select
                      value={task.status}
                      onChange={(e) => updateTaskStatus(task.id, e.target.value)}
                      className="px-3 py-1.5 text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                    >
                      {STATUS_OPTIONS.map(s => (
                        <option key={s} value={s}>{s}</option>
                      ))}
                    </select>
                    <Button variant="danger" size="sm" onClick={() => deleteTask(task.id)}>
                      🗑️
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}
