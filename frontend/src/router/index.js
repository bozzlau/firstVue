import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  },
  routes: [
    // ── 公开博客（带侧边栏布局）──────────────────────────────────────────────
    {
      path: '/',
      component: () => import('../components/public/PublicLayout.vue'),
      children: [
        { path: '', component: () => import('../views/public/HomeView.vue') },
        { path: 'posts/:slug', component: () => import('../views/public/PostView.vue') },
        { path: 'category/:slug', component: () => import('../views/public/CategoryView.vue') },
        { path: 'tag/:slug', component: () => import('../views/public/TagView.vue') },
        { path: 'search', component: () => import('../views/public/SearchView.vue') },
        { path: 'about', component: () => import('../views/public/AboutView.vue') },
      ],
    },

    // ── 管理后台 ────────────────────────────────────────────────────────────
    { path: '/admin/login', component: () => import('../views/admin/LoginView.vue') },
    {
      path: '/admin',
      component: () => import('../components/admin/AdminLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: 'dashboard', component: () => import('../views/admin/DashboardView.vue') },
        { path: 'posts', component: () => import('../views/admin/PostsView.vue') },
        { path: 'posts/new', component: () => import('../views/admin/PostEditView.vue') },
        { path: 'posts/:id', component: () => import('../views/admin/PostEditView.vue') },
        { path: 'categories', component: () => import('../views/admin/CategoriesView.vue') },
        { path: 'tags', component: () => import('../views/admin/TagsView.vue') },
        { path: 'comments', component: () => import('../views/admin/CommentsView.vue') },
      ],
    },
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const auth = useAuthStore()
    if (!auth.isLoggedIn) {
      return { path: '/admin/login' }
    }
  }
})

export default router
