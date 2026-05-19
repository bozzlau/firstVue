# Admin UI Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the admin dashboard from a plain Element Plus default style to a Stripe Dashboard-inspired professional light theme.

**Architecture:** Keep all data logic and Element Plus complex components (el-table, el-dialog, el-pagination, md-editor-v3) intact. Replace visual styling via Tailwind utilities and Element Plus CSS variable overrides. Rewrite layout components (AdminLayout, LoginView, DashboardView) from scratch; restyle the remaining views.

**Tech Stack:** Vue 3, Tailwind CSS v3, Element Plus 2.14, scoped CSS overrides

---

## File Map

| File | Action |
|------|--------|
| `frontend/src/style.css` | Add Element Plus CSS variable overrides |
| `frontend/src/components/admin/AdminLayout.vue` | Full rewrite (template + style) |
| `frontend/src/views/admin/LoginView.vue` | Full rewrite (template + style) |
| `frontend/src/views/admin/DashboardView.vue` | Full rewrite (template) |
| `frontend/src/views/admin/PostsView.vue` | Restyle template, keep script |
| `frontend/src/views/admin/PostEditView.vue` | Restyle template, keep script |
| `frontend/src/views/admin/CategoriesView.vue` | Restyle template, keep script |
| `frontend/src/views/admin/TagsView.vue` | Restyle template, keep script |
| `frontend/src/views/admin/CommentsView.vue` | Restyle template, keep script |

---

## Task 1: Element Plus CSS Variable Overrides

**Files:**
- Modify: `frontend/src/style.css`

- [ ] **Step 1: Add admin theme overrides to style.css**

Append the following block at the end of `frontend/src/style.css`:

```css
/* ================================================================
 * Admin panel — Stripe-style light theme
 * Scoped to .admin-scope to avoid bleeding into public blog
 * ================================================================ */
.admin-scope {
  --el-color-primary: #635bff;
  --el-color-primary-light-3: #8b85ff;
  --el-color-primary-light-5: #b0acff;
  --el-color-primary-light-7: #d4d2ff;
  --el-color-primary-light-8: #e4e3ff;
  --el-color-primary-light-9: #f0effe;
  --el-color-primary-dark-2: #5851e8;

  --el-border-color: #e3e8ef;
  --el-border-color-light: #eef1f6;
  --el-border-color-lighter: #f0f4f8;

  --el-bg-color: #ffffff;
  --el-bg-color-page: #f6f9fc;
  --el-fill-color-light: #f6f9fc;
  --el-fill-color-blank: #ffffff;

  --el-text-color-primary: #1a1f36;
  --el-text-color-regular: #1a1f36;
  --el-text-color-secondary: #697386;
  --el-text-color-placeholder: #aab7c4;

  --el-border-radius-base: 6px;
  --el-border-radius-small: 4px;

  --el-box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --el-box-shadow-light: 0 1px 2px rgba(0,0,0,0.04);
}
```

- [ ] **Step 2: Start dev server and verify no public blog styles changed**

```bash
cd frontend && npm run dev
```

