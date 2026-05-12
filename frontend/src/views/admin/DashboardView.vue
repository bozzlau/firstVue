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
    <h2 class="text-xl font-semibold text-gray-800 mb-6">仪表盘</h2>

    <div class="grid grid-cols-2 gap-4 max-w-lg" v-loading="loading">
      <el-card shadow="never">
        <div class="text-3xl font-bold text-blue-600">{{ totalPosts }}</div>
        <div class="text-gray-500 mt-1">文章总数</div>
      </el-card>

      <el-card shadow="never">
        <div class="text-3xl font-bold text-orange-500">{{ pendingComments }}</div>
        <div class="text-gray-500 mt-1">待审评论</div>
      </el-card>
    </div>
  </div>
</template>
