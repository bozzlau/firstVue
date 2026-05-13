# 12 · 组件通信：props

## 💡 什么是 props

Vue 组件默认是独立的，不知道外面有什么数据。**props 是父组件向子组件传数据的唯一正式通道**。

```
HomeView（父）
    ↓ :post="post"   传数据
PostCard（子）
    ↑ defineProps    声明接收
```

数据流是**单向的**：只能从父流向子，子不能直接修改 props。

## 🧩 子组件声明接收

`PostCard.vue`：

```js
defineProps({
  post: { type: Object, required: true },
})
```

`defineProps` 是 Vue 3 编译器宏，不需要 import。常见配置：

```js
defineProps({
  title:   { type: String,  required: true },
  count:   { type: Number,  default: 0 },
  visible: { type: Boolean, default: false },
  items:   { type: Array,   default: () => [] },  // 数组/对象默认值用函数
  post:    { type: Object,  required: true },
})
```

## 🧩 父组件传值

```html
<!-- 静态字符串（不加冒号） -->
<PostCard title="你好" />

<!-- 动态值（加冒号，值是 JS 表达式） -->
<PostCard :post="post" />
<PostCard :count="page * 10" />
```

加 `:` 和不加的区别：
- 不加：值是字符串字面量，`count="42"` 传的是字符串 `"42"`
- 加 `:`：值是 JS 表达式，`:count="42"` 传的是数字 `42`

## 🧩 子组件使用 props

模板里直接用 prop 名，不需要前缀：

```html
<h2>{{ post.title }}</h2>
<img :src="post.cover_image" />
```

script 里需要接收返回值：

```js
const props = defineProps({ post: Object })
console.log(props.post.title)
```

如果 script 里用不到（只在模板里用），可以不接收返回值，直接 `defineProps({...})`。

## ⚠️ 不能直接修改 props

```js
props.post.title = '新标题'   // ❌
```

数据从哪来就在哪改。`post` 是父组件的数据，应该在父组件里改，改完自动流下来。子组件需要触发父组件改数据时用 `emit`。

## 🧩 PostCard 里的细节

**点击整张卡片跳转：**
```html
<article @click="router.push(`/posts/${post.slug}`)">
```

**日期格式化：**
```html
{{ new Date(post.created_at).toLocaleDateString('zh-CN') }}
```
`post.created_at` 是 ISO 字符串，`new Date()` 转成 Date 对象，`.toLocaleDateString('zh-CN')` 格式化成 `2026/5/13`。

**文字截断：**
```html
<h2 class="line-clamp-2">{{ post.title }}</h2>
```
Tailwind 工具类，超过 2 行显示省略号。

## 🎯 小结

| 点 | 记住 |
|----|------|
| props | 父 → 子传数据的唯一正式通道 |
| `defineProps` | 子组件声明接收，可加类型和默认值 |
| `:prop="值"` | 加 `:` 值是 JS 表达式，不加是字符串 |
| 单向数据流 | 子不能直接改 props |
| 模板里 | 直接用 prop 名，不需要 `props.` 前缀 |

## 🔗 相关

- 上一章：[11 Vue 模板语法](11-vue-template-directives.md)
- 下一章：[13 Vue Router：路由与导航](13-vue-router.md)
