# 07 · .then() vs await：回调地狱的演化史

## 💡 核心结论

`.then()` 和 `await` 做的事情**完全一样**，选哪个取决于代码结构。

| 场景 | 推荐 |
|------|------|
| 一步转换（取字段、改格式） | `.then()` |
| 多步骤 / 有条件 / 需要错误处理 | `await` |

项目的实际分工：
- **`api/` 层**（纯数据转换）→ `.then()`
- **组件业务逻辑**（多步操作）→ `await`

## 💡 为什么有两种写法：异步的三个时代

### 时代 1：回调地狱（2015 前）

那时候没有 Promise，异步全靠**传回调函数**。假设要连续做 4 个依赖的请求：

```js
getCurrentUser((err, user) => {
  if (err) return handleError(err)
  getPosts(user.id, (err, posts) => {
    if (err) return handleError(err)
    getComments(posts[0].id, (err, comments) => {
      if (err) return handleError(err)
      getReplies(comments[0].id, (err, replies) => {
        if (err) return handleError(err)
        console.log(replies)
      })
    })
  })
})
```

**问题：**
- 缩进越来越深，像金字塔——名字叫 **"callback hell"**（回调地狱）
- 每一层都要单独 `if (err) return` 处理错误
- 想加条件判断？得大动嵌套结构

### 时代 2：Promise 链（ES6，2015）

Promise 把嵌套**拍平**成链式调用：

```js
getCurrentUser()
  .then((user) => getPosts(user.id))
  .then((posts) => getComments(posts[0].id))
  .then((comments) => getReplies(comments[0].id))
  .then((replies) => console.log(replies))
  .catch((err) => handleError(err))
```

**改进：**
- 不再嵌套
- 一个 `.catch()` 统一捕获所有错误

**仍然的问题：** 如果后面要用前面的结果，需要外部变量：

```js
let user, posts
getCurrentUser()
  .then((u) => { user = u; return getPosts(u.id) })
  .then((p) => { posts = p; return getComments(p[0].id) })
  .then((c) => getReplies(c[0].id))
  .then((replies) => ({ user, posts, replies }))
```

### 时代 3：async / await（ES2017）

```js
async function load() {
  try {
    const user = await getCurrentUser()
    const posts = await getPosts(user.id)
    const comments = await getComments(posts[0].id)
    const replies = await getReplies(comments[0].id)
    console.log({ user, posts, comments, replies })
  } catch (err) {
    handleError(err)
  }
}
```

看起来像同步代码，从上到下读，中间变量随便用。

## 🧩 真正体现 await 优势的场景：有条件分支

需求：如果用户没文章就跳过评论步骤。

**`.then()` 版本：**

```js
getCurrentUser()
  .then((user) => getPosts(user.id))
  .then((posts) => {
    if (posts.length === 0) return null   // 靠特殊值传递"跳过"
    return getComments(posts[0].id)
  })
  .then((comments) => {
    if (comments === null) return null    // 下一层还要判断
    return getReplies(comments[0].id)
  })
  .then((replies) => {
    if (replies === null) {
      console.log('没有内容')
    } else {
      console.log(replies)
    }
  })
```

**`await` 版本：**

```js
async function load() {
  const user = await getCurrentUser()
  const posts = await getPosts(user.id)
  if (posts.length === 0) {
    console.log('没有内容')
    return
  }
  const comments = await getComments(posts[0].id)
  const replies = await getReplies(comments[0].id)
  console.log(replies)
}
```

`await` 版本可以直接用 `if / return`，像普通代码；`.then()` 版本必须通过「返回 null → 下一层判断」传递控制流，非常绕。

## 🧩 项目里的具体体现

### `api/posts.js` 用 `.then()` —— 只做一件事

```js
export const getPosts = (params) =>
  client.get('/api/posts', { params }).then((r) => r.data)
```

只是「取响应对象 `r` 的 `data` 字段」这一步转换。用 `.then()` 两行搞定。

改成 `await` 版本：

```js
export const getPosts = async (params) => {
  const r = await client.get('/api/posts', { params })
  return r.data
}
```

功能相同，但多了 `async`、`{}`、`return`，四行。这里没必要。

### `HomeView.vue` 的 `load()` 用 `await` —— 有多步骤

```js
async function load() {
  loading.value = true
  try {
    const data = await getPosts({ page: page.value, page_size: 10 })
    posts.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}
```

5 个步骤 + try/finally + 多个赋值。用 `.then()` 嵌套会很难读。

## 🎯 小结

| 时代 | 写法 | 状态 |
|------|------|------|
| 2015 前 | 嵌套回调 | 已淘汰 |
| 2015+ | Promise `.then()` | 简单场景仍适用 |
| 2017+ | `async/await` | 复杂逻辑的主流 |

**经验法则：**
- 一行就写完 → `.then()`
- 多行、有条件、需要 try/finally → `async/await`

## 🔗 相关

- 上一章：[06 Promise 是什么](06-promise.md)
- 下一章：待写（axios 与 HTTP 请求基础）
