# 03 · ES 模块：import 语法

## 💡 什么是模块

一个 JavaScript 项目有很多文件，它们之间需要互相引用。「模块」就是**一个文件导出一些东西，另一个文件导入使用**。

## 🧩 三种 import 写法

### 1. 具名导入（最常用）

```js
import { ref, onMounted } from 'vue'
```

花括号里写出**具体要用的名字**。`vue` 包导出了很多东西（`ref`、`reactive`、`computed`、`watch`、`onMounted`...），这里只要两个，按需取用。

**对应的导出语法：**
```js
// vue 包内部大致是这样
export function ref(value) { ... }
export function onMounted(fn) { ... }
```

### 2. 默认导入

```js
import client from './client'
```

没有花括号。对应的导出：

```js
// api/client.js 最后一行
export default client
```

一个文件**只能有一个** `export default`，但可以有多个具名 `export`。

### 3. 混合导入

```js
import client, { setToken } from './client'
//     ↑默认     ↑具名
```

## 🧩 项目里的实例

打开 `HomeView.vue`：

```js
import { ref, onMounted } from 'vue'               // 具名
import { getPosts } from '../../api/posts'         // 具名
import PostCard from '../../components/public/PostCard.vue'  // 默认
```

打开 `api/posts.js`：

```js
import client from './client'                     // 默认导入
export const getPosts = (params) => ...           // 具名导出
export const adminCreatePost = (data) => ...      // 具名导出
```

打开 `api/client.js` 最后：

```js
export default client                             // 默认导出
```

## ⚠️ 路径规则

相对路径必须以 `./` 或 `../` 开头：

| 写法 | 含义 |
|------|------|
| `./client` | 同目录下的 `client.js` |
| `../stores/auth` | 上一级的 `stores/auth.js` |
| `../../api/posts` | 上两级的 `api/posts.js` |
| `vue` | `node_modules` 里的包 |
| `element-plus` | `node_modules` 里的包 |

没有 `./` 的路径会被当成 npm 包名。

## 💡 为什么 Vue 3 鼓励具名导入

Vue 2 时代：
```js
import Vue from 'vue'
Vue.ref(...)      // 所有 API 都挂在 Vue 上
```
打包时即使你只用 `ref`，整个 Vue 对象都会被打包进去。

Vue 3 把 API 拆成独立导出，配合构建工具的 **tree-shaking**（摇树优化），没用到的代码会被自动剔除，打包体积更小。

## 🎯 小结

| 语法 | 用途 |
|------|------|
| `import { A, B } from 'x'` | 具名导入，要什么拿什么 |
| `import X from 'x'` | 默认导入，对应 `export default` |
| `import X, { A } from 'x'` | 混合 |
| 路径 `./` / `../` | 相对路径 |
| 路径 `xxx` | npm 包 |

## 🔗 相关

- 下一章：[04 生命周期钩子：onMounted](04-onmounted-lifecycle.md)
