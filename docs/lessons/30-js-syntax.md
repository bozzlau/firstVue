# 30 · JavaScript 常用语法：箭头函数 / 模板字符串 / 可选链 / 解构赋值

这几个语法在项目里大量出现，但没有单独讲过。

---

## 🧩 箭头函数 `=>`（api/posts.js 第 5 行）

箭头函数是普通函数的简写语法，`=>` 是它的标志。

```javascript
// 普通函数
function add(a, b) {
  return a + b
}

// 箭头函数，完全等价
const add = (a, b) => {
  return a + b
}

// 只有一行 return 时，可以省略花括号和 return
const add = (a, b) => a + b
```

**项目里的三种形态：**

```javascript
// 形态 1：完整写法，多行逻辑，需要显式 return
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 形态 2：单行，省略花括号和 return，直接返回表达式
export const getPosts = (params) =>
  client.get('/api/posts', { params }).then((r) => r.data)

// 形态 3：单参数时括号可以省略
.then((r) => r.data)   // 有括号
.then(r => r.data)     // 省略括号，完全等价
```

**最常见的用法：作为参数传给另一个函数**

```javascript
// .then() 接收一个函数
client.get('/api/posts').then((r) => r.data)

// .filter() 对每个元素执行，返回 true 保留
[1, 2, 3, 4].filter((n) => n > 2)   // → [3, 4]

// .map() 对每个元素转换
[1, 2, 3].map((n) => n * 2)         // → [2, 4, 6]
```

| 写法 | 说明 |
|------|------|
| `(a, b) => { return a + b }` | 完整写法 |
| `(a, b) => a + b` | 单行，省略花括号和 return |
| `a => a * 2` | 单参数，省略括号 |
| `() => import(...)` | 无参数，括号不能省 |

---

## 🧩 模板字符串（client.js 第 10 行）

```javascript
config.headers.Authorization = `Bearer ${token}`
```

反引号（`` ` ``）包裹的字符串叫**模板字符串**，`${}` 里可以放任意 JavaScript 表达式：

```javascript
const name = "admin"
const age = 30

// 普通字符串拼接
"你好，" + name + "，你今年 " + age + " 岁"

// 模板字符串
`你好，${name}，你今年 ${age} 岁`
```

`${}` 里不只能放变量，任何表达式都行：

```javascript
`/admin/posts/${post.id}/logs`    // 变量
`第 ${page + 1} 页`               // 运算
`${isEdit ? '编辑' : '新建'}文章`  // 三元表达式
```

---

## 🧩 可选链 `?.`（client.js 第 18 行）

```javascript
if (error.response?.status === 401) {
```

`?.` 是**可选链操作符**，意思是：**如果左边的值是 `null` 或 `undefined`，就停止，返回 `undefined`，不报错**。

对比：

```javascript
// 没有可选链：error.response 是 undefined 时，访问 .status 直接报错
error.response.status   // TypeError: Cannot read properties of undefined

// 有可选链：error.response 是 undefined 时，返回 undefined，不报错
error.response?.status  // → undefined
```

网络请求失败时，`error.response` 可能不存在（比如断网）。用 `?.` 就不用先判断 `error.response` 是否存在再访问 `.status`。

可以连续使用：

```javascript
post?.category?.name   // post 或 category 任一为 null 都安全返回 undefined
```

---

## 🧩 解构赋值

### 数组解构（PostView.vue 第 20 行）

```javascript
const [p, c] = await Promise.all([
  getPost(route.params.slug),
  getComments(route.params.slug),
])
```

`Promise.all` 返回一个数组，数组解构按位置取值：

```javascript
const arr = [1, 2, 3]
const [a, b, c] = arr
// a = 1, b = 2, c = 3
```

等价的普通写法：

```javascript
const result = await Promise.all([getPost(slug), getComments(slug)])
const p = result[0]
const c = result[1]
```

### 对象解构（api/auth.js 第 8 行）

```javascript
const { data } = await client.post('/admin/login', form)
```

axios 返回的响应对象有很多字段（`status`、`headers`、`data`...），只需要 `data`，用对象解构直接取出来：

```javascript
const response = await client.post('/admin/login', form)
const data = response.data   // 普通写法

const { data } = await client.post('/admin/login', form)  // 解构写法，等价
```

对象解构可以同时取多个字段：

```javascript
const { status, data, headers } = response
```

也可以重命名：

```javascript
const { data: loginResult } = await client.post(...)
// loginResult 就是 response.data
```

---

## 🎯 小结

| 语法 | 记住 |
|------|------|
| `(a, b) => 表达式` | 箭头函数，普通函数的简写 |
| `` `${变量}` `` | 模板字符串，反引号包裹，`${}` 里放表达式 |
| `a?.b` | 可选链，`a` 为 null/undefined 时返回 undefined 不报错 |
| `const [a, b] = arr` | 数组解构，按位置取值 |
| `const { x } = obj` | 对象解构，按字段名取值 |

## 🔗 相关文件

- `frontend/src/api/client.js` — 模板字符串、可选链
- `frontend/src/views/public/PostView.vue` — 数组解构
- `frontend/src/api/auth.js` — 对象解构
