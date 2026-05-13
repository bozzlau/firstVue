# 13 · Vue Router：路由与导航

## 💡 vue-router 是什么，从哪来

`vue-router` 是一个**第三方 npm 包**，不是浏览器自带的，也不是 Vue 本身自带的。它是 Vue 官方团队单独开发的路由库。

打开 `frontend/package.json`，能看到它被单独列出来：

```json
"dependencies": {
  "vue": "^3.5.13",
  "vue-router": "^4.5.0",
  "pinia": "^2.3.1"
}
```

这三个都是独立的包，各司其职：
- `vue` —— Vue 框架本体
- `vue-router` —— 路由功能
- `pinia` —— 状态管理

用之前要 import：

```js
import { createRouter, createWebHistory } from 'vue-router'  // 创建路由器
import { useRouter, useRoute } from 'vue-router'             // 组件里使用
```

**判断一个东西从哪来的规则：**
- 引号里没有 `/` → npm 包（`'vue'`、`'vue-router'`、`'axios'`）
- 引号里有 `/` → 自己写的文件（`'../stores/auth'`、`'./client'`）

---

## 💡 为什么需要路由

传统网站：每个 URL 对应服务器上一个 HTML 文件，跳页面要重新请求服务器、整页刷新。

Vue 是**单页应用（SPA）**：整个网站只有一个 `index.html`，URL 变化时不刷新页面，由 JavaScript 决定显示哪个组件。这套机制就是**前端路由**，由 `vue-router` 实现。

---

## 🧩 路由怎么装进 Vue 应用

打开 `frontend/src/main.js`：

```js
import router from './router'       // 从 router/index.js 导入路由器

const app = createApp(App)
app.use(router)                     // 把路由器装进 Vue 应用
app.mount('#app')
```

`app.use(router)` 之后，所有组件才能用 `useRouter()` 和 `useRoute()`。

---

## 🧩 路由配置：URL 和组件的对应关系

打开 `frontend/src/router/index.js`：

```js
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('../components/public/PublicLayout.vue'),
      children: [
        { path: '', component: () => import('../views/public/HomeView.vue') },
        { path: 'posts/:slug', component: () => import('../views/public/PostView.vue') },
      ],
    },
  ],
})
```

用大白话解释：
- 访问 `/` → 渲染 `PublicLayout.vue`
- `PublicLayout.vue` 里有 `<RouterView />`，子路由的组件渲染在这里
- 子路径为空（`path: ''`）→ 把 `HomeView.vue` 塞进 `<RouterView />`

所以访问首页时，页面结构是：

```
PublicLayout（外壳：导航栏 + 侧边栏）
    └── HomeView（内容：文章列表，渲染在 <RouterView /> 里）
```

切换到文章详情页时，`PublicLayout` 不重新挂载，只有 `<RouterView />` 里的内容换成 `PostView`。

打开 `frontend/src/components/public/PublicLayout.vue`，找到：

```html
<RouterView />
```

这就是子组件渲染的位置。

---

## 💡 懒加载：`() => import(...)`

```js
component: () => import('../views/public/HomeView.vue')
```

注意这里不是直接 `import HomeView from '...'`，而是一个**返回 import 的函数**。

- 直接 import：打包时所有页面代码打进一个文件，首次加载慢
- 懒加载：每个页面单独打包，**访问到那个路由时才加载对应代码**

用户只访问首页，就不需要下载管理后台的代码。

---

## 🧩 动态路由参数 `:slug` `:id`

```js
{ path: 'posts/:slug', component: () => import('../views/public/PostView.vue') }
```

`:slug` 是占位符，匹配 URL 里对应位置的任意值：

| 访问的 URL | `:slug` 的值 |
|-----------|------------|
| `/posts/vim-why-use-it` | `vim-why-use-it` |
| `/posts/hello-world` | `hello-world` |

**看数据怎么流动：**

第一步，打开 `frontend/src/components/public/PostCard.vue` 第 14 行：

```js
@click="router.push(`/posts/${post.slug}`)"
```

点击文章卡片，把 `post.slug`（比如 `vim-why-use-it`）拼进 URL，跳转到 `/posts/vim-why-use-it`。

第二步，Vue Router 匹配到 `posts/:slug` 这条路由，渲染 `PostView.vue`。

第三步，打开 `frontend/src/views/public/PostView.vue`，找这两行：

