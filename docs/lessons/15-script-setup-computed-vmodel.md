# 15 · Vue 补充知识点：script setup / computed / v-model

---

## 一、`<script setup>` 是什么

每个 Vue 组件文件都长这样：

```vue
<script setup>
// JavaScript 逻辑
</script>

<template>
  <!-- HTML 结构 -->
</template>

<style scoped>
/* CSS 样式 */
</style>
```

Vue 2 的写法（仅作对比）：

```js
export default {
  data() {
    return { posts: [], loading: false }
  },
  methods: {
    async load() { ... }
  },
  mounted() {
    this.load()
  }
}
```

Vue 3 引入**组合式 API**，`<script setup>` 是它的语法糖，等价于：

```js
export default {
  setup() {
    const posts = ref([])
    // ...
    return { posts }   // 要手动 return 才能在模板里用
  }
}
```

加了 `setup` 关键字之后：
- 不用写 `export default { setup() { ... } }` 这层包装
- 不用手动 `return`，所有顶层变量和函数**自动**暴露给模板
- `defineProps` 等编译器宏可以直接用，不用 import

项目里所有组件都用这种写法。

---

## 二、computed 计算属性

**来源：`vue` 包**，和 `ref` 一样需要 import：

```js
import { ref, computed } from 'vue'
```

### 为什么需要 computed

看 `frontend/src/stores/auth.js` 第 8 行：

```js
const isLoggedIn = computed(() => !!token.value)
```

为什么不用普通函数？

```js
function isLoggedIn() { return !!token.value }    // 普通函数
const isLoggedIn = computed(() => !!token.value)  // computed
```

区别：
- 普通函数：每次调用都重新执行，返回普通值，不是响应式的
- `computed`：依赖的数据没变就返回缓存结果；依赖变了自动重新计算，返回**响应式的值**

`token` 变了 → `isLoggedIn` 自动更新 → 路由守卫、模板里用到它的地方也自动更新。

### `!!` 是什么

把任意值转成布尔值的技巧：

```js
!!null       // false
!!undefined  // false
!!0          // false

!!'abc'      // true（有值）
!!'eyJ...'   // true（有 token）
```

规律：有值是 `true`，`null` / `undefined` / `0` / 空字符串是 `false`。

### 项目里的实例

`frontend/src/views/admin/PostEditView.vue`：

```js
const isEdit = computed(() => !!route.params.id)
```

- 访问 `/admin/posts/new` → `route.params.id` 是 `undefined` → `false` → 新建模式
- 访问 `/admin/posts/5` → `route.params.id` 是 `'5'` → `true` → 编辑模式

模板里：

```html
<h2>{{ isEdit ? '编辑文章' : '新建文章' }}</h2>
```

URL 变了，标题自动跟着变。

---

## 三、v-model 双向绑定

打开 `frontend/src/views/admin/LoginView.vue`：

```js
const form = ref({ username: '', password: '' })
```

```html
<el-input v-model="form.username" />
<el-input v-model="form.password" />
```

### 什么是双向绑定

之前学的 `:value` 是单向的——只能把数据显示到页面，用户输入了什么数据不会自动更新。

`v-model` 是双向的：

```
数据 → 页面（显示）
页面 → 数据（用户输入时自动同步）
```

### v-model 的本质

`v-model` 是两件事的缩写：

```html
<!-- v-model 写法 -->
<input v-model="form.username" />

<!-- 等价的展开写法 -->
<input
  :value="form.username"
  @input="form.username = $event.target.value"
/>
```

- `:value` → 数据显示到输入框
- `@input` → 用户输入时把新值写回数据

### 登录表单的完整流程

1. `form` 是 ref 包装的对象，初始值都是空字符串
2. 用户在输入框打字 → `v-model` 自动把值同步到 `form.value.username`
3. 点登录按钮时直接用 `form.value` 里的数据，不需要手动读输入框

```js
await auth.login(form.value.username, form.value.password)
```

### ⚠️ ref 对象里的字段不用 `.value`

```js
const form = ref({ username: '', password: '' })

// script 里
form.value.username = 'admin'   // 外层 ref 要 .value，里面字段直接用

// template 里
v-model="form.username"         // 模板自动解包外层 ref，直接写字段名
```

---

## 🎯 小结

| 概念 | 来源 | 记住 |
|------|------|------|
| `<script setup>` | Vue 3 语法 | 组合式 API 的简洁写法，顶层变量自动暴露给模板 |
| `computed` | `vue` 包 | 基于响应式数据派生新值，有缓存，自动更新 |
| `!!值` | JavaScript | 把任意值转成布尔值 |
| `v-model` | Vue 指令 | 双向绑定，`:value` + `@input` 的缩写 |

## 🔗 相关文件

- `frontend/src/stores/auth.js` —— `computed` 实例
- `frontend/src/views/admin/PostEditView.vue` —— `computed` + `isEdit`
- `frontend/src/views/admin/LoginView.vue` —— `v-model` 表单实例
