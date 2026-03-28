import apiClient from './client'

export const getEmployees = async () => {
  const response = await apiClient.get('/employees')
  return response.data.data
}

export const getEmployee = async (id) => {
  const response = await apiClient.get(`/employees/${id}`)
  return response.data.data
}

export const createEmployee = async (name, email, department) => {
  const response = await apiClient.post('/employees', {
    name,
    email,
    department,
  })
  return response.data.data
}

export const updateEmployee = async (id, name, email, department) => {
  const response = await apiClient.put(`/employees/${id}`, {
    name,
    email,
    department,
  })
  return response.data.data
}

export const deleteEmployee = async (id) => {
  await apiClient.delete(`/employees/${id}`)
}
