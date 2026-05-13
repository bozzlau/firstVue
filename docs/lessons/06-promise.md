# 06 · Promise 是什么

## 💡 生活中的 Promise

想象你去咖啡店点咖啡：

1. 付钱下单 → 店员给你一张**小票**
2. 你拿着小票先去旁边等 → 这时咖啡还没做好
3. 咖啡做好了，店员叫号 → 你凭小票**取咖啡**

**Promise 就是这张小票。** 它代表一个「将来会有结果的异步操作」。

## 🧩 Promise 的三种状态

```
           ┌─── fulfilled (成功，有值)
pending ───┤
           └─── rejected  (失败，有错误)
```

| 状态 | 英文 | 含义 |
|------|------|------|
| 进行中 | pending | 咖啡还在做 |
| 成功 | fulfilled / resolved | 咖啡做好了，拿到值 |
| 失败 | rejected | 咖啡机坏了，抛出错误 |

状态一旦从 `pending` 变到其他两个之一，就**不可逆**。

## 🧩 验证一下

```js
const p = getPosts(...)   // 立刻返回，不会等
console.log(p)            // Promise { <pending> }
```

`p` 不是真正的数据，而是「将来能拿到数据的凭证」。

## 🧩 拿到值的两种方式

### 方式 1：`.then()`（老写法）

```js
getPosts(...).then((data) => {
  console.log(data)   // 咖啡好了，回调被调用
})
```

`.then()` 接收一个**回调函数**，Promise 成功时自动调用它，参数就是结果。

### 方式 2：`await`（新写法）

```js
const data = await getPosts(...)
console.log(data)     // 等拿到咖啡再往下走
```

两种写法**功能完全相同**，只是 `await` 读起来像同步代码更顺畅。

### 错误处理

```js
// .then 版本
getPosts(...)
  .then((data) => console.log(data))
  .catch((err) => console.error(err))

// await 版本
try {
  const data = await getPosts(...)
} catch (err) {
  console.error(err)
}
```

## 💡 async 函数和 Promise 的关系

```js
async function foo() {
  return 42
}

foo()              // Promise { 42 }，不是 42！
await foo()        // 42
```

只要函数带 `async`，返回值会**自动**被包装成 Promise。这就是为什么 `await foo()` 能拿到值。

## 🧩 手动创建 Promise（了解即可）

现实中很少自己写，但理解原理有帮助：

```js
const p = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve('ok')      // 1 秒后标记成功，值为 'ok'
    // reject(new Error('fail'))  // 或者失败
  }, 1000)
})

p.then((val) => console.log(val))  // 1 秒后打印 'ok'
```

日常业务里 `axios`、`fetch` 已经返回 Promise 了，你直接 `await` 用就行。

## 🧩 项目里的 Promise 链

看 `api/posts.js`：

```js
export const getPosts = (params) =>
  client.get('/api/posts', { params }).then((r) => r.data)
```

三步骤：
1. `client.get(...)` → 返回 Promise A（axios 的响应对象）
2. `.then((r) => r.data)` → 从响应里取 `data` 字段，返回**新的** Promise B
3. 外面 `await getPosts(...)` 拿到的就是 Promise B 里的 `r.data`

## 🎯 小结

| 点 | 记住 |
|----|------|
| 定义 | Promise 是「未来有结果的凭证」 |
| 三种状态 | pending / fulfilled / rejected |
| 拿值 | `.then(回调)` 或 `await` |
| async 函数 | 自动返回 Promise |
| 错误 | `.catch()` 或 `try/catch` |

## 🔗 相关

- 下一章：[07 .then() vs await：回调地狱的演化史](07-then-vs-await.md)
