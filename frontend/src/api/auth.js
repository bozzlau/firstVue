import client from './client'

export async function login(username, password) {
  // 后端用 OAuth2PasswordRequestForm，必须发 form-urlencoded 格式，不能发 JSON
  const form = new URLSearchParams()
  form.append('username', username)
  form.append('password', password)
  const { data } = await client.post('/admin/login', form)
  return data
}
