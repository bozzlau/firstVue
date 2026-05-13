# 04 · 生命周期钩子：onMounted

## 💡 什么是生命周期

一个 Vue 组件从出生到消失要经历几个阶段：

```
创建（created）
    ↓
挂载（mounted）  ← DOM 生成并插入页面，能看到了
    ↓
更新（updated）  ← 数据变化触发重新渲染
    ↓
卸载（unmounted） ← 组件被销毁
```

每个阶段，Vue 都允许你「插入一段自己的代码」——这些入口叫**生命周期钩子**。

## 🧩 `onMounted` 用法

```js
import { ref, onMounted } from 'vue'

async function load() {
  // 请求数据
}

onMounted(load)           // 组件挂载后执行 load
// 或写成箭头函数
onMounted(() => load())
```

执行时机：**DOM 已经生成并插入页面之后**。

## ⚠️ 为什么不在顶层直接调用 load()

看起来这样也行：

```js
const posts = ref([])
load()                    // 直接调
async function load() { ... }
```

**问题：**
- `<script setup>` 里的顶层代码会在组件**创建阶段**就执行，这时 DOM 还没生成
- 如果 `load()` 需要操作 DOM（比如聚焦某个输入框），就会失败
- 最佳实践：和页面相关的副作用都放 `onMounted` 里

**这个项目里 `load()` 只发请求不操作 DOM**，理论上放顶层也能跑。但遵循约定更好，未来加需求时不会踩坑。

## 🧩 常用的几个钩子

| 钩子 | 触发时机 | 典型用途 |
|------|---------|---------|
| `onMounted` | 组件挂载后 | 请求数据、获取 DOM 节点、注册事件 |
| `onUnmounted` | 组件卸载前 | 清理定时器、解绑事件、取消订阅 |
| `onUpdated` | 数据变化引发的 DOM 更新后 | 很少直接用 |
| `onBeforeMount` | 挂载前 | 几乎不用 |

## 🧩 配对使用 mount / unmount

典型场景：注册全局事件要记得解绑，否则内存泄漏。

```js
import { onMounted, onUnmounted } from 'vue'

function handleResize() {
  console.log('窗口变化')
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
```

本项目 `AdminLayout.vue` 和 `PostEditView.vue` 的拖拽功能也是这个模式——只不过事件是在 `mousedown` 时临时绑定、`mouseup` 时立刻解绑，不需要用组件级别的钩子。

## 💡 为什么叫「钩子」（hook）

英文 hook 是"挂钩、钩子"的意思。Vue 框架在特定时机会**"回头看"**你有没有"挂"东西在这个钩子上，有就执行。你不需要关心框架怎么跑，只需要把代码「挂」到对应位置。

## 🎯 小结

| 点 | 记住 |
|----|------|
| 作用 | 在组件生命周期的特定时刻执行代码 |
| 用法 | `onMounted(回调函数)` |
| 时机 | DOM 已插入页面，可以操作 DOM / 发请求 |
| 来源 | `import { onMounted } from 'vue'` |
| 对偶 | `onUnmounted` 用来清理 |

## 🔗 相关

- 下一章：[05 异步基础：async / await / try / finally](05-async-await.md)
