<script setup>
import { ref, onMounted } from 'vue'
import { getPosts } from '../../api/posts'
import PostCard from '../../components/public/PostCard.vue'

const posts = ref([])
const total = ref(0)
const page = ref(1)
const loading = ref(false)

async function load() {
  loading.value = true
  try {
    const data = await getPosts({ page: page.value, page_size: 10 })
    posts.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div>
    <div v-if="loading" class="text-center py-12 text-gray-400">加载中...</div>

    <div v-else-if="posts.length === 0" class="text-center py-12 text-gray-400">
      暂无文章
    </div>

    <div v-else class="space-y-4">
      <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>

    <div v-if="total > 10" class="mt-6 flex justify-center">
      <div class="flex gap-2">
        <button
          :disabled="page === 1"
          class="px-3 py-1.5 text-sm border rounded disabled:opacity-40 hover:bg-gray-50"
          @click="page--; load()"
        >
          上一页
        </button>
        <span class="px-3 py-1.5 text-sm text-gray-500">第 {{ page }} 页</span>
        <button
          :disabled="page * 10 >= total"
          class="px-3 py-1.5 text-sm border rounded disabled:opacity-40 hover:bg-gray-50"
          @click="page++; load()"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>
