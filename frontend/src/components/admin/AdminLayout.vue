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
  <div class="flex min-h-screen">
    <div
      class="relative shrink-0 flex flex-col"
      :style="{ width: sidebarWidth + 'px', backgroundColor: '#1e293b' }"
    >
      <div class="text-white text-center py-5 font-semibold text-lg border-b border-slate-700 whitespace-nowrap overflow-hidden">
        博客管理
      </div>
      <el-menu
        :default-active="route.path"
        router
        background-color="#1e293b"
        text-color="#94a3b8"
        active-text-color="#ffffff"
      >
        <el-menu-item index="/admin/dashboard">仪表盘</el-menu-item>
        <el-menu-item index="/admin/posts">文章管理</el-menu-item>
        <el-menu-item index="/admin/categories">分类管理</el-menu-item>
        <el-menu-item index="/admin/tags">标签管理</el-menu-item>
        <el-menu-item index="/admin/comments">评论管理</el-menu-item>
      </el-menu>

      <div class="mt-auto border-t border-slate-700 p-3">
        <el-button text class="w-full !text-slate-400 hover:!text-white" @click="logout">退出登录</el-button>
      </div>

      <div
        class="absolute top-0 right-0 w-1 h-full cursor-col-resize group"
        @mousedown="startDrag"
      >
        <div
          class="w-full h-full transition-colors"
          :class="isDragging ? 'bg-blue-400' : 'bg-transparent group-hover:bg-blue-400'"
        />
      </div>
    </div>

    <div class="flex-1 bg-gray-50 p-6 overflow-auto min-w-0">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
:deep(.el-menu-item.is-active) {
  background-color: #334155 !important;
  border-left: none !important;
}

:deep(.el-menu-item:hover) {
  background-color: #273549 !important;
}

:deep(.el-menu) {
  border-right: none;
}
</style>
