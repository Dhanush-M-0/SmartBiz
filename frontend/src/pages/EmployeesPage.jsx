import React, { useEffect, useState } from 'react'
import { Card } from '../components/Card'
import { Button } from '../components/Button'
import { Input, Select } from '../components/Input'
import { useApp } from '../context/AppContext'

const DEPARTMENTS = ['Engineering', 'Design', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations', 'IT', 'Management']

export function EmployeesPage() {
  const { employees, loading, fetchEmployees, addEmployee, updateEmp, deleteEmp } = useApp()
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [formData, setFormData] = useState({ name: '', email: '', department: '' })
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchEmployees()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (editingId) {
      await updateEmp(editingId, formData.name, formData.email, formData.department)
    } else {
      await addEmployee(formData.name, formData.email, formData.department)
    }
    setFormData({ name: '', email: '', department: '' })
    setShowForm(false)
    setEditingId(null)
  }

  const handleEdit = (emp) => {
    setFormData({ name: emp.name, email: emp.email, department: emp.department })
    setEditingId(emp.id)
    setShowForm(true)
  }

  const handleCancel = () => {
    setFormData({ name: '', email: '', department: '' })
    setShowForm(false)
    setEditingId(null)
  }

  const filteredEmployees = employees.filter(emp => 
    emp.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    emp.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    emp.department?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const getDepartmentColor = (dept) => {
    const colors = {
      'Engineering': 'bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300',
      'Design': 'bg-purple-100 dark:bg-purple-900/50 text-purple-700 dark:text-purple-300',
      'Marketing': 'bg-pink-100 dark:bg-pink-900/50 text-pink-700 dark:text-pink-300',
      'Sales': 'bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300',
      'HR': 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-700 dark:text-yellow-300',
      'Finance': 'bg-emerald-100 dark:bg-emerald-900/50 text-emerald-700 dark:text-emerald-300',
      'IT': 'bg-cyan-100 dark:bg-cyan-900/50 text-cyan-700 dark:text-cyan-300',
      'Management': 'bg-indigo-100 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-300',
    }
    return colors[dept] || 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
  }

  return (
    <div className="space-y-6">
      {/* Header Actions */}
      <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
        <Button onClick={() => setShowForm(true)} variant="primary">
          <span>➕</span> Add Employee
        </Button>
        
        <div className="w-full sm:w-72">
          <input
            type="text"
            placeholder="Search employees..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>
      </div>

      {/* Form Modal */}
      {showForm && (
        <Card>
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-6">
            {editingId ? '✏️ Edit Employee' : '➕ Add New Employee'}
          </h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input
                label="Full Name"
                placeholder="John Doe"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required
              />
              <Input
                label="Email Address"
                type="email"
                placeholder="john@company.com"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
              />
              <Select
                label="Department"
                value={formData.department}
                onChange={(e) => setFormData({...formData, department: e.target.value})}
                required
              >
                <option value="">Select department...</option>
                {DEPARTMENTS.map(dept => (
                  <option key={dept} value={dept}>{dept}</option>
                ))}
              </Select>
            </div>
            <div className="flex gap-3 pt-2">
              <Button type="submit" variant="primary" disabled={loading}>
                {loading ? 'Saving...' : editingId ? 'Update Employee' : 'Add Employee'}
              </Button>
              <Button type="button" variant="ghost" onClick={handleCancel}>
                Cancel
              </Button>
            </div>
          </form>
        </Card>
      )}

      {/* Employees Table */}
      <Card>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white">
            All Employees ({filteredEmployees.length})
          </h3>
        </div>
        
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          </div>
        ) : filteredEmployees.length === 0 ? (
          <div className="text-center py-8">
            <span className="text-4xl mb-2 block">👥</span>
            <p className="text-gray-500 dark:text-gray-400">
              {searchTerm ? 'No employees match your search' : 'No employees yet. Add your first employee!'}
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <th className="text-left px-4 py-3 text-sm font-semibold text-gray-600 dark:text-gray-300">Name</th>
                  <th className="text-left px-4 py-3 text-sm font-semibold text-gray-600 dark:text-gray-300">Email</th>
                  <th className="text-left px-4 py-3 text-sm font-semibold text-gray-600 dark:text-gray-300">Department</th>
                  <th className="text-left px-4 py-3 text-sm font-semibold text-gray-600 dark:text-gray-300">Joined</th>
                  <th className="text-right px-4 py-3 text-sm font-semibold text-gray-600 dark:text-gray-300">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                {filteredEmployees.map(emp => (
                  <tr key={emp.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center">
                          <span className="text-primary-600 dark:text-primary-400 font-semibold">
                            {emp.name?.charAt(0)?.toUpperCase()}
                          </span>
                        </div>
                        <span className="font-medium text-gray-800 dark:text-white">{emp.name}</span>
                      </div>
                    </td>
                    <td className="px-4 py-4 text-gray-600 dark:text-gray-300">{emp.email}</td>
                    <td className="px-4 py-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getDepartmentColor(emp.department)}`}>
                        {emp.department}
                      </span>
                    </td>
                    <td className="px-4 py-4 text-gray-500 dark:text-gray-400 text-sm">
                      {emp.created_at ? new Date(emp.created_at).toLocaleDateString() : '-'}
                    </td>
                    <td className="px-4 py-4">
                      <div className="flex justify-end gap-2">
                        <Button variant="ghost" size="sm" onClick={() => handleEdit(emp)}>
                          ✏️ Edit
                        </Button>
                        <Button variant="danger" size="sm" onClick={() => deleteEmp(emp.id)}>
                          🗑️ Delete
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  )
}
