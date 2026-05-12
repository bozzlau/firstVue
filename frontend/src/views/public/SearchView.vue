<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchPosts } from '../../api/posts'
import PostCard from '../../components/public/PostCard.vue'

const route = useRoute()
const router = useRouter()
const posts = ref([])
const total = ref(0)
const loading = ref(false)
const q = ref(route.query.q || '')

async function load() {
  if (!q.value.trim()) return
  loading.value = true
  try {
    const data = await searchPosts({ q: q.value, page: 1, page_size: 20 })
    posts.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

function doSearch() {
  router.replace({ query: { q: q.value } })
}

onMounted(load)
watch(() => route.query.q, (val) => {
  q.value = val || ''
  load()
})
</script>

<template>
  <div>
    <form @submit.prevent="doSearch" class="flex mb-6">
      <input
        v-model="q"
        type="text"
        placeholder="搜索文章..."
        class="flex-1 border border-gray-200 rounded-l px-4 py-2 text-sm outline-none focus:border-blue-400"
      />
      <button
        type="submit"
        class="bg-blue-500 text-white px-4 py-2 rounded-r text-sm hover:bg-blue-600"
      >
        搜索
      </button>
    </form>

    <p v-if="q && !loading" class="text-sm text-gray-500 mb-4">
      "{{ q }}" 共找到 {{ total }} 篇文章
    </p>

    <div v-if="loading" class="text-center py-12 text-gray-400">搜索中...</div>
    <div v-else-if="posts.length === 0 && q" class="text-center py-12 text-gray-400">没有找到相关文章</div>
    <div v-else class="space-y-4">
      <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
  </div>
</template>
