# 博客前端重设计：HUD 主题 → 温暖编辑风格

## Context

当前博客前端是暗色 HUD/终端风格（amber-dark 主题），用户希望将公开页面改为 `index-fluid-v2.html` 模板的温暖编辑风格（米白底色、衬线字体、橙珊瑚色 accent、流体动画）。管理后台（`.admin-scope`）完全不动。

---

## 目标设计特征（来自 index-fluid-v2.html）

- **色彩**：米白底 `#f9f8f6`、白色卡片、深炭色文字 `#1a1714`、橙珊瑚 accent `#e85d3a`、琥珀金 `#f5a623`、青绿 `#4ecdc4`
- **字体**：衬线（Iowan Old Style/Charter/Georgia）用于标题，系统 sans 用于正文，JetBrains Mono 用于标签/元数据
- **动效**：鼠标光晕、滚动 reveal、blob 浮动/变形、hover 上浮
- **布局**：粘性导航（毛玻璃）、Hero 两栏、标签导航栏、精选文章卡、文章列表 + 热度面板、深色 footer

---

## 文件改动范围

| 文件 | 改动 |
|------|------|
| `tailwind.config.js` | 新增 `ed.*` 颜色命名空间 + serif 字体 + 新动画 |
| `src/style.css` | 替换 HUD tokens/utilities → 编辑风格 tokens/utilities；保留 `.admin-scope` |
| `src/components/public/PublicLayout.vue` | 全新导航 + 侧边栏（热度面板）；保留 `provide('tocVisible')` |
| `src/views/public/HomeView.vue` | Hero + 标签导航 + 精选文章 + 文章列表 |
| `src/components/public/PostCard.vue` | 改为三列行式布局（标签 | 标题+摘要 | 日期） |
| `src/components/public/PostToc.vue` | 改为编辑风格 TOC |
| `src/components/public/HudPanel.vue` | 改为编辑风格 Panel（或新建 EdPanel.vue） |
| `src/views/public/PostView.vue` | 编辑风格文章页 |
| `src/views/public/CategoryView.vue` | 编辑风格分类页 |
| `src/views/public/TagView.vue` | 编辑风格标签页 |
| `src/views/public/SearchView.vue` | 编辑风格搜索页 |
| `src/views/public/AboutView.vue` | 编辑风格关于页 |

**不改动**：`src/style.css` 中 `.admin-scope` 块、所有 admin views/components、router、API 层、Pinia stores

---

## 实施步骤

### Step 1：tailwind.config.js

在 `theme.extend.colors` 中**新增** `ed` 命名空间（保留 `hud` 直到所有公开组件迁移完成，最后一步删除）：

```js
ed: {
  bg:       'rgb(var(--ed-bg) / <alpha-value>)',
  surface:  'rgb(var(--ed-surface) / <alpha-value>)',
  surface2: 'rgb(var(--ed-surface2) / <alpha-value>)',
  border:   'rgb(var(--ed-border) / <alpha-value>)',
  fg:       'rgb(var(--ed-fg) / <alpha-value>)',
  muted:    'rgb(var(--ed-muted) / <alpha-value>)',
  accent:   'rgb(var(--ed-accent) / <alpha-value>)',
  accent2:  'rgb(var(--ed-accent2) / <alpha-value>)',
  accent3:  'rgb(var(--ed-accent3) / <alpha-value>)',
}
```

新增 `serif` 字体族：`['Iowan Old Style', 'Charter', 'Georgia', 'serif']`

新增动画：`blob-float`、`blob-morph`、`fade-up`

### Step 2：style.css

**替换** `:root` 块（5 个 HUD 主题 → 1 个编辑主题）：
```css
:root {
  --ed-bg: 249 248 246;
  --ed-surface: 255 255 255;
  --ed-surface2: 240 237 232;
  --ed-border: 229 224 216;
  --ed-fg: 26 23 20;
  --ed-muted: 138 130 120;
  --ed-accent: 232 93 58;
  --ed-accent2: 245 166 35;
  --ed-accent3: 78 205 196;
}
```

**替换** `html, body` 基础样式（米白底、深色文字、系统 sans）

**新增** CSS：
- `.cursor-glow`（fixed 全屏，用 CSS 变量 `--cursor-x/y` 驱动 radial-gradient）
- `.reveal` / `.reveal.is-visible`（滚动 reveal 动画）
- `@keyframes blob-float`、`@keyframes blob-morph`
- `@layer components`：`.ed-panel`、`.ed-tag`、`.ed-btn-primary`、`.ed-btn-ghost`、`.ed-input`、`.ed-article-row`
- `.prose-ed`（替换 `.prose-hud`，衬线字体、编辑风格代码块/引用）

**保留不动**：`.admin-scope { ... }` 整块

### Step 3：HudPanel.vue → 改为 EdPanel

直接修改 `HudPanel.vue`，改为编辑风格 panel（白色卡片、圆角、细边框），保持相同 props 接口（`label`、`status`、`noPad`）以避免修改所有调用方。

### Step 4：PostToc.vue

改为编辑风格 TOC（白色背景、衬线标题、accent 高亮激活项）。保留所有逻辑不变，只改模板样式。

### Step 5：PostCard.vue

