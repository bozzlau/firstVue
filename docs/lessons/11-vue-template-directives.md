# 11 · Vue 模板语法：v-if / v-for / :key / {{ }} / :attr / @event

## 💡 什么是指令

HTML 本身没有条件渲染、循环这些能力。Vue 通过在标签上加 `v-` 开头的特殊属性来扩展 HTML，这些属性叫**指令**。

## 🧩 v-if / v-else-if / v-else

控制元素**是否渲染到 DOM**：

```html
<div v-if="loading">加载中...</div>
<div v-else-if="posts.length === 0">暂无文章</div>
<div v-else>文章列表</div>
```

- `loading` 为 true → 只渲染第一个，后两个不存在于 DOM
- `loading` 为 false 且 posts 为空 → 只渲染第二个
- 其他 → 只渲染第三个

⚠️ `v-else-if` 和 `v-else` 必须紧跟在 `v-if` 元素后面，中间不能插其他元素。

## 💡 v-if vs v-show

```html
<div v-if="show">...</div>    <!-- false 时不渲染，DOM 里没有 -->
<div v-show="show">...</div>  <!-- 始终渲染，false 时 display:none -->
```

| | v-if | v-show |
|--|------|--------|
| 切换开销 | 高（创建/销毁） | 低（改 CSS） |
| 初始开销 | 低（false 不渲染） | 高（始终渲染） |
| 适合 | 条件很少变化 | 频繁切换 |

## 🧩 v-for：循环渲染

```html
<PostCard v-for="post in posts" :key="post.id" :post="post" />
```

对数组每个元素渲染一次。可以拿索引：

```html
<div v-for="(post, index) in posts" :key="post.id">
  {{ index + 1 }}. {{ post.title }}
</div>
```

## 💡 :key 为什么必须加

没有 key：Vue 按位置对比，删除中间元素时可能复用错误的 DOM 节点，出现数据错乱。

有 key：Vue 按 id 精确匹配，只操作对应节点。

⚠️ key 必须唯一，用稳定的 id，**不要用数组索引**（删除元素后索引会变）。

## 🧩 {{ }} 插值表达式

```html
<span>第 {{ page }} 页</span>
```

双花括号里放 JavaScript **表达式**（有返回值的）：

```html
{{ page + 1 }}
{{ posts.length > 0 }}
{{ title.toUpperCase() }}
{{ isAdmin ? '管理员' : '访客' }}
```

⚠️ 只能是表达式，不能是语句：
```html
{{ if (x) { ... } }}   <!-- ❌ -->
{{ x > 0 ? x : 0 }}   <!-- ✅ -->
```

## 🧩 :属性 —— 动态属性绑定

`:` 是 `v-bind:` 的缩写，把 HTML 属性值绑定到 JS 表达式。

**关键区别：有冒号和没有冒号**

```html
<!-- 没有冒号：值是字符串 "post"，传给子组件的是文字 -->
<PostCard post="post" />

<!-- 有冒号：值是 JS 表达式，传给子组件的是 post 变量的内容 -->
<PostCard :post="post" />
```

更多例子（来自 `HomeView.vue`）：

```html
<!-- 动态禁用按钮 -->
<button :disabled="page === 1">上一页</button>
<button :disabled="page * 10 >= total">下一页</button>

<!-- 动态 key -->
<PostCard :key="post.id" v-for="post in posts" />

<!-- 动态图片地址 -->
<img :src="post.cover_image" />

<!-- 动态链接 -->
<a :href="'/posts/' + post.slug">阅读</a>
```

**规律：冒号后面的引号里是 JavaScript，没有冒号就是普通字符串。**

## 🧩 @事件 —— 事件监听

`@` 是 `v-on:` 的缩写，监听事件，触发时执行表达式：

```html
<button @click="page--; load()">上一页</button>
<input @input="handleInput" />
<form @submit.prevent="handleLogin">...</form>
```

`.prevent` 是**事件修饰符**，等价于在处理函数里调用 `event.preventDefault()`，阻止表单提交时的页面跳转。常见修饰符：

| 修饰符 | 作用 |
|--------|------|
| `.prevent` | 阻止默认行为（如表单跳转） |
| `.stop` | 阻止事件冒泡 |
| `.once` | 只触发一次 |

**`:` 和 `@` 的完整写法对照：**

```html
<!-- 完全等价 -->
<button v-bind:disabled="page === 1">上一页</button>
<button      :disabled="page === 1">上一页</button>

<button v-on:click="load()">刷新</button>
<button     @click="load()">刷新</button>
```

实际开发都用缩写（`:` 和 `@`），更简洁。

## 🎯 小结

| 指令 | 作用 |
|------|------|
| `v-if` / `v-else-if` / `v-else` | 条件渲染 |
| `v-show` | 条件显示（display:none） |
| `v-for="item in list"` | 循环渲染 |
| `:key` | 给循环元素唯一标识 |
| `{{ 表达式 }}` | 插值渲染 |
| `:属性` | 动态绑定 HTML 属性 |
| `@事件` | 监听 DOM 事件 |

## 🔗 相关

- 上一章：[10 axios 拦截器（下）](10-axios-response-interceptor.md)
- 下一章：[12 组件通信：props](12-vue-props.md)