Open `http://localhost:6006` — public blog should look identical to before.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/style.css
git commit -m "style: add admin Stripe theme CSS variable overrides"
```

---

## Task 2: AdminLayout Rewrite

**Files:**
- Modify: `frontend/src/components/admin/AdminLayout.vue`

- [ ] **Step 1: Replace the entire template and style block**

Keep the existing `<script setup>` block unchanged (all JS logic stays). Replace `<template>` and `<style scoped>` with:

```vue
<template>
  <div class="admin-scope flex min-h-screen bg-[#f6f9fc]">
    <!-- Sidebar -->
    <div
      class="relative shrink-0 flex flex-col bg-white border-r border-[#e3e8ef]"
      :style="{ width: sidebarWidth + 'px' }"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-5 py-4 border-b border-[#e3e8ef]">
        <div class="w-7 h-7 rounded-md bg-[#635bff] flex items-center justify-center text-white text-sm font-bold shrink-0">B</div>
        <div class="overflow-hidden">
          <div class="text-sm font-semibold text-[#1a1f36] whitespace-nowrap">博客管理</div>
          <div class="text-[11px] text-[#697386] whitespace-nowrap">Admin Dashboard</div>
        </div>
      </div>

      <!-- Nav -->
      <nav class="flex-1 px-2.5 py-3 space-y-0.5">
        <div class="px-2.5 pt-2 pb-1 text-[11px] font-semibold text-[#697386] uppercase tracking-wider">概览</div>
        <router-link
          to="/admin/dashboard"
          class="flex items-center gap-2.5 px-2.5 py-1.5 rounded-md text-[13.5px] transition-colors"
          :class="route.path === '/admin/dashboard'
            ? 'bg-[#f0effe] text-[#635bff] font-medium'
            : 'text-[#697386] hover:bg-[#f6f9fc] hover:text-[#1a1f36]'"
        >
          <span class="text-base leading-none">⊞</span>
          <span>仪表盘</span>
        </router-link>

        <div class="px-2.5 pt-3 pb-1 text-[11px] font-semibold text-[#697386] uppercase tracking-wider">内容</div>
        <router-link
          to="/admin/posts"
          class="flex items-center gap-2.5 px-2.5 py-1.5 rounded-md text-[13.5px] transition-colors"
          :class="route.path.startsWith('/admin/posts')
            ? 'bg-[#f0effe] text-[#635bff] font-medium'
            : 'text-[#697386] hover:bg-[#f6f9fc] hover:text-[#1a1f36]'"
        >
          <span class="text-base leading-none">≡</span>
          <span>文章管理</span>
        </router-link>
        <router-link
          to="/admin/categories"
          class="flex items-center gap-2.5 px-2.5 py-1.5 rounded-md text-[13.5px] transition-colors"
          :class="route.path === '/admin/categories'
            ? 'bg-[#f0effe] text-[#635bff] font-medium'
            : 'text-[#697386] hover:bg-[#f6f9fc] hover:text-[#1a1f36]'"
        >
          <span class="text-base leading-none">⊟</span>
          <span>分类管理</span>
        </router-link>
        <router-link
          to="/admin/tags"
          class="flex items-center gap-2.5 px-2.5 py-1.5 rounded-md text-[13.5px] transition-colors"
          :class="route.path === '/admin/tags'
            ? 'bg-[#f0effe] text-[#635bff] font-medium'
            : 'text-[#697386] hover:bg-[#f6f9fc] hover:text-[#1a1f36]'"
        >
          <span class="text-base leading-none">⊞</span>
          <span>标签管理</span>
        </router-link>
        <router-link
          to="/admin/comments"
          class="flex items-center gap-2.5 px-2.5 py-1.5 rounded-md text-[13.5px] transition-colors"
          :class="route.path === '/admin/comments'
            ? 'bg-[#f0effe] text-[#635bff] font-medium'
            : 'text-[#697386] hover:bg-[#f6f9fc] hover:text-[#1a1f36]'"
        >
          <span class="text-base leading-none">✉</span>
          <span>评论管理</span>
        </router-link>
      </nav>

      <!-- User / Logout -->
      <div class="border-t border-[#e3e8ef] px-2.5 py-3">
        <div class="flex items-center gap-2.5 px-2.5 py-1.5 rounded-md hover:bg-[#f6f9fc] cursor-pointer group" @click="logout">
          <div class="w-7 h-7 rounded-full bg-gradient-to-br from-[#635bff] to-[#a78bfa] flex items-center justify-center text-white text-xs font-semibold shrink-0">A</div>
          <div class="flex-1 overflow-hidden">
            <div class="text-[13px] font-medium text-[#1a1f36] whitespace-nowrap">admin</div>
            <div class="text-[11px] text-[#697386]">管理员</div>
          </div>
          <span class="text-[#697386] group-hover:text-[#e53e3e] transition-colors text-sm">⏻</span>
        </div>
      </div>

      <!-- Drag handle -->
      <div
        class="absolute top-0 right-0 w-1 h-full cursor-col-resize group"
        @mousedown="startDrag"
      >
        <div
          class="w-full h-full transition-colors"
          :class="isDragging ? 'bg-[#635bff]' : 'bg-transparent group-hover:bg-[#635bff]/30'"
        />
      </div>
    </div>

    <!-- Main -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
a { text-decoration: none; }
</style>
```

- [ ] **Step 2: Verify in browser**

Open `http://localhost:6006/admin/dashboard` — sidebar should show white background, indigo active state, user row at bottom.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/admin/AdminLayout.vue
git commit -m "feat: rewrite AdminLayout with Stripe-style sidebar"
```

---

## Task 3: LoginView Rewrite

**Files:**
- Modify: `frontend/src/views/admin/LoginView.vue`

- [ ] **Step 1: Replace template (keep script unchanged)**

```vue
<template>
  <div class="admin-scope min-h-screen bg-[#f6f9fc] flex items-center justify-center px-4">
    <div class="w-full max-w-sm">
      <!-- Card -->
      <div class="bg-white border border-[#e3e8ef] rounded-[10px] shadow-[0_4px_24px_rgba(0,0,0,0.08)] px-8 py-8">
        <!-- Logo + Title -->
        <div class="flex items-center gap-3 mb-6">
          <div class="w-8 h-8 rounded-lg bg-[#635bff] flex items-center justify-center text-white font-bold text-base shrink-0">B</div>
          <div>
            <div class="text-base font-semibold text-[#1a1f36]">博客管理后台</div>
            <div class="text-[12px] text-[#697386]">请使用管理员账号登录</div>
          </div>
        </div>

        <el-form :model="form" @submit.prevent="handleLogin" label-position="top">
          <el-form-item label="用户名">
            <el-input v-model="form.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              show-password
            />
          </el-form-item>

          <el-alert
            v-if="error"
            :title="error"
            type="error"
            show-icon
            :closable="false"
            class="mb-4"
          />

          <el-button
            type="primary"
            native-type="submit"
            :loading="loading"
            class="w-full !mt-2"
          >
            登录
          </el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>
```

- [ ] **Step 2: Verify in browser**

Open `http://localhost:6006/admin/login` — centered white card with logo, indigo login button.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/admin/LoginView.vue
git commit -m "feat: rewrite LoginView with Stripe-style card"
```

---

## Task 4: DashboardView Rewrite

**Files:**
- Modify: `frontend/src/views/admin/DashboardView.vue`

- [ ] **Step 1: Replace template (keep script unchanged)**

```vue
<template>
  <div>
    <!-- Topbar -->
    <div class="sticky top-0 z-10 bg-white border-b border-[#e3e8ef] px-7 h-14 flex items-center justify-between">
      <span class="text-[15px] font-semibold text-[#1a1f36]">仪表盘</span>
      <router-link to="/admin/posts/new">
        <el-button type="primary" size="small">+ 新建文章</el-button>
      </router-link>
    </div>

    <!-- Content -->
    <div class="p-7" v-loading="loading">
      <!-- Stats -->
      <div class="grid grid-cols-3 gap-4 mb-6 max-w-2xl">
        <div class="bg-white border border-[#e3e8ef] rounded-lg px-5 py-5">
          <div class="text-[11px] font-semibold text-[#697386] uppercase tracking-wider mb-2">文章总数</div>
          <div class="text-[28px] font-semibold text-[#1a1f36] leading-none mb-1.5">{{ totalPosts }}</div>
          <div class="text-[12px] text-[#697386]">已发布文章</div>
        </div>
        <div class="bg-white border border-[#e3e8ef] rounded-lg px-5 py-5">
          <div class="text-[11px] font-semibold text-[#697386] uppercase tracking-wider mb-2">待审评论</div>
          <div class="text-[28px] font-semibold leading-none mb-1.5" :class="pendingComments > 0 ? 'text-[#f59e0b]' : 'text-[#1a1f36]'">{{ pendingComments }}</div>
          <div class="text-[12px]" :class="pendingComments > 0 ? 'text-[#f59e0b]' : 'text-[#697386]'">{{ pendingComments > 0 ? '需要处理' : '暂无待审' }}</div>
        </div>
        <div class="bg-white border border-[#e3e8ef] rounded-lg px-5 py-5">
          <div class="text-[11px] font-semibold text-[#697386] uppercase tracking-wider mb-2">快速操作</div>
          <router-link to="/admin/posts/new" class="block text-[13px] text-[#635bff] hover:underline mb-1">+ 新建文章</router-link>
          <router-link to="/admin/comments" class="block text-[13px] text-[#635bff] hover:underline">审核评论</router-link>
        </div>
      </div>
    </div>
  </div>
</template>
```

- [ ] **Step 2: Verify in browser**

Open `http://localhost:6006/admin/dashboard` — three stat cards in a row, sticky topbar.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/admin/DashboardView.vue
git commit -m "feat: rewrite DashboardView with Stripe-style stat cards"
```

---

## Task 5: PostsView Restyle

**Files:**
- Modify: `frontend/src/views/admin/PostsView.vue`

- [ ] **Step 1: Replace template (keep script unchanged)**

```vue
<template>
  <div>
    <!-- Topbar -->
    <div class="sticky top-0 z-10 bg-white border-b border-[#e3e8ef] px-7 h-14 flex items-center justify-between">
      <span class="text-[15px] font-semibold text-[#1a1f36]">文章管理</span>
      <el-button type="primary" size="small" @click="router.push('/admin/posts/new')">+ 新建文章</el-button>
    </div>

    <div class="p-7">
      <!-- Toolbar -->
      <div class="flex items-center gap-3 mb-4">
        <el-input
          placeholder="搜索文章…"
          style="max-width: 260px"
          clearable
        />
        <el-checkbox v-model="includeDeleted" @change="load">显示已删除</el-checkbox>
      </div>

      <!-- Table card -->
      <div class="bg-white border border-[#e3e8ef] rounded-lg overflow-hidden">
        <el-table
          :data="posts"
          v-loading="loading"
          :border="false"
          style="width: 100%"
        >
          <el-table-column prop="title" label="标题" show-overflow-tooltip>
            <template #default="{ row }">
              <span :class="row.deleted_at ? 'line-through text-[#aab7c4]' : 'text-[#1a1f36]'">{{ row.title }}</span>
              <div class="text-[11px] text-[#697386] mt-0.5">{{ row.slug }}</div>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <span v-if="row.deleted_at" class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11.5px] font-medium bg-[#f0f4f8] text-[#697386]">
                <span class="w-1.5 h-1.5 rounded-full bg-[#aab7c4]"></span>已删除
              </span>
              <span v-else-if="row.published" class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11.5px] font-medium bg-[#e6f9f2] text-[#09b57a]">
                <span class="w-1.5 h-1.5 rounded-full bg-[#09b57a]"></span>已发布
              </span>
              <span v-else class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11.5px] font-medium bg-[#fff4e6] text-[#f59e0b]">
                <span class="w-1.5 h-1.5 rounded-full bg-[#f59e0b]"></span>草稿
              </span>
            </template>
          </el-table-column>
          <el-table-column label="分类" width="100">
            <template #default="{ row }">
              <span class="text-[13px] text-[#697386]">{{ row.category?.name || '—' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="views" label="浏览量" width="80">
            <template #default="{ row }">
              <span class="text-[13px] text-[#697386]">{{ row.views }}</span>
            </template>
          </el-table-column>
          <el-table-column label="创建时间" width="120">
            <template #default="{ row }">
              <span class="text-[13px] text-[#697386]">{{ new Date(row.created_at).toLocaleDateString('zh-CN') }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="160">
            <template #default="{ row }">
              <template v-if="!row.deleted_at">
                <button
                  class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#c7c4ff] text-[#635bff] bg-white hover:bg-[#f0effe] transition-colors mr-1.5"
                  @click="router.push(`/admin/posts/${row.id}`)"
                >编辑</button>
                <el-popconfirm title="确认删除？" @confirm="remove(row.id)">
                  <template #reference>
                    <button class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#fecaca] text-[#e53e3e] bg-white hover:bg-[#fff5f5] transition-colors">删除</button>
                  </template>
                </el-popconfirm>
              </template>
              <button
                v-else
                class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#a7f3d0] text-[#09b57a] bg-white hover:bg-[#f0fdf9] transition-colors"
                @click="restore(row.id)"
              >恢复</button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- Pagination -->
      <div class="mt-4 flex justify-end">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @change="load"
        />
      </div>
    </div>
  </div>
</template>
```

- [ ] **Step 2: Verify in browser**

Open `http://localhost:6006/admin/posts` — table inside white card, status badges with colored dots, outline action buttons.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/admin/PostsView.vue
git commit -m "feat: restyle PostsView with Stripe-style table and badges"
```

---

## Task 6: CategoriesView and TagsView Restyle

**Files:**
- Modify: `frontend/src/views/admin/CategoriesView.vue`
- Modify: `frontend/src/views/admin/TagsView.vue`

- [ ] **Step 1: Replace CategoriesView template (keep script unchanged)**

```vue
<template>
  <div>
    <div class="sticky top-0 z-10 bg-white border-b border-[#e3e8ef] px-7 h-14 flex items-center justify-between">
      <span class="text-[15px] font-semibold text-[#1a1f36]">分类管理</span>
      <el-button type="primary" size="small" @click="openCreate">+ 新建分类</el-button>
    </div>

    <div class="p-7">
      <div class="bg-white border border-[#e3e8ef] rounded-lg overflow-hidden">
        <el-table :data="categories" v-loading="loading" :border="false" style="width:100%">
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="slug" label="Slug" />
          <el-table-column prop="description" label="描述" show-overflow-tooltip />
          <el-table-column label="操作" width="140">
            <template #default="{ row }">
              <button
                class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#c7c4ff] text-[#635bff] bg-white hover:bg-[#f0effe] transition-colors mr-1.5"
                @click="openEdit(row)"
              >编辑</button>
              <el-popconfirm title="确认删除？" @confirm="remove(row.id)">
                <template #reference>
                  <button class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#fecaca] text-[#e53e3e] bg-white hover:bg-[#fff5f5] transition-colors">删除</button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <el-dialog v-model="dialogVisible" :title="editing ? '编辑分类' : '新建分类'" width="400px">
      <el-form :model="form" label-position="top">
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="Slug"><el-input v-model="form.slug" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>
```

- [ ] **Step 2: Replace TagsView template (keep script unchanged)**

```vue
<template>
  <div>
    <div class="sticky top-0 z-10 bg-white border-b border-[#e3e8ef] px-7 h-14 flex items-center justify-between">
      <span class="text-[15px] font-semibold text-[#1a1f36]">标签管理</span>
      <el-button type="primary" size="small" @click="openCreate">+ 新建标签</el-button>
    </div>

    <div class="p-7">
      <div class="bg-white border border-[#e3e8ef] rounded-lg overflow-hidden">
        <el-table :data="tags" v-loading="loading" :border="false" style="width:100%">
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="slug" label="Slug" />
          <el-table-column label="操作" width="140">
            <template #default="{ row }">
              <button
                class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#c7c4ff] text-[#635bff] bg-white hover:bg-[#f0effe] transition-colors mr-1.5"
                @click="openEdit(row)"
              >编辑</button>
              <el-popconfirm title="确认删除？" @confirm="remove(row.id)">
                <template #reference>
                  <button class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#fecaca] text-[#e53e3e] bg-white hover:bg-[#fff5f5] transition-colors">删除</button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <el-dialog v-model="dialogVisible" :title="editing ? '编辑标签' : '新建标签'" width="360px">
      <el-form :model="form" label-position="top">
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="Slug"><el-input v-model="form.slug" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>
```

- [ ] **Step 3: Verify in browser**

Open `/admin/categories` and `/admin/tags` — both show sticky topbar, white table card, outline action buttons.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/admin/CategoriesView.vue frontend/src/views/admin/TagsView.vue
git commit -m "feat: restyle CategoriesView and TagsView with Stripe-style tables"
```

---

## Task 7: CommentsView Restyle

**Files:**
- Modify: `frontend/src/views/admin/CommentsView.vue`

- [ ] **Step 1: Replace template (keep script unchanged)**

```vue
<template>
  <div>
    <div class="sticky top-0 z-10 bg-white border-b border-[#e3e8ef] px-7 h-14 flex items-center justify-between">
      <span class="text-[15px] font-semibold text-[#1a1f36]">评论管理</span>
      <!-- Tab filter -->
      <div class="flex rounded-md border border-[#e3e8ef] overflow-hidden">
        <button
          v-for="opt in [{value:'all',label:'全部'},{value:'pending',label:'待审核'},{value:'approved',label:'已通过'}]"
          :key="opt.value"
          class="px-3 py-1.5 text-[12.5px] font-medium transition-colors"
          :class="filter === opt.value
            ? 'bg-[#635bff] text-white'
            : 'bg-white text-[#697386] hover:bg-[#f6f9fc]'"
          @click="filter = opt.value"
        >{{ opt.label }}</button>
      </div>
    </div>

    <div class="p-7">
      <div class="bg-white border border-[#e3e8ef] rounded-lg overflow-hidden">
        <el-table :data="filtered()" v-loading="loading" :border="false" style="width:100%">
          <el-table-column prop="author_name" label="作者" width="100" />
          <el-table-column prop="author_email" label="邮箱" width="180" show-overflow-tooltip />
          <el-table-column prop="content" label="内容" show-overflow-tooltip />
          <el-table-column prop="post_id" label="文章ID" width="80" />
          <el-table-column label="状态" width="90">
            <template #default="{ row }">
              <span v-if="row.approved" class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11.5px] font-medium bg-[#e6f9f2] text-[#09b57a]">
                <span class="w-1.5 h-1.5 rounded-full bg-[#09b57a]"></span>已通过
              </span>
              <span v-else class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11.5px] font-medium bg-[#fff4e6] text-[#f59e0b]">
                <span class="w-1.5 h-1.5 rounded-full bg-[#f59e0b]"></span>待审核
              </span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="160">
            <template #default="{ row }">
              <button
                v-if="!row.approved"
                class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#a7f3d0] text-[#09b57a] bg-white hover:bg-[#f0fdf9] transition-colors mr-1.5"
                @click="approve(row.id)"
              >通过</button>
              <el-popconfirm title="确认删除？" @confirm="remove(row.id)">
                <template #reference>
                  <button class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#fecaca] text-[#e53e3e] bg-white hover:bg-[#fff5f5] transition-colors">删除</button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>
```

- [ ] **Step 2: Verify in browser**

Open `/admin/comments` — tab filter buttons in topbar, status badges, outline action buttons.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/admin/CommentsView.vue
git commit -m "feat: restyle CommentsView with tab filter and Stripe-style table"
```

---

## Task 8: PostEditView Restyle

**Files:**
- Modify: `frontend/src/views/admin/PostEditView.vue`

- [ ] **Step 1: Replace template (keep script unchanged)**

```vue
<template>
  <div v-loading="loading" class="flex flex-col h-full">
    <!-- Topbar -->
    <div class="sticky top-0 z-10 bg-white border-b border-[#e3e8ef] px-7 h-14 flex items-center justify-between shrink-0">
      <div class="flex items-center gap-2 text-[13px]">
        <router-link to="/admin/posts" class="text-[#697386] hover:text-[#635bff] transition-colors">文章管理</router-link>
        <span class="text-[#e3e8ef]">/</span>
        <span class="text-[#1a1f36] font-medium">{{ isEdit ? '编辑文章' : '新建文章' }}</span>
      </div>
      <div class="flex gap-2">
        <el-button @click="router.push('/admin/posts')">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </div>
    </div>

    <!-- Editor area -->
    <div ref="containerRef" class="flex flex-1 min-h-0 overflow-hidden">
      <!-- Main -->
      <div class="flex-1 min-w-0 overflow-y-auto p-7 space-y-4" :style="{ minWidth: MIN_MAIN + 'px' }">
        <el-form :model="form" label-position="top">
          <div class="flex gap-3">
            <el-form-item label="标题" class="flex-[2]">
              <el-input v-model="form.title" />
            </el-form-item>
            <el-form-item label="Slug（URL 路径）" class="flex-1">
              <el-input v-model="form.slug" />
            </el-form-item>
          </div>
          <el-form-item label="摘要">
            <el-input v-model="form.summary" placeholder="一句话描述文章内容" />
          </el-form-item>
          <el-form-item label="正文">
            <MdEditor v-model="form.content" style="height: 500px" />
          </el-form-item>
        </el-form>
      </div>

      <!-- Drag handle -->
      <div
        class="w-3 shrink-0 cursor-col-resize flex items-center justify-center group"
        @mousedown="startDrag"
      >
        <div
          class="w-px h-full transition-colors"
          :class="isDragging ? 'bg-[#635bff]' : 'bg-[#e3e8ef] group-hover:bg-[#635bff]/50'"
        />
      </div>

      <!-- Sidebar -->
      <div
        class="shrink-0 overflow-y-auto border-l border-[#e3e8ef] bg-white"
        :style="{ width: sidebarWidth + 'px', minWidth: MIN_SIDEBAR + 'px' }"
      >
        <el-form :model="form" label-position="top" class="p-5 space-y-1">
          <!-- Publish settings -->
          <div class="text-[11px] font-semibold text-[#697386] uppercase tracking-wider mb-3">发布设置</div>
          <el-form-item label="发布状态">
            <el-switch v-model="form.published" active-text="已发布" inactive-text="草稿" />
          </el-form-item>

          <div class="border-t border-[#e3e8ef] my-4"></div>

          <!-- Meta -->
          <div class="text-[11px] font-semibold text-[#697386] uppercase tracking-wider mb-3">分类与标签</div>
          <el-form-item label="分类">
            <el-select v-model="form.category_id" clearable placeholder="选择分类" class="w-full">
              <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="标签">
            <el-select v-model="form.tag_ids" multiple placeholder="选择标签" class="w-full">
              <el-option v-for="tag in tags" :key="tag.id" :label="tag.name" :value="tag.id" />
            </el-select>
          </el-form-item>

          <div class="border-t border-[#e3e8ef] my-4"></div>

          <div class="text-[11px] font-semibold text-[#697386] uppercase tracking-wider mb-3">封面图</div>
          <el-form-item label="封面图 URL">
            <el-input v-model="form.cover_image" placeholder="https://..." />
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
```

- [ ] **Step 2: Verify in browser**

Open `/admin/posts/new` — breadcrumb topbar, white sidebar with section dividers, drag handle still works.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/admin/PostEditView.vue
git commit -m "feat: restyle PostEditView with Stripe-style sidebar and topbar"
```

---

## Task 9: Final Verification

- [ ] **Step 1: Run build to check for errors**

```bash
cd frontend && npm run build
```

Expected: no errors, build completes successfully.

- [ ] **Step 2: Full flow test**

1. Open `http://localhost:6006/admin/login` — Stripe-style login card
2. Login → `/admin/dashboard` — stat cards, sticky topbar
3. Navigate to 文章管理 — table in white card, status badges, outline buttons
4. Click 新建文章 → PostEditView — breadcrumb, draggable sidebar
5. Navigate to 分类管理, 标签管理 — consistent table style
6. Navigate to 评论管理 — tab filter in topbar
7. Drag sidebar in AdminLayout — drag handle turns indigo, width changes
8. Open public blog at `http://localhost:6006` — HUD theme unchanged

- [ ] **Step 3: Final commit**

```bash
git add -A
git commit -m "feat: complete admin UI redesign to Stripe-style light theme"
```
