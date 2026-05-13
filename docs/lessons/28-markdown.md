# 28 · Markdown 编辑与渲染

## 💡 两个不同的库，两个不同的场景

| 场景 | 库 | 作用 |
|------|-----|------|
| 后台写文章 | `md-editor-v3` | 所见即所得的 Markdown 编辑器 |
| 前台读文章 | `marked` | 把 Markdown 字符串转成 HTML |

两个都是第三方 npm 包，在 `frontend/package.json` 里。

---

## 🧩 编辑器：md-editor-v3（PostEditView.vue 第 4 行）

```javascript
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'   // 编辑器的样式，必须单独引入
```

在模板里使用：

```html
<MdEditor v-model="form.content" style="height: 100%" />
```

`v-model` 把编辑器内容和 `form.content` 双向绑定（第 15 课）——用户在编辑器里打字，`form.content` 自动更新；保存时直接把 `form.content` 发给后端。

`md-editor-v3` 是 Vue 3 专用的，提供左边写 Markdown、右边实时预览的分栏界面，工具栏支持加粗、插入图片等操作。

---

## 🧩 渲染：marked（PostView.vue 第 4 行）

```javascript
import { marked } from 'marked'   // marked 是第三方包
```

在模板里使用：

```html
<div
  class="prose prose-gray max-w-none"
  v-html="marked(post.content)"
/>
```

**`marked(post.content)`** — 把 Markdown 字符串转成 HTML 字符串：

```javascript
marked("# 标题\n\n**加粗**文字")
// → "<h1>标题</h1>\n<p><strong>加粗</strong>文字</p>"
```

**`v-html`** — Vue 的特殊指令，把字符串作为 HTML 插入到元素里。普通的 `{{ }}` 插值会把 HTML 标签当成文本显示，`v-html` 才会真正渲染成 HTML。

**`prose prose-gray`** — Tailwind CSS Typography 插件（第 16 课）提供的类，给 HTML 内容自动加上排版样式：标题有层级感、段落有间距、代码块有背景色。

---

## 🧩 Promise.all：并行请求（PostView.vue 第 20 行）

文章详情页需要同时加载文章内容和评论：

```javascript
const [p, c] = await Promise.all([
  getPost(route.params.slug),
  getComments(route.params.slug),
])
post.value = p
comments.value = c
```

**`Promise.all([...])`** — 同时发出多个请求，等所有请求都完成后才继续。

对比串行写法：

```javascript
// 串行：先等文章，再等评论，总时间 = 200ms + 150ms = 350ms
const p = await getPost(slug)
const c = await getComments(slug)

// 并行：同时发，总时间 = max(200ms, 150ms) = 200ms
const [p, c] = await Promise.all([getPost(slug), getComments(slug)])
```

`const [p, c] = ...` 是数组解构，`Promise.all` 返回一个数组，按顺序对应传入的每个 Promise 的结果。

---

## 🧩 watch：监听路由变化（PostView.vue 第 43 行）

```javascript
onMounted(load)
watch(() => route.params.slug, load)
```

**为什么需要 `watch`？**

从文章 A 跳到文章 B，URL 从 `/posts/article-a` 变成 `/posts/article-b`，但 Vue Router 复用了同一个 `PostView` 组件，不会重新挂载，所以 `onMounted` 不会再次触发。

`watch` 监听 `route.params.slug`，slug 一变就重新调用 `load()`，加载新文章的数据。

`() => route.params.slug` 是一个函数，返回要监听的值。每次这个值变化，`watch` 就调用第二个参数（`load`）。

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `md-editor-v3` | npm 包 | Vue 3 的 Markdown 编辑器组件 |
| `marked` | npm 包 | 把 Markdown 字符串转成 HTML |
| `v-html` | Vue | 把字符串作为 HTML 渲染，不是文本 |
| `prose` | Tailwind Typography 插件 | 给 HTML 内容自动加排版样式 |
| `Promise.all([...])` | JavaScript 内置 | 并行发多个请求，全部完成后继续 |
| `watch(getter, fn)` | Vue | 监听值变化，变了就执行 fn |

## 🔗 相关文件

- `frontend/src/views/admin/PostEditView.vue` — Markdown 编辑器
- `frontend/src/views/public/PostView.vue` — Markdown 渲染
