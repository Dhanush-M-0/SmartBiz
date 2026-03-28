import React, { useEffect, useState } from 'react'
import { Card } from '../components/Card'
import { Button } from '../components/Button'
import { Input } from '../components/Input'
import { useApp } from '../context/AppContext'
import { Toast } from '../components/Toast'

export function TasksPage() {
  const { tasks, employees, loading, toast, fetchTasks, fetchEmployees, addTask, updateTaskStatus, deleteTask } = useApp()
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

  return (
    <div className="space-y-6">
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => {}} />}

      <div className="flex gap-4">
        <Button onClick={() => setShowForm(true)} variant="primary">
          ➕ Add Task
        </Button>
        <select 
          value={statusFilter} 
          onChange={(e) => setStatusFilter(e.target.value)}
          className="input-field"
        >
          <option>All</option>
          <option>Pending</option>
          <option>In Progress</option>
          <option>Done</option>
        </select>
      </div>

      {/* Form Modal */}
      {showForm && (
        <Card className="bg-white">
          <h3 className="text-xl font-bold mb-4">Add Task</h3>
          <form onSubmit={handleSubmit}>
            <Input
              label="Title"
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              required
            />
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea
                className="input-field"
                rows="3"
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Assign To</label>
                <select
                  className="input-field"
                  value={formData.assigned_to}
                  onChange={(e) => setFormData({...formData, assigned_to: e.target.value})}
                >
                  <option value="">Unassigned</option>
                  {employees.map(emp => (
                    <option key={emp.id} value={emp.id}>{emp.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
                <select
                  className="input-field"
                  value={formData.priority}
                  onChange={(e) => setFormData({...formData, priority: e.target.value})}
                >
                  <option>Low</option>
                  <option>Medium</option>
                  <option>High</option>
                </select>
              </div>
            </div>
            <Input
              label="Deadline"
              type="date"
              value={formData.deadline}
              onChange={(e) => setFormData({...formData, deadline: e.target.value})}
              required
            />
            <div className="flex gap-2">
              <Button type="submit" variant="primary" disabled={loading}>
                {loading ? 'Saving...' : 'Save'}
              </Button>
              <Button type="button" variant="secondary" onClick={() => setShowForm(false)}>Cancel</Button>
            </div>
          </form>
        </Card>
      )}

      {/* Tasks List */}
      <Card>
        {loading ? (
          <p>Loading...</p>
        ) : filteredTasks.length === 0 ? (
          <p className="text-gray-500">No tasks</p>
        ) : (
          <div className="space-y-2">
            {filteredTasks.map(task => (
              <div key={task.id} className="flex justify-between items-center p-4 bg-gray-50 rounded-lg border">
                <div className="flex-1">
                  <p className="font-medium text-gray-800">{task.title}</p>
                  <p className="text-sm text-gray-600">{task.description}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {task.employees?.name || 'Unassigned'} • Due: {task.deadline} • Priority: {task.priority}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <select
                    value={task.status}
                    onChange={(e) => updateTaskStatus(task.id, e.target.value)}
                    className="input-field text-sm"
                  >
                    <option>Pending</option>
                    <option>In Progress</option>
                    <option>Done</option>
                  </select>
                  <Button variant="danger" size="sm" onClick={() => deleteTask(task.id)}>Delete</Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}
