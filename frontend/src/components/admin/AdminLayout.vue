<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const sidebarWidth = ref(200)
const isDragging = ref(false)
const MIN_WIDTH = 100  // 200px 的一半
const MAX_WIDTH = 400

const navItems = [
  { to: '/admin/dashboard',  label: '仪表盘',  icon: '⊞', exact: true },
  { to: '/admin/posts',      label: '文章管理', icon: '≡', exact: false },
  { to: '/admin/categories', label: '分类管理', icon: '⊟', exact: true },
  { to: '/admin/tags',       label: '标签管理', icon: '◈', exact: true },
  { to: '/admin/comments',   label: '评论管理', icon: '✉', exact: true },
]

function startDrag(e) {
  e.preventDefault()
  const startX = e.clientX
  const startWidth = sidebarWidth.value

  document.body.style.cursor = 'col-resize'
  document.body.style.userSelect = 'none'
  isDragging.value = true

  function onMove(e) {
    const delta = e.clientX - startX
    sidebarWidth.value = Math.max(MIN_WIDTH, Math.min(startWidth + delta, MAX_WIDTH))
  }

  function onUp() {
    isDragging.value = false
    document.body.style.cursor = ''
    document.body.style.userSelect = ''
    document.removeEventListener('mousemove', onMove)
    document.removeEventListener('mouseup', onUp)
  }

  document.addEventListener('mousemove', onMove)
  document.addEventListener('mouseup', onUp)
}

function logout() {
  auth.logout()
  router.push('/admin/login')
}
</script>

<template>
  <div class="admin-scope flex h-screen overflow-hidden bg-[#f6f9fc]">
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
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="no-underline flex items-center gap-2.5 px-2.5 py-1.5 rounded-md text-[13.5px] transition-colors"
          :class="(item.exact ? route.path === item.to : route.path.startsWith(item.to))
            ? 'bg-[#f0effe] text-[#635bff] font-medium'
            : 'text-[#697386] hover:bg-[#f6f9fc] hover:text-[#1a1f36]'"
        >
          <span class="text-base leading-none">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
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
    <div class="flex-1 flex flex-col min-w-0 overflow-auto p-6">
      <RouterView />
    </div>
  </div>
</template>
