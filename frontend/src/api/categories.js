import client from './client'

export const getCategories = () =>
  client.get('/api/categories').then((r) => r.data)

export const adminGetCategories = () =>
  client.get('/admin/categories').then((r) => r.data)

export const adminCreateCategory = (data) =>
  client.post('/admin/categories', data).then((r) => r.data)

export const adminUpdateCategory = (id, data) =>
  client.put(`/admin/categories/${id}`, data).then((r) => r.data)

export const adminDeleteCategory = (id) =>
  client.delete(`/admin/categories/${id}`).then((r) => r.data)
