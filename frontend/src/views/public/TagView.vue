<script setup>
import { ref, onMounted, watch, computed, inject } from 'vue'
import { useRoute } from 'vue-router'
import { getPosts } from '../../api/posts'
import PostCard from '../../components/public/PostCard.vue'

const route = useRoute()
const posts = ref([])
const total = ref(0)
const loading = ref(false)
const tags = inject('tags', ref([]))

const tagName = computed(() => {
  const tag = tags.value.find(t => t.slug === route.params.slug)
  return tag?.name || route.params.slug
})

async function load() {
  loading.value = true
  try {
    const data = await getPosts({ tag: route.params.slug, page: 1, page_size: 20 })
    posts.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => route.params.slug, load)
</script>

<template>
  <div>
    <header class="mb-10 pt-4">
      <div class="ed-sec-title mb-5">标签</div>
      <div class="flex items-baseline gap-4 flex-wrap">
        <h1 class="font-serif font-bold text-ed-fg"
          style="font-size: clamp(36px, 5vw, 56px); line-height: 1.1; letter-spacing: -0.02em;">
          # {{ tagName }}
        </h1>
        <span class="font-mono text-sm text-ed-muted">共 {{ total }} 篇</span>
      </div>
    </header>

    <div v-if="loading" class="text-center py-16 text-ed-muted text-sm" style="min-height: calc(100vh - 56px);">加载中...</div>
    <div v-else-if="posts.length === 0" class="text-center py-16 text-ed-muted text-sm">该标签下暂无文章</div>
    <div v-else>
      <PostCard v-for="(post, i) in posts" :key="post.id" :post="post" :index="i + 1" />
    </div>
  </div>
</template>
