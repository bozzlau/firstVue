# 个人博客项目总结

**项目类型：** 全栈个人博客  
**开发目的：** 通过实战学习 Python 后端 + Vue 3 前端的全栈开发  
**完成时间：** 2026-05-13（持续迭代中）  
**当前版本：** v2.0 — HUD 主题系统升级（2026-05-16）

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
| 前台样式 | Tailwind CSS v3 + CSS 变量主题系统 | HUD 风格博客公开页，5 套可切换配色 |
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
│       │   ├── post.js         # 文章列表缓存
│       │   └── theme.js        # 当前主题 + localStorage 持久化
│       ├── router/
│       │   └── index.js        # 路由配置 + 路由守卫
│       ├── components/
│       │   ├── public/
│       │   │   ├── PublicLayout.vue  # 顶部 HUD 状态栏 + 侧边栏
│       │   │   ├── PostCard.vue      # HUD 时间轴卡片
│       │   │   ├── HudPanel.vue      # 通用 HUD 框面板（带四角 L 装饰）
│       │   │   ├── StatusDot.vue     # 呼吸状态点
│       │   │   └── ThemeSwitcher.vue # 顶栏主题切换下拉
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
- HUD 风格 UI + 5 套主题（3 暗 2 浅）实时切换，选择持久化

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

### 管理后台布局优化（2026-05-13）
- **可拖拽侧边栏**：`AdminLayout` 左侧导航栏宽度可拖拽调整（默认 200px，最小 100px，最大 400px），用原生 `mousemove` / `mouseup` 事件实现，不依赖第三方库。
- **退出登录移至侧边栏底部**：移除了原来独占 60px 的顶部 header，"退出登录"改放侧边栏底部（`mt-auto`），内容区从页面顶部直接开始，节省垂直空间。
- **文章编辑器右侧栏可拖拽**：`PostEditView` 右侧属性栏（发布状态/分类/标签/封面图）宽度可拖拽（默认 256px，最小 128px），主编辑区自动填满剩余空间。
- **编辑器表单紧凑化**：标题与 Slug 并排一行（2:1 比例），摘要改为单行输入，表单间距从 16px 缩为 8px，编辑器上方节省约 150px 垂直空间。

---

## v2.0 — HUD 主题系统升级（2026-05-16）

公开页前端从经典「白底 + 灰卡 + 蓝按钮」整体重构为 HUD（仪表盘）视觉风格，并配套上线**多主题切换系统**。后台 `/admin/*` 完全保留 Element Plus，本次升级零侵入。

### 视觉重构 — HUD 风格

完整重写了所有公开页（`HomeView` / `PostView` / `CategoryView` / `TagView` / `SearchView` / `AboutView`）和布局组件（`PublicLayout` / `PostCard`），引入「博客系统控制台」隐喻：

- **品牌符号**：顶栏 `▮▮▮ BLOG.SYS v1.0` + 实时时钟 + `● ONLINE` 呼吸状态点 + `003 POSTS` 计数
- **HUD 装饰原语**：`.hud-frame` 四角 L 形高亮 + `.hud-grid-bg` 极淡网格底 + `.hud-glow-bar` hover 时的左缘光柱 + `.hud-scan` 可选扫描线
- **HUD 文案**：区段用 `// LATEST_FEED` `// CATEGORY` `// TRANSMISSIONS` 等等宽前缀；按钮 `[ EXEC ]` `[ TRANSMIT ▸ ]`；空态 `// NO_DATA`；加载态 `[ LOADING ▮▮▮ ]`
- **数字感**：文章卡前缀 `[001]`（`padStart(3, '0')`）；日期前 `◆`；阅读量前 `▸`
- **新增原子组件**：`HudPanel.vue`（通用 HUD 框）、`StatusDot.vue`（呼吸状态点）
- **字体**：标题/UI 用 Space Grotesk，编号/时间戳/技术标签用 JetBrains Mono，正文用 Inter + 系统中文字体
- **prose 主题**：文章正文用自定义 `.prose-hud` 类，链接、代码块、引用、表格全部按 HUD 风重做

### 多主题切换系统

提供 5 套配色，可在顶栏 `◐ THEME` 切换，实时 0.35s 平滑过渡，无刷新：

| Key | 名称 | 模式 | 强调色 | 背景 |
|-----|------|------|--------|------|
| `amber-dark` | 琉珀控制台 | dark | `#ffb700` | `#121214` |
| `cyan-dark` | 电子终端 | dark | `#22d3ee` | `#0c1018` |
| `magenta-dark` | 赛博粉紫 | dark | `#ec4899` | `#120a18` |
| `paper-light` | 牛皮蓝图 | light | `#b87900` | `#f4eedf` |
| `frost-light` | 极地霜白 | light | `#0d9488` | `#eef2f7` |

### 实现要点

- **CSS 变量 + Tailwind alpha-value 占位**：`tailwind.config.js` 把 `colors.hud.*` 全部声明为 `rgb(var(--hud-*) / <alpha-value>)`，变量值用空格分隔的 RGB 三元组（如 `255 183 0`）。这样 `bg-hud-amber/10`、`border-hud-amber/60` 这类透明度变体在任何主题下都自动生效，**所有视图组件的 Tailwind class 一行没改**，只换底层 CSS 变量映射就完成主题切换。
- **主题数据源**：`stores/theme.js`（Pinia setup store）维护 `themes` 列表 + `current` 引用，`setTheme(key)` 同步写 `localStorage` 和 `<html data-theme="...">`，与现有 `auth.js` 模式保持一致。
- **FOUC 预防**：`index.html` 的 `<head>` 加内联 IIFE 脚本，在 Vue 启动前先把 `data-theme` 写到 `<html>` 上，首屏不闪默认主题。
- **全局过渡**：`body`、`.hud-frame`、`.hud-btn`、`.prose-hud` 等关键容器加 `transition: background-color/border-color/color 0.35s ease`，切换瞬间整页平滑变色。
- **切换 UI**：`ThemeSwitcher.vue` 顶栏触发 + 下拉浮层，每行展示色卡（背景 + 强调）、中文名、key 和 mode；点击外部 / `Esc` 自动关闭。

### 受影响文件

- 修改：`tailwind.config.js`、`src/style.css`（重写）、`index.html`、`src/main.js`、`PublicLayout.vue`、`PostCard.vue`、所有 `views/public/*.vue`
- 新增：`stores/theme.js`、`components/public/HudPanel.vue`、`components/public/StatusDot.vue`、`components/public/ThemeSwitcher.vue`
- 不动：所有 `views/admin/*`、`components/admin/*`、`api/*`、`router/*`、后端

---

## 运行测试

```bash
cd backend
pytest              # 运行所有测试
pytest -v           # 显示详细输出
```

测试使用内存 SQLite 数据库，每个测试用例独立建表/清表，互不干扰。
