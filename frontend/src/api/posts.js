import client from './client'

// ── 公开接口 ──────────────────────────────────────────────────────────────────

export const getPosts = (params) =>
  client.get('/api/posts', { params }).then((r) => r.data)

export const getPost = (slug) =>
  client.get(`/api/posts/${slug}`).then((r) => r.data)

export const searchPosts = (params) =>
  client.get('/api/search', { params }).then((r) => r.data)

// ── 管理接口 ──────────────────────────────────────────────────────────────────

export const adminGetPosts = (params) =>
  client.get('/admin/posts', { params }).then((r) => r.data)

export const adminGetPost = (id) =>
  client.get(`/admin/posts/${id}`).then((r) => r.data)

export const adminCreatePost = (data) =>
  client.post('/admin/posts', data).then((r) => r.data)

export const adminUpdatePost = (id, data) =>
  client.put(`/admin/posts/${id}`, data).then((r) => r.data)

export const adminDeletePost = (id) =>
  client.delete(`/admin/posts/${id}`).then((r) => r.data)

export const adminRestorePost = (id) =>
  client.post(`/admin/posts/${id}/restore`).then((r) => r.data)

export const adminGetPostLogs = (id) =>
  client.get(`/admin/posts/${id}/logs`).then((r) => r.data)
