# 14 · Pinia 状态管理

## 💡 Pinia 是什么，从哪来

`pinia` 是一个**第三方 npm 包**，Vue 官方团队开发的状态管理库。打开 `frontend/package.json`：

```json
"dependencies": {
  "vue": "^3.5.13",
  "vue-router": "^4.5.0",
  "pinia": "^2.3.1"
}
```

用之前要 import：

```js
import { defineStore } from 'pinia'
```

装进 Vue 应用，打开 `frontend/src/main.js`：

```js
import { createPinia } from 'pinia'

const app = createApp(App)
app.use(createPinia())   // 把 Pinia 装进应用
app.use(router)
app.mount('#app')
```

---

## 💡 为什么需要状态管理

token 需要在很多地方用到：
- `client.js` 的请求拦截器要读它（加进请求头）
- `router/index.js` 的路由守卫要读它（判断是否登录）
- `AdminLayout.vue` 的退出登录按钮要清掉它

如果每个地方都自己去 `localStorage.getItem('token')`，代码重复，而且 token 变了不知道哪些地方需要更新。

**Pinia 的作用：把共享数据放在一个集中的地方，所有组件都从这里读写。**

```
LoginView ──写入──→ useAuthStore ←──读取── 路由守卫
                        ↑
AdminLayout ──读取──────┘
```

---

## 🧩 定义 Store

打开 `frontend/src/stores/auth.js`：

```js
import { defineStore } from 'pinia'   // 从 pinia 包导入
import { ref, computed } from 'vue'   // 从 vue 包导入
import * as authApi from '../api/auth' // 从自己写的文件导入

export const useAuthStore = defineStore('auth', () => {
  // 状态（数据）
  const token = ref(localStorage.getItem('token') || null)

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)

  // 方法
  async function login(username, password) {
    const data = await authApi.login(username, password)
    token.value = data.access_token
    localStorage.setItem('token', data.access_token)
  }

  function logout() {
    token.value = null
    localStorage.removeItem('token')
  }

  return { token, isLoggedIn, login, logout }  // 必须 return 才能被外部使用
})
```

`defineStore` 接收两个参数：
- `'auth'`：这个 store 的唯一名字，调试工具里显示用
- 第二个参数：一个函数，里面定义数据和方法，写法和 `<script setup>` 几乎一样

---

## 🧩 逐行拆解

**初始化 token：**

```js
const token = ref(localStorage.getItem('token') || null)
```

- `localStorage.getItem('token')`：从浏览器本地存储读 token
- `|| null`：如果没有就用 null
- `ref(...)`：包装成响应式

这行的意思：**页面刷新时，从 localStorage 恢复之前的登录状态**。

**login 方法：**

```js
async function login(username, password) {
  const data = await authApi.login(username, password)  // 发请求
  token.value = data.access_token                        // 更新响应式数据
  localStorage.setItem('token', data.access_token)       // 持久化
}
```

登录成功后做两件事：
1. `token.value = ...` → 更新响应式数据，所有用到 `isLoggedIn` 的地方立刻更新
2. `localStorage.setItem(...)` → 持久化，刷新页面后还能恢复

**logout 方法：**

```js
function logout() {
  token.value = null
  localStorage.removeItem('token')
}
```

清掉内存里的 token，也清掉 localStorage 里的。

**return：**

```js
return { token, isLoggedIn, login, logout }
```

Store 里的东西默认外面看不到，**必须 return 才能被组件使用**。

---

## 🧩 组件里怎么用

打开 `frontend/src/components/admin/AdminLayout.vue` 第 3-7 行：

```js
import { useAuthStore } from '../../stores/auth'  // 从自己写的文件导入

const auth = useAuthStore()   // 调用，拿到 store 实例

function logout() {
  auth.logout()               // 调用 store 里的方法
  router.push('/admin/login')
}
```

打开 `frontend/src/router/index.js` 第 40-47 行：

```js
router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const auth = useAuthStore()
    if (!auth.isLoggedIn) {      // 读取 store 里的计算属性
      return { path: '/admin/login' }
    }
  }
})
```

**同一个 `useAuthStore()`，在任何地方调用，拿到的都是同一份数据。** 这就是状态管理的核心价值。

---

## 💡 `import * as authApi` 是什么语法

```js
import * as authApi from '../api/auth'
```

`* as authApi` 意思是：把 `api/auth.js` 里所有导出的东西，全部打包成一个对象叫 `authApi`。

```js
authApi.login(username, password)   // 等价于单独 import { login } 再调用
```

这里用 `* as` 是为了可读性——看到 `authApi.login` 就知道这是 API 调用。

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `pinia` | npm 包，单独安装 | Vue 官方状态管理库 |
| `defineStore` | `pinia` 包 | 定义一个 store |
| `useAuthStore` | 自己写的 `stores/auth.js` | 在组件里调用，拿到 store 实例 |
| `return { ... }` | store 内部 | 必须 return 才能被外部使用 |
| 核心价值 | — | 共享数据集中管理，任何地方调用拿到同一份数据 |

## 🔗 相关文件

- `frontend/src/main.js` —— Pinia 装进 Vue 应用
- `frontend/src/stores/auth.js` —— store 定义
- `frontend/src/components/admin/AdminLayout.vue` —— 使用 store 示例
- `frontend/src/router/index.js` —— 路由守卫里使用 store
