import client from './client'

export const getTags = () =>
  client.get('/api/tags').then((r) => r.data)

export const adminGetTags = () =>
  client.get('/admin/tags').then((r) => r.data)

export const adminCreateTag = (data) =>
  client.post('/admin/tags', data).then((r) => r.data)

export const adminUpdateTag = (id, data) =>
  client.put(`/admin/tags/${id}`, data).then((r) => r.data)

export const adminDeleteTag = (id) =>
  client.delete(`/admin/tags/${id}`).then((r) => r.data)