改为三列行式布局，匹配模板的 `.article-row`：
- 左列（~100px）：第一个 tag pill
- 中列（flex-1）：serif 标题 + 摘要，hover 变 accent 色
- 右列（~80px）：日期（mono）+ 分类

保留 `props`、`router`、`code`、`dateStr` 计算属性。

### Step 6：PublicLayout.vue

**导航**：
- 粘性，毛玻璃效果（`backdrop-blur`，米白半透明背景）
- Logo：衬线字体，accent 渐变点
- 导航链接：文章、关于
- 搜索图标（点击展开）
- 移除 ThemeSwitcher、StatusDot、时钟

**布局**：
- 保留两栏 grid（主内容 + 右侧边栏）
- 文章页保留三栏（TOC + 主内容 + 侧边栏）
- 保留 `provide('tocVisible', tocVisible)`

**右侧边栏**：
- 分类列表（编辑风格）
- 标签云（热度面板，logarithmic 缩放 + accent 颜色渐变）
- 移除 HUD 系统状态信息

**鼠标光晕**：在 `onMounted` 中监听 `mousemove`，更新 CSS 变量 `--cursor-x/y`

**滚动 reveal**：在 `onMounted` 中设置 IntersectionObserver，为 `.reveal` 元素添加 `.is-visible`

**Footer**：深色背景（`--ed-fg`）、波浪 SVG 分隔线、品牌 + 社交链接

### Step 7：HomeView.vue

**Hero 区域**：
- 两栏 grid（左：标题/简介/CTA，右：最近文章卡片 + 统计）
- 动态数据：`totalPosts`（从 PublicLayout 通过 `inject` 或直接 API 获取）、`tags.length`、建站年数
- 最近 3 篇文章：新增 API 调用 `getPosts({ page: 1, page_size: 3 })`
- Blob 动画背景

**标签导航栏**：
- 粘性（`top: 56px`），水平滚动
- 从 PublicLayout 通过 `inject` 获取 tags，或直接调用 `getTags()`
- 点击跳转 `/tag/:slug`，当前路由高亮

**精选文章**：
- 取第一篇文章（或 `is_featured` 字段，若无则取最新）
- 两栏卡片：左侧深色视觉区（blob + 大字）+ 右侧内容

**文章列表**：
- 使用新版 PostCard（行式布局）
- 保留分页逻辑

### Step 8：PostView.vue

- 文章头部：衬线大标题、日期/分类/标签（编辑风格）
- 正文：`.prose-ed` 类
- 评论区：编辑风格卡片
- 将 `document.querySelectorAll('.prose-hud h2[id]...')` 改为 `.prose-ed h2[id]...`

### Step 9：CategoryView.vue、TagView.vue、SearchView.vue

- 替换 HUD frame/标签为编辑风格 header
- 保留所有逻辑和 PostCard 使用

### Step 10：AboutView.vue

- 改为编辑风格个人介绍页（白色卡片、衬线标题、简洁布局）
- 保留内容数据

### Step 11：清理

- 从 `tailwind.config.js` 删除 `hud.*` 颜色和 HUD 动画
- 从 `style.css` 删除所有 HUD 变量和 `.prose-hud`（`.admin-scope` 保留）
- 删除 `ThemeSwitcher.vue`、`StatusDot.vue`（若不再使用）

### Step 12：将本方案文档保存到项目中

将本文档复制到 `docs/editorial-redesign-plan.md`，让项目本身记录这次重设计的背景、决策和分支说明。

### Step 13：更新项目文档

在 `CLAUDE.md` 中补充分支说明，记录两个分支各自保留的 UI 版本：

```
## 分支说明

- `master`：HUD 终端风格（暗色，amber accent，多主题切换）
- `feat/editorial-redesign`：编辑/杂志风格（米白底，橙珊瑚 accent，衬线字体，流体动画）
  参考设计稿：/Users/lyb/openDesign/blog/index-fluid-v2.html

如需切换版本：git checkout master 或 git checkout feat/editorial-redesign
如需合并新设计到主线：在 master 上执行 git merge feat/editorial-redesign
```

---

## 数据流说明

- **Hero 统计**：`totalPosts` 已在 PublicLayout 中获取，通过 `provide/inject` 传给 HomeView；`tags.length` 同理；建站年数硬编码
- **Hero 最近文章**：HomeView 自行调用 `getPosts({ page: 1, page_size: 3 })`
- **标签导航**：HomeView 通过 `inject('tags')` 从 PublicLayout 获取（需在 PublicLayout 中 `provide('tags', tags)`）
- **热度面板**：PublicLayout 侧边栏直接使用已有的 `tagCloud` computed

---

## 验证方式

1. `cd frontend && npm run dev` 启动开发服务器
2. 访问 `http://localhost:6006` 验证首页 Hero、标签导航、文章列表
3. 点击文章验证 PostView 样式和 TOC
4. 访问 `/category/:slug`、`/tag/:slug`、`/search`、`/about` 验证各页面
5. 访问 `http://localhost:6006/admin` 验证管理后台样式未受影响
6. 检查鼠标光晕、滚动 reveal、blob 动画是否正常
7. 缩小窗口验证响应式布局（移动端 Hero 单栏、标签导航可滚动）
