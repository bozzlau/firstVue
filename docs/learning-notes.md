# 学习笔记 — Python + Vue 个人 Blog 项目

记录开发过程中学到的概念和解释，方便随时回顾。

---

## 架构概念

### 前后端分离是什么意思？
传统网站：浏览器请求一个 URL，服务器返回一整个 HTML 页面。
前后端分离：后端只返回 JSON 数据，前端自己决定怎么渲染成页面。

好处：
- 后端可以同时服务 Web 前端、手机 App、小程序，接口是通用的
- 前后端可以独立开发、独立部署
- 职责清晰，后端管数据，前端管展示

本项目：后端跑在 `localhost:8000`，前端跑在 `localhost:5173`，两者通过 HTTP 请求通信。

---

### 单页应用（SPA）是什么？
传统网站每跳一个页面，浏览器都要向服务器请求新的 HTML 文件，页面会刷新。

SPA（Single Page Application）：整个网站只有一个 HTML 文件，页面切换是 JavaScript 在浏览器里动态替换内容，不刷新页面。

Vue 就是用来构建 SPA 的框架。Vue Router 负责管理"当前 URL 对应显示哪个组件"。

---

## 后端概念

### REST API 是什么？
后端不直接返回 HTML，而是返回 JSON 数据。每个 URL 对应一种"资源"，用 HTTP 方法表达操作意图：

| HTTP 方法 | 含义 | 例子 |
|-----------|------|------|
| GET | 查询 | `GET /api/posts` 获取文章列表 |
| POST | 新建 | `POST /api/posts` 创建新文章 |
| PUT | 修改 | `PUT /api/posts/1` 修改文章 |
| DELETE | 删除 | `DELETE /api/posts/1` 删除文章 |

---

### JWT Token 是什么？为什么用它？
登录成功后，后端返回一个加密字符串（Token）。之后每次请求管理接口，前端在请求头里带上这个 Token，后端验证它是否有效、是否过期。

**和传统 Session 的区别：**
- Session：服务器存登录状态，每次请求带 Session ID，服务器查表验证
- JWT：服务器不存状态，Token 本身包含用户信息和签名，服务器只需验证签名

JWT 更适合前后端分离，因为后端不需要维护 Session 存储。

**JWT 安全注意事项：**
1. Token 存 `httpOnly Cookie`，不存 `localStorage`（防止 XSS 攻击读取）
2. 设置较短过期时间（1小时），配合 Refresh Token 自动续期
3. 密钥用足够长的随机字符串，存环境变量，不写进代码
4. 生产环境必须用 HTTPS

---

### Model vs Schema 的区别

**Model（数据库模型）**：用 Python 类描述数据库表结构，是数据库层的概念。

**Schema（Pydantic 模式）**：定义 API 接口接收什么数据、返回什么数据，是 API 层的概念。

同一个概念（比如"用户"），在两层的"形状"不同：

```python
# Model — 数据库里存的（完整的）
class User:
    id, username, email, hashed_password, created_at

# Schema — API 登录时接收的
class UserLogin:
    username, password  # 明文密码，用完就丢，不存数据库

# Schema — API 返回给前端的
class UserResponse:
    id, username, email, created_at
    # 注意：没有 hashed_password，绝对不能暴露给前端
```

**类比：** 身份证（Model）上有所有信息，但网站注册（Schema）只填用户名和邮箱，个人主页（Schema）只显示用户名。同一个"你"，不同场合展示不同信息。

---

### 为什么要有 services 层？
路由（router）负责"接收请求、返回响应"，services 负责"具体怎么处理数据"。

不分层的问题：路由函数越来越长，查数据库、处理业务逻辑、格式化返回值全混在一起，难以维护和测试。

分层后：路由只有几行（调用 service），service 专注业务逻辑，各司其职。

---

### 逻辑删除 vs 物理删除

**物理删除**：`DELETE FROM post WHERE id=1`，数据彻底消失，无法恢复。

**逻辑删除**：不真正删除，在表里加 `deleted_at` 字段，删除时设为当前时间，查询时过滤掉有值的记录。

本项目用逻辑删除，原因：
- 文章是花时间写的内容，误删可以恢复
- 这是生产系统的主流做法

配合 `PostLog` 表记录每次操作（发布/删除/恢复），保留完整历史。

---

## 前端概念

### Vue Router 是什么？
管理"URL → 组件"映射的工具。

```
/                → HomePage 组件
/posts/my-blog   → PostDetail 组件（:slug = "my-blog"）
/admin/posts     → AdminPosts 组件
```

**路由守卫（Navigation Guard）**：每次跳转前执行的钩子函数。用来保护 `/admin/*` 路由：检查是否已登录，没登录就跳到 `/admin/login`。写一次，所有管理页面自动受保护。

---

### Pinia 是什么？
Vue 的状态管理库。解决的问题：某些数据（比如"当前用户是否已登录"）需要在很多组件里用到，如果靠组件间传递会很麻烦。

Pinia 提供一个全局 store，任何组件都可以直接读取和修改，不需要层层传递。

---

### views vs components 的区别

| | views | components |
|--|-------|------------|
| 对应关系 | 和路由一一对应 | 被多个页面复用 |
| 例子 | `HomePage.vue`、`PostDetail.vue` | `PostCard.vue`、`CommentForm.vue` |
| 特点 | 通常比较大，是页面的"骨架" | 专注单一功能，可复用 |

---

### api/ 目录的作用
把所有 HTTP 请求集中管理，页面组件只调用函数，不直接写 axios。

**好处：**
- 后端地址变了，只改 `api/client.js` 一个地方
- JWT Token 在 `client.js` 里统一附加，不用每个请求手动加
- 接口逻辑集中，方便维护

**类比 Python：** 就像不在每个函数里都写数据库连接，而是统一初始化 `db = Database()` 然后到处引用。

---

## UI 框架

### Element Plus
- Vue 3 最流行的 UI 组件库，中文文档完善
- 提供表格、表单、分页、弹窗等完整组件
- 风格偏企业后台，适合管理页面
- 本项目用于：`/admin/*` 所有管理后台页面

### Tailwind CSS
- 不是传统 UI 库，而是"工具类 CSS"
- 提供大量原子化 CSS class（如 `text-lg`、`flex`、`p-4`），自己组合样式
- 设计自由度高，适合做有个性的博客前台

### shadcn-vue
- 基于 Tailwind CSS 的组件集合
- 特点：把组件代码直接复制进你的项目（不是 npm 包），完全可定制
- 本项目用于：`/` 公开博客所有页面

---

*持续更新中……*