```js
const route = useRoute()            // 从 vue-router 包导入，读取当前路由信息
const slug = route.params.slug      // 取出 URL 里 :slug 对应的值
```

然后用这个 `slug` 去请求文章详情：

```js
const data = await getPost(slug)    // 发请求：GET /api/posts/vim-why-use-it
```

---

## 🧩 meta：给路由附加信息

打开 `frontend/src/router/index.js` 第 24 行：

```js
{
  path: '/admin',
  component: () => import('../components/admin/AdminLayout.vue'),
  meta: { requiresAuth: true },    // ← 自定义信息：需要登录
  children: [
    { path: 'dashboard', ... },
    { path: 'posts', ... },
    { path: 'posts/:id', ... },
  ],
}
```

`meta` 是你自己定义的附加数据，可以写任何东西。

子路由会**自动继承**父路由的 meta，所以 `/admin/dashboard`、`/admin/posts` 等所有子路由都自动带上 `requiresAuth: true`，不用每个都写一遍。

---

## 🧩 路由守卫：beforeEach

打开 `frontend/src/router/index.js` 第 40 行：

```js
router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const auth = useAuthStore()
    if (!auth.isLoggedIn) {
      return { path: '/admin/login' }
    }
  }
})
```

`beforeEach` 是 `vue-router` 提供的方法，**每次路由跳转之前**都会执行这个函数。

参数 `to` 是即将进入的路由对象，包含 `path`、`params`、`meta` 等信息。

**场景：没登录时直接访问 `/admin/dashboard`**

1. Vue Router 准备跳转到 `/admin/dashboard`
2. `beforeEach` 触发，`to` 就是 `/admin/dashboard` 这个路由
3. `to.meta.requiresAuth` → `true`（继承自父路由 `/admin`）
4. `auth.isLoggedIn` → `false`（没登录）
5. 返回 `{ path: '/admin/login' }` → 重定向到登录页，原来的跳转被取消

已登录时，`beforeEach` 什么都不返回，正常跳转。

---

## 🧩 useRouter vs useRoute

这两个都从 `vue-router` 包导入，经常搞混：

```js
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()   // 路由器实例，用来跳转
const route = useRoute()     // 当前路由信息，用来读参数
```

| | `useRouter()` | `useRoute()` |
|--|--------------|-------------|
| 来源 | `vue-router` 包 | `vue-router` 包 |
| 返回 | 路由器实例 | 当前路由信息 |
| 用途 | **操作**路由（跳转） | **读取**路由（参数、路径） |
| 常用 | `router.push('/path')` | `route.params.id` |

**项目里的实例：**

`PostCard.vue` 第 2、8、14 行（需要跳转，用 `useRouter`）：
```js
import { useRouter } from 'vue-router'
const router = useRouter()
@click="router.push(`/posts/${post.slug}`)"
```

`PostEditView.vue`（需要读参数，用 `useRoute`）：
```js
const route = useRoute()
const isEdit = computed(() => !!route.params.id)
// /admin/posts/new → route.params.id 是 undefined → isEdit = false（新建）
// /admin/posts/5   → route.params.id 是 '5'       → isEdit = true（编辑）
```

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `vue-router` | npm 包，单独安装 | Vue 官方路由库 |
| `createRouter` | `vue-router` | 创建路由器，只在 `router/index.js` 用一次 |
| `useRouter()` | `vue-router` | 组件里跳转用 |
| `useRoute()` | `vue-router` | 组件里读参数用 |
| 嵌套路由 | 路由配置 | 父组件渲染一次，子路由在 `<RouterView>` 里切换 |
| `:param` | 路由配置 | 动态参数，`route.params.xxx` 取值 |
| `meta` | 路由配置 | 附加信息，子路由自动继承 |
| `beforeEach` | `vue-router` | 跳转前执行，返回路径则重定向 |

## 🔗 相关文件

- `frontend/src/main.js` —— 路由器装进 Vue 应用
- `frontend/src/router/index.js` —— 路由配置、守卫
- `frontend/src/components/public/PublicLayout.vue` —— `<RouterView />` 位置
- `frontend/src/components/public/PostCard.vue` —— `useRouter` 跳转示例
- `frontend/src/views/public/PostView.vue` —— `useRoute` 读参数示例
- `frontend/src/views/admin/PostEditView.vue` —— `route.params.id` 判断新建/编辑
