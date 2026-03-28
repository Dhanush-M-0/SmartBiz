import React, { createContext, useState } from 'react'
import * as employeeApi from '../api/employees'
import * as taskApi from '../api/tasks'

export const AppContext = createContext()

export function AppProvider({ children }) {
  const [employees, setEmployees] = useState([])
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [toast, setToast] = useState(null)

  // Employees
  const fetchEmployees = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await employeeApi.getEmployees()
      setEmployees(data)
    } catch (err) {
      setError(err.message)
      showToast(err.message, 'error')
    } finally {
      setLoading(false)
    }
  }

  const addEmployee = async (name, email, department) => {
    try {
      setLoading(true)
      const newEmployee = await employeeApi.createEmployee(name, email, department)
      setEmployees([...employees, newEmployee])
      showToast('Employee added successfully', 'success')
      return true
    } catch (err) {
      setError(err.message)
      showToast(err.message, 'error')
      return false
    } finally {
      setLoading(false)
    }
  }

  const updateEmp = async (id, name, email, department) => {
    try {
      setLoading(true)
      const updated = await employeeApi.updateEmployee(id, name, email, department)
      setEmployees(employees.map(e => e.id === id ? updated : e))
      showToast('Employee updated successfully', 'success')
      return true
    } catch (err) {
      setError(err.message)
      showToast(err.message, 'error')
      return false
    } finally {
      setLoading(false)
    }
  }

  const deleteEmp = async (id) => {
    try {
      setLoading(true)
      await employeeApi.deleteEmployee(id)
      setEmployees(employees.filter(e => e.id !== id))
      showToast('Employee deleted successfully', 'success')
      return true
    } catch (err) {
      setError(err.message)
      showToast(err.message, 'error')
      return false
    } finally {
      setLoading(false)
    }
  }

  // Tasks
  const fetchTasks = async (status = null) => {
    try {
      setLoading(true)
      setError(null)
      const data = await taskApi.getTasks(status)
      setTasks(data)
    } catch (err) {
      setError(err.message)
      showToast(err.message, 'error')
    } finally {
      setLoading(false)
    }
  }

  const addTask = async (title, description, assigned_to, priority, deadline) => {
    try {
      setLoading(true)
      const newTask = await taskApi.createTask(title, description, assigned_to, priority, deadline)
      setTasks([...tasks, newTask])
      showToast('Task created successfully', 'success')
      return true
    } catch (err) {
      setError(err.message)
      showToast(err.message, 'error')
      return false
    } finally {
      setLoading(false)
    }
  }

  const updateTaskStatus = async (id, status) => {
    try {
      setLoading(true)
      const updated = await taskApi.updateTask(id, { status })
      setTasks(tasks.map(t => t.id === id ? updated : t))
      showToast('Task updated successfully', 'success')
      return true
    } catch (err) {
      setError(err.message)
      showToast(err.message, 'error')
      return false
    } finally {
      setLoading(false)
    }
  }

  const deleteTask = async (id) => {
    try {
      setLoading(true)
      await taskApi.deleteTask(id)
      setTasks(tasks.filter(t => t.id !== id))
      showToast('Task deleted successfully', 'success')
      return true
    } catch (err) {
      setError(err.message)
      showToast(err.message, 'error')
      return false
    } finally {
      setLoading(false)
    }
  }

  const showToast = (message, type) => {
    setToast({ message, type })
    setTimeout(() => setToast(null), 3000)
  }

  return (
    <AppContext.Provider value={{
      employees,
      tasks,
      loading,
      error,
      toast,
      fetchEmployees,
      addEmployee,
      updateEmp,
      deleteEmp,
      fetchTasks,
      addTask,
      updateTaskStatus,
      deleteTask,
    }}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const context = React.useContext(AppContext)
  if (!context) {
    throw new Error('useApp must be used within AppProvider')
  }
  return context
}
