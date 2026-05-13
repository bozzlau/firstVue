# 05 · 异步基础：async / await / try / finally

## 💡 为什么要异步

网络请求需要时间（几十毫秒到几秒）。如果 JavaScript 傻等着，整个页面就卡住了——按钮点不动、动画停住。所以浏览器环境里所有耗时操作都是**异步**的：发出请求后立刻返回，结果到达时再通知你。

## 🧩 async 函数

在函数前加 `async` 关键字，这个函数就变成「异步函数」：

```js
async function load() {
  // ...
}
```

**两个特性：**
1. 永远返回一个 Promise（哪怕你写 `return 1`，外面拿到的也是 `Promise<1>`）
2. 内部可以用 `await`

## 🧩 await 关键字

`await` 的作用是「等 Promise 完成，取出结果」：

```js
const data = await getPosts(...)   // 等请求完成，data 是真正的数据
posts.value = data.items            // 然后往下走
```

**没有 await 会怎样：**

```js
const data = getPosts(...)          // data 是 Promise 对象，不是数据
console.log(data)                   // Promise { <pending> }
posts.value = data.items            // ❌ undefined，Promise 没有 items
```

## ⚠️ await 只能在 async 函数里用

```js
// ❌ 报错
function load() {
  const data = await getPosts(...)
}

// ✅
async function load() {
  const data = await getPosts(...)
}
```

## 🧩 try / catch / finally

异步操作可能失败（网络中断、服务器 500）。用 `try / catch` 捕获错误：

```js
try {
  const data = await getPosts(...)
} catch (err) {
  console.error('请求失败', err)
}
```

**`finally` 无论成功失败都执行**，用来做清理：

```js
loading.value = true
try {
  const data = await getPosts(...)
  posts.value = data.items
} finally {
  loading.value = false   // ← 无论成功/失败，都会回到 false
}
```

这里为什么不用 `catch`？**让错误自然抛出**，由更上层（或全局错误处理器）管。如果 `catch` 吞掉错误，调试时会很痛苦（请求失败了但你看不到）。

## 🧩 项目里的完整例子

`HomeView.vue`：

```js
async function load() {
  loading.value = true              // ① 开启加载状态
  try {
    const data = await getPosts({   // ② 发请求，等结果
      page: page.value,
      page_size: 10,
    })
    posts.value = data.items        // ③ 赋值触发 Vue 重新渲染
    total.value = data.total
  } finally {
    loading.value = false           // ④ 无论如何关掉加载状态
  }
}
```

执行流程：
1. `loading = true` → 页面显示「加载中...」
2. `await getPosts(...)` → 异步请求，函数**暂停**在这里（但不阻塞其他代码）
3. 请求完成 → 继续执行第 3 行，把数据塞进 ref
4. ref 变了 → Vue 自动重新渲染
5. `finally` 关掉加载状态

## ⚠️ 常见错误：忘了加 async

```js
onMounted(load)          // ✅ 传函数引用，即使 load 是 async 也没问题

onMounted(async () => {  // ✅ 箭头函数也可以加 async
  await load()
})

onMounted(() => {         // ⚠️ 无 async，下面用 await 会报错
  await load()            // ❌
})
```

## 🎯 小结

| 关键字 | 作用 |
|--------|------|
| `async` | 标记函数为异步，返回 Promise |
| `await` | 等 Promise 完成，取结果 |
| `try { }` | 包住可能出错的代码 |
| `catch (e)` | 捕获错误 |
| `finally { }` | 无论成功失败都执行 |

## 🔗 相关

- 下一章：[06 Promise 是什么](06-promise.md)
