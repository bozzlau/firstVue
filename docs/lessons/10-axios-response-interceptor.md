# 10 · axios 拦截器（下）—— 响应拦截器

## 🧩 响应拦截器的结构

```js
client.interceptors.response.use(
  (response) => response,       // 成功（2xx）时调用
  (error) => {                  // 失败（4xx/5xx/网络错误）时调用
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/admin/login'
    }
    return Promise.reject(error)
  }
)
```

第一个函数成功时原样返回，重点在失败处理函数。

## 💡 `?.` 可选链操作符

请求失败有两种情况：
1. 服务器有响应但状态码是 4xx/5xx → `error.response` 存在
2. 网络断了，没收到响应 → `error.response` 是 `undefined`

```js
// 没有 ?.：网络断了时直接报错
error.response.status    // TypeError: Cannot read property 'status' of undefined

// 有 ?.：左边是 null/undefined 就返回 undefined，不报错
error.response?.status   // undefined，安全跳过
```

常见用法：

```js
user?.name               // user 可能是 null
post?.category?.name     // 链式，任何一环是 null 都安全
arr?.[0]                 // 数组元素
fn?.()                   // 函数可能不存在
```

## 💡 401 是什么

HTTP 状态码 `401 Unauthorized` = 未认证，token 没带或已过期。

后端每个需要登录的接口都验证 token，失败就返回 401。前端拦截到 401 就知道登录状态失效了。

## 🧩 `window.location.href` vs `router.push`

```js
window.location.href = '/admin/login'   // 浏览器原生，整页刷新
router.push('/admin/login')             // Vue Router，SPA 内跳转，不刷新
```

`client.js` 是普通 JS 文件，不在 Vue 组件里，拿不到 `router` 实例，所以用浏览器原生 API。

## 💡 `return Promise.reject(error)` 为什么不能省

```js
(error) => {
  if (error.response?.status === 401) { ... }
  return Promise.reject(error)   // ← 必须有
}
```

如果省掉，失败处理函数返回 `undefined`，axios 把它当成「成功」——错误被**吞掉**，业务代码的 `catch` 收不到任何错误，调试时完全看不出哪里出了问题。

`Promise.reject(error)` = 「我处理完了，但错误还是要继续往外抛」。

## 🧩 完整流程：token 过期后发请求

```
业务代码：adminGetPosts()
    ↓
请求拦截器：从 localStorage 取 token，塞进 header
    ↓
后端验证失败：返回 401
    ↓
响应拦截器（失败函数）：
    1. 检测到 401
    2. localStorage.removeItem('token')  清掉过期 token
    3. window.location.href = '/admin/login'  跳转登录页
    4. return Promise.reject(error)  错误继续往外抛
    ↓
业务代码的 catch（如果有）：收到错误
```

这套机制让所有接口自动处理登录失效，业务代码不用每处都写跳转逻辑。

## 🎯 小结

| 点 | 记住 |
|----|------|
| 响应拦截器 | `.interceptors.response.use(成功fn, 失败fn)` |
| `?.` 可选链 | 左边是 null/undefined 就返回 undefined，不报错 |
| 401 | HTTP 未认证，token 无效或过期 |
| `Promise.reject(error)` | 让错误继续往外传，不能吞掉 |
| `window.location.href` | 浏览器原生跳转，整页刷新 |

## 🔗 相关

- 上一章：[09 axios 拦截器（上）—— 请求拦截器](09-axios-request-interceptor.md)
- 下一章：[11 Vue 模板语法：v-if / v-for / :key](11-vue-template-directives.md)
