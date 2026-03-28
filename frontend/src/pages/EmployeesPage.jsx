import React, { useEffect, useState } from 'react'
import { Card } from '../components/Card'
import { Button } from '../components/Button'
import { Input } from '../components/Input'
import { useApp } from '../context/AppContext'
import { Toast } from '../components/Toast'

export function EmployeesPage() {
  const { employees, loading, toast, fetchEmployees, addEmployee, updateEmp, deleteEmp } = useApp()
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [formData, setFormData] = useState({ name: '', email: '', department: '' })

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

  return (
    <div className="space-y-6">
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => {}} />}

      <Button onClick={() => setShowForm(true)} variant="primary">
        ➕ Add Employee
      </Button>

      {/* Form Modal */}
      {showForm && (
        <Card className="bg-white">
          <h3 className="text-xl font-bold mb-4">{editingId ? 'Edit Employee' : 'Add Employee'}</h3>
          <form onSubmit={handleSubmit}>
            <Input
              label="Name"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              required
            />
            <Input
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              required
            />
            <Input
              label="Department"
              value={formData.department}
              onChange={(e) => setFormData({...formData, department: e.target.value})}
              required
            />
            <div className="flex gap-2">
              <Button type="submit" variant="primary" disabled={loading}>
                {loading ? 'Saving...' : 'Save'}
              </Button>
              <Button type="button" variant="secondary" onClick={handleCancel}>
                Cancel
              </Button>
            </div>
          </form>
        </Card>
      )}

      {/* Employees Table */}
      <Card>
        {loading ? (
          <p>Loading...</p>
        ) : employees.length === 0 ? (
          <p className="text-gray-500">No employees yet</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100">
                <tr>
                  <th className="text-left px-4 py-2">Name</th>
                  <th className="text-left px-4 py-2">Email</th>
                  <th className="text-left px-4 py-2">Department</th>
                  <th className="text-left px-4 py-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                {employees.map(emp => (
                  <tr key={emp.id} className="border-t hover:bg-gray-50">
                    <td className="px-4 py-2">{emp.name}</td>
                    <td className="px-4 py-2">{emp.email}</td>
                    <td className="px-4 py-2">{emp.department}</td>
                    <td className="px-4 py-2 space-x-2">
                      <Button variant="secondary" size="sm" onClick={() => handleEdit(emp)}>Edit</Button>
                      <Button variant="danger" size="sm" onClick={() => deleteEmp(emp.id)}>Delete</Button>
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
