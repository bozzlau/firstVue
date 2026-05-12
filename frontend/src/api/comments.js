import client from './client'

// ── 公开接口 ──────────────────────────────────────────────────────────────────

export const getComments = (slug) =>
  client.get(`/api/posts/${slug}/comments`).then((r) => r.data)

export const createComment = (slug, data) =>
  client.post(`/api/posts/${slug}/comments`, data).then((r) => r.data)

// ── 管理接口 ──────────────────────────────────────────────────────────────────

export const adminGetComments = () =>
  client.get('/admin/comments').then((r) => r.data)

export const adminUpdateComment = (id, data) =>
  client.patch(`/admin/comments/${id}`, data).then((r) => r.data)

export const adminDeleteComment = (id) =>
  client.delete(`/admin/comments/${id}`).then((r) => r.data)
