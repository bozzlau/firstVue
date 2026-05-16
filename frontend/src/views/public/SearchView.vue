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
    <section class="hud-frame mb-5">
      <div class="flex items-center justify-between h-7 px-3 border-b border-hud-borderDim bg-hud-amber/5">
        <span class="font-mono text-[11px] uppercase tracking-[0.2em] text-hud-amber">// QUERY</span>
        <span class="font-mono text-[10px] text-hud-textMuted">[ TYPE TO SEARCH ]</span>
      </div>
      <form @submit.prevent="doSearch" class="flex items-center gap-3 p-4">
        <span class="font-mono text-hud-amber text-base">▸</span>
        <input
          v-model="q"
          type="text"
          placeholder="search keywords ____"
          class="hud-input flex-1 text-base"
        />
        <button type="submit" class="hud-btn">[ EXEC ]</button>
      </form>
    </section>

    <p v-if="q && !loading" class="font-mono text-[11px] uppercase tracking-wider text-hud-textDim mb-4">
      <span class="text-hud-amber">▸ RESULT</span>
      <span class="mx-2 text-hud-textMuted">·</span>
      <span class="text-hud-amberSoft">"{{ q }}"</span>
      <span class="mx-2 text-hud-textMuted">·</span>
      <span class="text-hud-amber">{{ String(total).padStart(3, '0') }}</span> HITS
    </p>

    <div v-if="loading" class="text-center py-16 font-mono text-xs uppercase tracking-widest text-hud-textDim">
      [ SCANNING ▮▮▮ ]
    </div>
    <div v-else-if="posts.length === 0 && q" class="text-center py-16 font-mono text-xs uppercase tracking-widest text-hud-textMuted">
      // NO_MATCH
    </div>
    <div v-else class="space-y-3">
      <PostCard
        v-for="(post, i) in posts"
        :key="post.id"
        :post="post"
        :index="i + 1"
      />
    </div>
  </div>
</template>
