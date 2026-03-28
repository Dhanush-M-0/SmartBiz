import apiClient from './client'

export const getTasks = async (status = null) => {
  const params = status ? { status } : {}
  const response = await apiClient.get('/tasks', { params })
  return response.data.data
}

export const getTask = async (id) => {
  const response = await apiClient.get(`/tasks/${id}`)
  return response.data.data
}

export const createTask = async (title, description, assigned_to, priority, deadline) => {
  const response = await apiClient.post('/tasks', {
    title,
    description,
    assigned_to,
    priority,
    deadline,
  })
  return response.data.data
}

export const updateTask = async (id, updates) => {
  const response = await apiClient.put(`/tasks/${id}`, updates)
  return response.data.data
}

export const deleteTask = async (id) => {
  await apiClient.delete(`/tasks/${id}`)
}
