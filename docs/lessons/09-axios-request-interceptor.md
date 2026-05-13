# 09 · axios 拦截器（上）—— 请求拦截器

## 💡 什么是拦截器

把 axios 发请求想象成一条流水线：

```
业务代码发起请求
    ↓
[请求拦截器]  ← 可以在这里修改请求
    ↓
真正发送到服务器
    ↓
服务器响应
    ↓
[响应拦截器]  ← 可以在这里处理响应或错误
    ↓
交给业务代码
```

拦截器 = 「在请求离开 / 响应到达之前，插一段自己的逻辑」。写一次，所有用 `client` 发的请求都自动经过。

## 🧩 请求拦截器代码

`src/api/client.js`：

```js
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

## 🧩 逐行拆解

```js
client.interceptors.request.use((config) => {
```
注册请求拦截器。axios 每次发请求时把**请求配置对象** `config` 传进来。

```js
  const token = localStorage.getItem('token')
```
从浏览器本地存储取出之前保存的 token。

```js
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
```
有 token 就塞进请求头。没 token 就不塞（公开接口也走这个拦截器，但不需要 token）。

```js
  return config
})
```
**必须 return config**，否则 axios 不知道怎么发请求。

## 💡 为什么要拦截器

没有拦截器，每个接口都要手动写 token：

```js
client.get('/admin/posts', {
  headers: { Authorization: `Bearer ${token}` }  // 每个接口都抄一遍
})
```

有拦截器之后：

```js
client.get('/admin/posts')   // 自动加上 token，什么都不用写
```

## 💡 localStorage 是什么

浏览器自带的**持久化存储**，关闭浏览器再打开还在：

```js
localStorage.setItem('token', 'abc123')   // 存
localStorage.getItem('token')              // 取 → 'abc123'
localStorage.removeItem('token')           // 删
```

特点：
- 只能存字符串，存对象要先 `JSON.stringify()`
- 大小约 5~10MB
- 同源共享（同域名下所有页面能互相读取）
- 不会随请求自动发给后端（cookie 会）

## 💡 模板字符串（template literal）

```js
`Bearer ${token}`
```

用反引号 `` ` `` 包起来，`${}` 里的变量会被自动替换：

```js
const name = '张三'
const age = 20

// 老写法：字符串拼接
'你好，我是 ' + name + '，今年 ' + age + ' 岁'

// 新写法：模板字符串
`你好，我是 ${name}，今年 ${age} 岁`
```

## 💡 Bearer 是什么

HTTP 标准定义的授权格式之一，全名 Bearer Token（持有者令牌）。谁拿着这个 token 就代表谁。固定格式：

```
Authorization: Bearer <token字符串>
```

后端按这个格式解析，验证 token 是否有效。

## 🎯 小结

| 点 | 记住 |
|----|------|
| 拦截器 | 请求发出前/响应到达后自动执行的中间逻辑 |
| 请求拦截器 | `client.interceptors.request.use(fn)`，必须 return config |
| localStorage | 浏览器持久化存储，只存字符串 |
| 模板字符串 | 反引号 + `${变量}`，替代字符串拼接 |
| Bearer 格式 | `Authorization: Bearer <token>` |

## 🔗 相关

- 上一章：[08 axios 和 HTTP 客户端基础](08-axios-basics.md)
- 下一章：[10 axios 拦截器（下）—— 响应拦截器](10-axios-response-interceptor.md)
