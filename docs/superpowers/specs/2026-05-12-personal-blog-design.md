# Personal Blog Design Spec

**Date:** 2026-05-12  
**Stack:** FastAPI (Python) + Vue 3  
**Author:** lyb

---

## 1. 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端框架 | FastAPI | 自动生成 Swagger 文档，类型提示友好 |
| ORM | SQLAlchemy | Python 类映射数据库表，无需手写 SQL |
| 数据库迁移 | Alembic | 管理数据库结构变更历史 |
| 认证 | JWT（httpOnly Cookie） | 无状态认证，Token 存 Cookie 防 XSS |
| 数据库 | SQLite（开发）/ PostgreSQL（生产） | |
| 前端框架 | Vue 3 + Vite | 单页应用，组件化开发 |
| 路由 | Vue Router | URL 与组件的映射管理 |
| 状态管理 | Pinia | 跨组件共享状态（登录状态、数据缓存） |
| 后台 UI | Element Plus | 表格/表单/分页等管理组件开箱即用 |
| 前台 UI | Tailwind CSS + shadcn-vue | 设计自由，博客风格独特 |

---

## 2. 数据模型

### User（管理员）
```
id, username, email, hashed_password, created_at
```

### Category（分类）
```
id, name, slug, description
```
`slug`：URL 友好名称，如 `tech`、`life`

### Tag（标签）
```
id, name, slug
```

### Post（文章）
```
id, title, content(Markdown), summary, cover_image
status: draft | published
views
author_id → User
category_id → Category
tags → Tag（多对多）
deleted_at（逻辑删除，null 表示未删除）
created_at, updated_at
```

### Comment（评论）
```
id, post_id → Post
author_name, author_email, content
is_approved（审核开关）
created_at
```

### PostLog（操作日志）
```
id, post_id → Post
action: published | deleted | restored
operated_at
note（可选备注）
```

### 关键关系
- Post ↔ Category：多对一
- Post ↔ Tag：多对多
- Post ↔ Comment：一对多
- Post ↔ PostLog：一对多

### 删除策略
使用**逻辑删除**：`deleted_at` 字段记录删除时间，查询时过滤 `deleted_at IS NOT NULL`。每次状态变更同时写入 `PostLog`，保留完整操作历史。

---

## 3. API 接口

### 公开接口（无需认证）
```
GET  /api/posts                       文章列表（分页、分类/标签筛选）
GET  /api/posts/{slug}                文章详情（同时记录浏览量）
GET  /api/categories                  分类列表
GET  /api/tags                        标签列表
GET  /api/search?q=关键词             搜索文章
POST /api/posts/{slug}/comments       提交评论
GET  /api/posts/{slug}/comments       获取文章评论
```

### 管理接口（需要 JWT Token）
```
POST /api/auth/login                  登录，返回 JWT Token

GET    /api/admin/posts               所有文章（含草稿、已删除）
POST   /api/admin/posts               新建文章
PUT    /api/admin/posts/{id}          修改文章
DELETE /api/admin/posts/{id}          软删除
POST   /api/admin/posts/{id}/restore  恢复删除
GET    /api/admin/posts/{id}/logs     操作日志

POST/PUT/DELETE /api/admin/categories/{id}
POST/PUT/DELETE /api/admin/tags/{id}

GET  /api/admin/comments              所有评论（含待审核）
PUT  /api/admin/comments/{id}/approve 审核通过
DELETE /api/admin/comments/{id}       删除评论
```

---

## 4. 前端页面结构

### 公开页面（Tailwind + shadcn-vue）
```
/                    首页 — 最新文章列表 + 分类导航
/posts/:slug         文章详情 — 正文 + 评论区
/category/:slug      分类页
/tag/:slug           标签页
/search              搜索结果页
/about               关于我
```

### 管理后台（Element Plus）
```
/admin/login         登录页
/admin/dashboard     仪表盘
/admin/posts         文章列表
/admin/posts/new     新建文章（Markdown 编辑器）
/admin/posts/:id     编辑文章
/admin/categories    分类管理
/admin/tags          标签管理
/admin/comments      评论管理
```

所有 `/admin/*` 路由通过 Vue Router 路由守卫保护，未登录自动跳转 `/admin/login`。

---

## 5. 项目目录结构

### 后端
```
backend/
├── app/
│   ├── main.py          # FastAPI 入口，注册路由
│   ├── config.py        # 配置（从环境变量读取）
│   ├── database.py      # 数据库连接
│   ├── dependencies.py  # 公共依赖（DB会话、登录验证）
│   ├── models/          # SQLAlchemy 数据库模型
│   ├── schemas/         # Pydantic 请求/响应格式
│   ├── routers/
│   │   ├── public/      # 公开接口
│   │   └── admin/       # 管理接口
│   └── services/        # 业务逻辑层
├── alembic/             # 数据库迁移
├── requirements.txt
└── .env                 # 环境变量（不提交 git）
```

### 前端
```
frontend/src/
├── main.js
├── App.vue
├── router/index.js
├── stores/
│   ├── auth.js          # 登录状态
│   └── post.js          # 文章缓存
├── api/
│   ├── client.js        # axios 实例（自动附加 Token）
│   ├── posts.js
│   └── auth.js
├── views/
│   ├── public/          # 博客页面
│   └── admin/           # 管理后台
└── components/
    ├── public/
    └── admin/
```

---

## 6. 开发顺序

```
第一阶段：后端
  1. 搭建 FastAPI 项目骨架
  2. 定义数据库模型 + 运行迁移
  3. 实现公开 API
  4. 实现 JWT 登录认证
  5. 实现管理 API
  → 全程用 Swagger UI 测试

第二阶段：前端
  6. 搭建 Vue 3 项目，配置路由 + Pinia
  7. 安装 Element Plus + Tailwind + shadcn-vue
  8. 实现管理后台
  9. 实现公开博客页面

第三阶段：完善
  10. 评论功能
  11. 搜索功能
  12. Markdown 编辑器集成
```
