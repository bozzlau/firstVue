# 26 · 完整链路串讲

这一课不讲新知识，把前面 25 课的内容串成一条完整的线。

入口：**用户打开首页，文章列表出现在屏幕上。**

---

## 第一步：浏览器打开 `http://localhost:6006`

Vue Router（第 13 课）匹配到路径 `/`，渲染 `HomeView.vue`。

`PublicLayout.vue` 是父路由组件，先渲染导航栏和侧边栏，`HomeView` 渲染在 `<RouterView />` 的位置里。

---

## 第二步：HomeView 挂载，触发数据加载

`frontend/src/views/public/HomeView.vue`：

```javascript
const posts = ref([])      // 响应式变量，初始空数组（第 2 课）
const loading = ref(false)

async function load() {    // async 函数（第 5 课）
  loading.value = true
  try {
    const data = await getPosts({ page: page.value, page_size: 10 })
    posts.value = data.items   // 赋值触发页面重新渲染
    total.value = data.total
  } finally {
    loading.value = false
  }
}

onMounted(load)   // 组件挂载后执行 load（第 4 课）
```

`onMounted` 是 Vue 提供的生命周期钩子，组件挂载到 DOM 后自动调用 `load`。

---

## 第三步：getPosts 发出 HTTP 请求

`frontend/src/api/posts.js`：

```javascript
export const getPosts = (params) =>
  client.get('/api/posts', { params }).then((r) => r.data)
```

`client` 是 axios 实例（第 8 课），`{ params }` 会自动拼成 URL 查询字符串：`/api/posts?page=1&page_size=10`。

`.then((r) => r.data)` 取出响应体，返回一个 Promise（第 6、7 课）。`await` 等待 Promise 完成，拿到最终数据。

**axios 请求拦截器**（第 9 课）在发出前自动加上：

```
Authorization: Bearer eyJhbGci...
```

（如果 localStorage 里有 token 的话。公开接口没有 token 也能访问。）

---

## 第四步：请求到达 FastAPI

后端收到 `GET /api/posts?page=1&page_size=10`。

`backend/app/main.py` 里注册了路由，FastAPI 匹配到 `backend/app/routers/public/blog.py` 里的 `list_posts` 函数（第 17、18 课）：

```python
@router.get("/posts", response_model=PaginatedPosts)
def list_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
```

FastAPI 自动做了这些事：
- 从 URL 读取 `page=1`、`page_size=10`，转成整数
- 执行 `get_db()`，创建数据库连接注入为 `db`（第 18 课 Depends）

---

## 第五步：Service 层查数据库

路由调用 `svc.get_posts()`（第 21 课）：

```python
total, items = svc.get_posts(
    db,
    published_only=True,
    page=page,
    page_size=page_size,
)
```

Service 层用 SQLAlchemy 构建查询（第 19、21 课）：

```python
q = db.query(Post)
q = q.filter(Post.deleted_at.is_(None))    # 过滤软删除
q = q.filter(Post.published.is_(True))     # 只要已发布
total = q.count()
items = q.order_by(Post.created_at.desc()).offset(0).limit(10).all()
```

SQLAlchemy 把这段 Python 翻译成 SQL 执行，返回 `Post` 对象列表。

---

## 第六步：Pydantic 过滤输出字段

路由返回数据，FastAPI 按 `response_model=PaginatedPosts` 过滤（第 20 课）：

```python
return {"total": total, "items": items}
```

`Post` 对象有几十个字段，`PostSummaryOut` 只保留前端需要的：`id`、`title`、`slug`、`summary`、`views`、`category`、`tags`……

`content`（文章全文）、`deleted_at`、`logs` 等字段全部丢掉，序列化成 JSON 返回。

---

## 第七步：axios 响应拦截器处理返回

**axios 响应拦截器**（第 10 课）收到响应：

```javascript
response => response   // 正常就直接返回
error => {
  if (error.response?.status === 401) {
    // token 失效，清除登录状态，跳转登录页
  }
  return Promise.reject(error)
}
```

公开接口正常返回，拦截器直接放行。

---

## 第八步：Vue 响应式更新页面

`load()` 里的 `await` 拿到数据：

```javascript
const data = await getPosts(...)
posts.value = data.items   // 触发响应式更新
```

`posts` 是 `ref`（第 2 课），赋值后 Vue 自动重新渲染模板：

```html
<PostCard v-for="post in posts" :key="post.id" :post="post" />
```

`v-for` 循环（第 11 课）为每篇文章渲染一个 `PostCard` 组件，通过 `props`（第 12 课）把文章数据传进去。

文章列表出现在屏幕上。

---

## 完整链路图

```
用户打开 http://localhost:6006
    ↓
Vue Router 匹配路由 → 渲染 HomeView.vue          [第 13 课]
    ↓
onMounted 触发 load()                             [第 4 课]
    ↓
async/await 等待请求完成                           [第 5 课]
    ↓
getPosts() → axios 发出 GET /api/posts            [第 8 课]
    ↓
请求拦截器自动加 Authorization 头                  [第 9 课]
    ↓
FastAPI 匹配路由，解析参数，注入 db               [第 17、18 课]
    ↓
Pydantic Schema 验证参数                          [第 20 课]
    ↓
Service 层 SQLAlchemy 查数据库                    [第 19、21 课]
    ↓
response_model 过滤字段，序列化成 JSON            [第 20 课]
    ↓
响应拦截器处理返回                                 [第 10 课]
    ↓
posts.value = data.items → ref 触发重新渲染       [第 2 课]
    ↓
v-for 循环渲染 PostCard，props 传数据             [第 11、12 课]
    ↓
文章列表出现在屏幕上
```

## 🔗 涉及文件

- `frontend/src/views/public/HomeView.vue` — 首页组件
- `frontend/src/api/posts.js` — HTTP 请求封装
- `frontend/src/api/client.js` — axios 实例和拦截器
- `backend/app/routers/public/blog.py` — 路由层
- `backend/app/services/blog.py` — Service 层
- `backend/app/models/post.py` — 数据模型
- `backend/app/schemas/blog.py` — Pydantic Schema
