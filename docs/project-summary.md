# 个人博客项目总结

**项目类型：** 全栈个人博客  
**开发目的：** 通过实战学习 Python 后端 + Vue 3 前端的全栈开发  
**完成时间：** 2026-05-12

---

## 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| 后端框架 | FastAPI | REST API，自动生成 Swagger 文档 |
| ORM | SQLAlchemy 2.x | Python 类映射数据库表 |
| 数据库迁移 | Alembic | 管理数据库结构变更历史 |
| 认证 | JWT（Bearer Token） | 无状态管理员认证 |
| 数据库 | SQLite（开发） | 文件型数据库，无需安装 |
| 前端框架 | Vue 3 + Vite | 单页应用（SPA） |
| 路由 | Vue Router 4 | URL 与组件的映射 |
| 状态管理 | Pinia | 跨组件共享登录状态 |
| HTTP 客户端 | Axios | 前端发起 API 请求 |
| 后台 UI | Element Plus | 管理后台表格/表单/弹窗组件 |
| 前台样式 | Tailwind CSS v3 | 原子化 CSS，博客公开页面 |
| Markdown 编辑 | md-editor-v3 | 文章编辑器 |
| Markdown 渲染 | marked | 文章详情页正文渲染 |

---

## 项目结构

```
firstVue/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── main.py             # 应用入口，注册路由和中间件
│   │   ├── config.py           # 从 .env 读取配置
│   │   ├── database.py         # 数据库连接和 Session 工厂
│   │   ├── dependencies.py     # 公共依赖（JWT 验证）
│   │   ├── models/             # SQLAlchemy 数据库模型
│   │   │   └── post.py         # Post, Category, Tag, Comment, PostLog
│   │   ├── schemas/            # Pydantic 请求/响应格式
│   │   │   └── blog.py
│   │   ├── routers/
│   │   │   ├── public/         # 无需认证的公开接口
│   │   │   │   └── blog.py     # 文章列表、详情、评论、搜索
│   │   │   └── admin/          # 需要 JWT 的管理接口
│   │   │       ├── auth.py     # 登录
│   │   │       ├── posts.py    # 文章 CRUD + 软删除 + 恢复
│   │   │       ├── categories_tags.py
│   │   │       └── comments.py
│   │   └── services/
│   │       ├── auth.py         # 密码哈希、JWT 生成/验证
│   │       └── blog.py         # 所有业务逻辑（数据库操作）
│   ├── alembic/                # 数据库迁移文件
│   ├── tests/                  # pytest 测试
│   ├── requirements.txt
│   └── .env                    # 环境变量（不提交 git）
│
├── frontend/                   # Vue 3 前端
│   └── src/
│       ├── main.js             # 应用入口，注册 Pinia 和 Router
│       ├── api/                # 所有 HTTP 请求集中管理
│       │   ├── client.js       # axios 实例（自动附加 JWT Token）
│       │   ├── auth.js
│       │   ├── posts.js
│       │   ├── categories.js
│       │   ├── tags.js
│       │   └── comments.js
│       ├── stores/
│       │   ├── auth.js         # 登录状态 + token 持久化
│       │   └── post.js         # 文章列表缓存
│       ├── router/
│       │   └── index.js        # 路由配置 + 路由守卫
│       ├── components/
│       │   ├── public/
│       │   │   ├── PublicLayout.vue  # 顶部导航 + 侧边栏
│       │   │   └── PostCard.vue      # 文章卡片（可复用）
│       │   └── admin/
│       │       └── AdminLayout.vue   # 管理后台侧边栏布局
│       └── views/
│           ├── public/         # 博客公开页面
│           │   ├── HomeView.vue       # 首页文章列表
│           │   ├── PostView.vue       # 文章详情 + 评论区
│           │   ├── CategoryView.vue   # 分类筛选页
│           │   ├── TagView.vue        # 标签筛选页
│           │   ├── SearchView.vue     # 搜索结果页
│           │   └── AboutView.vue      # 关于我
│           └── admin/          # 管理后台页面
│               ├── LoginView.vue
│               ├── DashboardView.vue
│               ├── PostsView.vue      # 文章列表（含软删除/恢复）
│               ├── PostEditView.vue   # 新建/编辑文章（Markdown 编辑器）
│               ├── CategoriesView.vue
│               ├── TagsView.vue
│               └── CommentsView.vue   # 评论审核
│
└── docs/
    ├── learning-notes.md       # 开发过程中的学习笔记
    └── superpowers/
        ├── specs/              # 设计文档
        └── plans/              # 实现计划
```

