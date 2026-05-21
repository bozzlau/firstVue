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
  if (!q.value.trim()) {
    posts.value = []
    total.value = 0
    return
  }
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
    <header class="mb-8">
      <h1 class="font-serif text-3xl font-bold text-ed-fg mb-4">搜索</h1>
      <form @submit.prevent="doSearch" class="flex items-center gap-3">
        <input v-model="q" type="text" placeholder="输入关键词..." class="ed-input flex-1 text-base" />
        <button type="submit" class="ed-btn-primary">搜索 →</button>
      </form>
    </header>

    <div v-if="q && !loading" class="mb-6 text-sm text-ed-muted">
      "<span class="text-ed-fg font-medium">{{ q }}</span>" 的搜索结果，共 <span class="text-ed-accent font-medium">{{ total }}</span> 篇
    </div>

    <div v-if="loading" class="text-center py-16 text-ed-muted text-sm" style="min-height: calc(100vh - 56px);">搜索中...</div>
    <div v-else-if="posts.length === 0 && q" class="text-center py-16 text-ed-muted text-sm">未找到相关文章</div>
    <div v-else>
      <PostCard v-for="(post, i) in posts" :key="post.id" :post="post" :index="i + 1" />
    </div>
  </div>
</template>
