<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

function logout() {
  auth.logout()
  router.push('/admin/login')
}
</script>

<template>
  <el-container class="min-h-screen">
    <el-aside width="200px" class="bg-gray-900">
      <div class="text-white text-center py-5 font-semibold text-lg border-b border-gray-700">
        博客管理
      </div>
      <el-menu
        :default-active="route.path"
        router
        background-color="#111827"
        text-color="#d1d5db"
        active-text-color="#ffffff"
      >
        <el-menu-item index="/admin/dashboard">仪表盘</el-menu-item>
        <el-menu-item index="/admin/posts">文章管理</el-menu-item>
        <el-menu-item index="/admin/categories">分类管理</el-menu-item>
        <el-menu-item index="/admin/tags">标签管理</el-menu-item>
        <el-menu-item index="/admin/comments">评论管理</el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="flex items-center justify-end border-b bg-white px-6">
        <el-button text @click="logout">退出登录</el-button>
      </el-header>
      <el-main class="bg-gray-50">
        <RouterView />
      </el-main>
    </el-container>
  </el-container>
</template>