---

## 功能清单

### 公开博客（访客可见）

- 首页文章列表，分页浏览
- 文章详情页，渲染 Markdown 正文
- 按分类/标签筛选文章
- 全文搜索（标题 + 摘要 + 正文）
- 文章评论（提交后等待审核）
- 侧边栏显示所有分类和标签

### 管理后台（需登录）

- JWT 登录认证，token 存 localStorage
- 仪表盘：文章总数、待审评论数
- 文章管理：新建/编辑（Markdown 编辑器）、发布/草稿切换、软删除/恢复
- 分类/标签管理：增删改
- 评论管理：审核通过/删除，按状态筛选

---

## 启动方式

```bash
# 后端（终端 1）
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8001
# API 文档：http://localhost:8001/docs

# 前端（终端 2）
cd frontend
npm run dev
# 博客首页：http://localhost:6006
# 管理后台：http://localhost:6006/admin/login
```

**默认管理员账号：** `admin` / `changeme123`

---

## API 接口概览

### 公开接口（无需认证）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/posts` | 文章列表（分页、分类/标签筛选） |
| GET | `/api/posts/:slug` | 文章详情（同时记录浏览量） |
| GET | `/api/categories` | 分类列表 |
| GET | `/api/tags` | 标签列表 |
| GET | `/api/search?q=关键词` | 搜索文章 |
| GET | `/api/posts/:slug/comments` | 文章评论 |
| POST | `/api/posts/:slug/comments` | 提交评论 |

### 管理接口（需要 Bearer JWT）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/admin/login` | 登录，返回 JWT |
| GET/POST/PUT/DELETE | `/admin/posts` | 文章 CRUD |
| POST | `/admin/posts/:id/restore` | 恢复软删除的文章 |
| GET | `/admin/posts/:id/logs` | 文章操作日志 |
| GET/POST/PUT/DELETE | `/admin/categories` | 分类管理 |
| GET/POST/PUT/DELETE | `/admin/tags` | 标签管理 |
| GET/PATCH/DELETE | `/admin/comments` | 评论管理 |

---

## 关键设计决策

### 软删除（Soft Delete）
文章删除时不从数据库移除，而是设置 `deleted_at` 字段为当前时间。公开接口自动过滤掉已删除文章，管理后台可以恢复。好处：误删可恢复，保留历史数据。

### PostLog 操作日志
每次文章状态变更（发布/草稿/删除/恢复）都写一条 `post_logs` 记录，保留完整操作历史，方便追溯。

### 分层架构（Router → Service → Model）
- **Router**：只负责解析请求、调用 Service、返回响应
- **Service**：所有业务逻辑和数据库操作集中在这里
- **Model**：只描述数据库表结构

好处：逻辑清晰，Service 可以被多个 Router 复用，也更容易测试。

### 前端 API 层集中管理
所有 HTTP 请求放在 `src/api/` 目录，页面组件只调用函数，不直接写 axios。axios 实例统一处理 JWT 附加和 401 跳转，改一处全局生效。

### 嵌套路由布局
公开页面嵌套在 `PublicLayout`（含导航栏和侧边栏）下，管理页面嵌套在 `AdminLayout`（含侧边菜单）下。布局组件只渲染一次，切换子页面时布局不重新挂载，性能更好。

---

## 运行测试

```bash
cd backend
pytest              # 运行所有测试
pytest -v           # 显示详细输出
```

测试使用内存 SQLite 数据库，每个测试用例独立建表/清表，互不干扰。
