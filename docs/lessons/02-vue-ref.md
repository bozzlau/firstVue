# 02 · Vue 3 响应式：ref

## 💡 为什么需要"响应式"

普通 JavaScript 变量变了，页面不会自动更新：

```js
let count = 0
count = 5   // 值变了，但页面上显示的还是 0
```

浏览器不知道"这个变量变了应该重新画页面"。Vue 要解决的就是这个问题——让数据变化**自动**触发页面更新。

## 🧩 `ref` 的用法

```js
import { ref } from 'vue'

const count = ref(0)   // 把 0 包装成响应式
```

`ref()` 返回的**不是**普通值，而是一个对象，真正的值在 `.value` 里：

```js
console.log(count)         // RefImpl { value: 0 }
console.log(count.value)   // 0
count.value = 5            // ✅ Vue 检测到，触发更新
count = 5                  // ❌ 这样是替换整个 ref 对象，失去响应式
```

## ⚠️ script 里必须写 `.value`

看 `HomeView.vue`：

```js
const posts = ref([])
const loading = ref(false)

async function load() {
  loading.value = true              // ✅ 要 .value
  const data = await getPosts(...)
  posts.value = data.items          // ✅ 要 .value
  loading.value = false             // ✅ 要 .value
}
```

## ⚠️ template 里不要写 `.value`

```html
<template>
  <div v-if="loading">加载中...</div>       <!-- 不是 loading.value -->
  <span>第 {{ page }} 页</span>              <!-- 不是 page.value -->
  <div v-for="post in posts">...</div>       <!-- 不是 posts.value -->
</template>
```

Vue 在模板里自动「解包」ref，帮你省掉了 `.value`。

## 💡 为什么要分 script 和 template 不一样

一开始觉得很别扭，但其实有道理：
- **script 里**：你可能同时操作 ref 对象本身（比如传给函数）和 `.value`，必须明确区分
- **template 里**：只会读取值，不会操作 ref 对象，自动解包更简洁

## 🧩 ref 能包装什么

任何值都可以：

```js
ref(0)              // 数字
ref('hello')        // 字符串
ref(true)           // 布尔
ref([])             // 数组
ref({ name: 'a' })  // 对象
ref(null)           // null
```

## 🎯 小结

| 点 | 记住 |
|----|------|
| 作用 | 让数据变化自动触发页面更新 |
| 来源 | `import { ref } from 'vue'` |
| 用法 | `const x = ref(初始值)` |
| script 读写 | 要加 `.value` |
| template 读写 | 不加 `.value`（自动解包） |

## 🔗 相关

- 下一章：[03 ES 模块：import 语法](03-es-module-import.md)
- 对比：还有一个叫 `reactive` 的 API，只能包装对象/数组，后面遇到再讲
