# 27 · 管理后台链路串讲：登录与发文

入口：**管理员打开登录页，输入密码，进入后台发布文章。**

---

## 第一步：访问 `/admin/login`，路由守卫检查

Vue Router 的 `beforeEach` 守卫（第 13 课）在每次跳转前执行：

```javascript
// frontend/src/router/index.js
router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return '/admin/login'
  }
})
```

`/admin/login` 没有 `requiresAuth`，直接放行，渲染 `LoginView.vue`。

---

## 第二步：Pinia store 初始化，读取 localStorage

`frontend/src/stores/auth.js`（第 14 课）：

```javascript
const token = ref(localStorage.getItem('token') || null)
const isLoggedIn = computed(() => !!token.value)
```

页面刷新时，Pinia store 重新初始化，从 `localStorage` 读取上次保存的 token。如果 token 还在，`isLoggedIn` 就是 `true`，路由守卫直接放行到后台，不需要重新登录。

`!!token.value` — 两个感叹号把任意值转成布尔值：`null` → `false`，有值 → `true`。

---

## 第三步：用户提交表单，触发登录

`LoginView.vue`：

```javascript
async function handleLogin() {
  try {
    await auth.login(form.value.username, form.value.password)
    router.push('/admin/dashboard')   // 登录成功，跳转后台
  } catch {
    error.value = '用户名或密码错误'
  }
}
```

`v-model="form.username"` 把输入框和 `form.username` 双向绑定（第 15 课），用户输入时自动同步。

---

## 第四步：Pinia store 发请求，保存 token

`auth.js` 里的 `login` 函数：

```javascript
async function login(username, password) {
  const data = await authApi.login(username, password)
  token.value = data.access_token          // 更新响应式状态
  localStorage.setItem('token', data.access_token)  // 持久化到本地
}
```

`authApi.login` 发出 `POST /admin/login`，后端验证密码（第 22 课），返回 JWT。

两个地方都要存：
- `token.value` — 当前页面用，响应式，`isLoggedIn` 立即变成 `true`
- `localStorage` — 持久化，刷新页面后还在

---

## 第五步：后续请求自动带 token

登录成功后，管理员进入后台，每次操作都会发请求。

`frontend/src/api/client.js` 的请求拦截器（第 9 课）：

```javascript
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

每次请求发出前，拦截器从 `localStorage` 读 token，加到请求头。后端 `get_current_admin` 验证这个 token（第 22 课），验证通过才执行接口逻辑。

---

## 第六步：token 过期，自动跳回登录页

响应拦截器（第 10 课）：

```javascript
(error) => {
  if (error.response?.status === 401) {
    localStorage.removeItem('token')
    window.location.href = '/admin/login'
  }
  return Promise.reject(error)
}
```

token 过期后，后端返回 401，拦截器自动清除 token 并跳转登录页。管理员不需要手动处理，整个过程对业务代码透明。

---

## 第七步：退出登录

`AdminLayout.vue` 底部的退出按钮：

```javascript
function logout() {
  auth.logout()
  router.push('/admin/login')
}
```

`auth.logout()`（Pinia store）：

```javascript
function logout() {
  token.value = null
  localStorage.removeItem('token')
}
```

`token.value = null` → `isLoggedIn` 变成 `false` → 路由守卫拦截所有 `/admin/*` 请求。

---

## 完整链路图

```
访问 /admin/login
    ↓
路由守卫检查 isLoggedIn                           [第 13 课]
    ↓
Pinia store 从 localStorage 读 token             [第 14 课]
    ↓
用户填写表单，v-model 双向绑定                    [第 15 课]
    ↓
提交 → auth.login() → POST /admin/login          [第 14 课]
    ↓
后端验证密码（bcrypt），生成 JWT 返回             [第 22 课]
    ↓
token 存入 ref + localStorage                    [第 14 课]
    ↓
router.push('/admin/dashboard')                  [第 13 课]
    ↓
后续每次请求，拦截器自动加 Authorization 头       [第 9 课]
    ↓
后端 get_current_admin 验证 token                [第 22 课]
    ↓
验证通过 → 执行业务逻辑
验证失败(401) → 拦截器清除 token，跳回登录页     [第 10 课]
```

## 🔗 涉及文件

- `frontend/src/stores/auth.js` — token 状态管理
- `frontend/src/views/admin/LoginView.vue` — 登录页
- `frontend/src/api/client.js` — axios 拦截器
- `frontend/src/router/index.js` — 路由守卫
- `backend/app/routers/admin/auth.py` — 登录接口
- `backend/app/dependencies.py` — get_current_admin
