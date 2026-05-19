<script setup>
import { ref, onMounted } from 'vue'
import { adminGetPosts } from '../../api/posts'
import { adminGetComments } from '../../api/comments'

const totalPosts = ref(0)
const pendingComments = ref(0)
const loading = ref(true)

onMounted(async () => {
  try {
    const [postsData, commentsData] = await Promise.all([
      adminGetPosts({ page: 1, page_size: 1 }),
      adminGetComments(),
    ])
    totalPosts.value = postsData.total
    pendingComments.value = commentsData.filter((c) => !c.approved).length
  } finally {
    loading.value = false
  }
})
</script>

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
