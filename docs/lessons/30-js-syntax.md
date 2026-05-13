# 30 · JavaScript 常用语法：模板字符串 / 可选链 / 解构赋值

这三个语法在项目里大量出现，但没有单独讲过。

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
| `` `${变量}` `` | 模板字符串，反引号包裹，`${}` 里放表达式 |
| `a?.b` | 可选链，`a` 为 null/undefined 时返回 undefined 不报错 |
| `const [a, b] = arr` | 数组解构，按位置取值 |
| `const { x } = obj` | 对象解构，按字段名取值 |

## 🔗 相关文件

- `frontend/src/api/client.js` — 模板字符串、可选链
- `frontend/src/views/public/PostView.vue` — 数组解构
- `frontend/src/api/auth.js` — 对象解构
