# 31 · 懒加载：动态 import

## 💡 为什么要懒加载

普通 import 在文件顶部，应用启动时把所有组件代码一次性打包加载。博客有十几个页面，用户打开首页时却要下载所有页面的代码，浪费流量，首屏变慢。

懒加载的思路：**用到哪个页面，才加载那个页面的代码**。

---

## 🧩 动态 import 语法

```javascript
// 静态 import：启动时立即加载
import HomeView from '../views/public/HomeView.vue'

// 动态 import：调用时才加载，返回 Promise
() => import('../views/public/HomeView.vue')
```

`() => import(...)` 是一个**函数**，返回 Promise。Vue Router 看到 `component` 是函数时，会在路由匹配时才调用它，触发加载。

---

## 🧩 实际效果

```javascript
routes: [
  {
    path: '/',
    component: () => import('../components/public/PublicLayout.vue'),
    children: [
      { path: '', component: () => import('../views/public/HomeView.vue') },
      { path: 'posts/:slug', component: () => import('../views/public/PostView.vue') },
      // ...
    ],
  },
]
```

用户打开首页 `/`：
- 加载 `PublicLayout.vue` + `HomeView.vue` 的代码
- `PostView.vue`、`LoginView.vue`、所有管理后台页面的代码**不加载**

用户点击某篇文章：
- 这时才加载 `PostView.vue` 的代码
- 已加载过的组件直接复用，不重复加载

Vite 构建时会把每个懒加载的组件打成独立的 chunk 文件，浏览器按需下载。

---

## 🧩 对比：不用懒加载

```javascript
// 如果全部静态 import
import HomeView from '../views/public/HomeView.vue'
import PostView from '../views/public/PostView.vue'
import LoginView from '../views/admin/LoginView.vue'
import PostEditView from '../views/admin/PostEditView.vue'
// ... 十几个

// 所有代码打成一个大文件，首屏要下载全部
```

项目规模小时差别不大，页面多了之后懒加载能显著减少首屏加载时间。

---

## 🎯 小结

| 概念 | 记住 |
|------|------|
| 静态 import | 顶部声明，启动时加载 |
| 动态 import `() => import(...)` | 函数形式，调用时才加载，返回 Promise |
| Vue Router 懒加载 | `component` 传函数，路由匹配时才加载组件代码 |

## 🔗 相关文件

- `frontend/src/router/index.js` — 所有路由都用了懒加载
