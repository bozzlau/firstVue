# 08 · axios 和 HTTP 客户端基础

## 💡 什么是 axios

axios 是**第三方 HTTP 请求库**。浏览器原生有 `fetch`，但 axios 用起来更省心。

| 对比 | `fetch`（原生） | `axios`（第三方） |
|------|---------------|------------------|
| JSON 解析 | 要手动 `await r.json()` | 自动 |
| 非 2xx 状态码 | 不报错 | 自动进入 catch |
| 拦截器 | 无 | 有 |
| 超时 | 麻烦 | 一个配置 |
| 取消请求 | 一般 | 好 |

项目统一用 axios。

## 🧩 创建实例

看 `src/api/client.js`：

```js
import axios from 'axios'

const client = axios.create({
  baseURL: 'http://localhost:8001',
})
```

没有直接用 `axios.get()`，而是先 `axios.create({...})` 造了一个**实例** `client`。

## 💡 为什么要造实例

不用实例的写法：

```js
axios.get('http://localhost:8001/api/posts')
axios.get('http://localhost:8001/api/posts/hello')
axios.post('http://localhost:8001/admin/login', ...)
```

后端换地址就要改几十处。

用实例 + baseURL：

```js
client.get('/api/posts')           // 自动拼成完整 URL
client.get('/api/posts/hello')
client.post('/admin/login', ...)
```

所有请求共享一份配置——域名、超时、默认 headers 都写一次。这是 `client.js` 存在的价值。

## 🧩 响应对象结构

```js
client.get('/api/posts').then((r) => r.data)
```

`r` 是 axios 包装的响应对象：

```js
{
  data: { ... },          // ← 后端返回的真正内容
  status: 200,            // HTTP 状态码
  statusText: 'OK',
  headers: { ... },       // 响应头
  config: { ... },        // 本次请求的配置
  request: XMLHttpRequest // 底层请求对象
}
```

业务代码只关心 `data`，所以 `api/` 层统一 `.then((r) => r.data)` 脱壳，返回纯数据。

## 🧩 `{ params }`：query string

```js
client.get('/api/posts', { params: { page: 1, page_size: 10 } })
```

会自动拼成：

```
http://localhost:8001/api/posts?page=1&page_size=10
```

这是 HTTP 的 **query parameter**（查询参数），常用于分页、筛选、搜索。

手工拼的坑：

```js
// 如果 q 里有空格、中文、&，需要自己 encodeURIComponent
client.get(`/api/posts?q=${encodeURIComponent(q)}`)
```

axios 的 `params` 帮你做好编码。

## 🧩 常用方法对照

| axios | HTTP 方法 | 用途 |
|-------|----------|------|
| `client.get(url, { params })` | GET | 查询 |
| `client.post(url, body)` | POST | 新建 |
| `client.put(url, body)` | PUT | 更新（完整替换） |
| `client.patch(url, body)` | PATCH | 更新（部分字段） |
| `client.delete(url)` | DELETE | 删除 |

## 🎯 小结

| 点 | 记住 |
|----|------|
| 作用 | 发 HTTP 请求的第三方库 |
| 创建实例 | `axios.create({ baseURL })` 共享配置 |
| 响应结构 | `{ data, status, headers, ... }`，业务只要 `.data` |
| query 参数 | 用 `{ params: {...} }`，自动编码 |

## 🔗 相关

- 下一章：[09 axios 拦截器](09-axios-interceptors.md)
