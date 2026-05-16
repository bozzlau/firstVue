<script setup>
import { ref, onMounted, computed } from 'vue'
import { getPosts } from '../../api/posts'
import PostCard from '../../components/public/PostCard.vue'

const posts = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const loading = ref(false)

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

async function load() {
  loading.value = true
  try {
    const data = await getPosts({ page: page.value, page_size: pageSize })
    posts.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

onMounted(load)

function go(delta) {
  const next = page.value + delta
  if (next < 1 || next > totalPages.value) return
  page.value = next
  load()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<template>
  <div>
    <div class="flex items-end justify-between mb-5 pb-2 border-b border-hud-borderDim">
      <div class="flex items-center gap-3">
        <span class="hud-section-label">// LATEST_FEED</span>
        <span class="font-mono text-[10px] text-hud-textMuted">▮▮▮▮▮</span>
      </div>
      <span class="font-mono text-[11px] uppercase tracking-wider text-hud-textDim">
        <span class="text-hud-amber">{{ String(total).padStart(3, '0') }}</span> ENTRIES
      </span>
    </div>

    <div v-if="loading" class="flex items-center justify-center gap-2 py-16 font-mono text-xs uppercase tracking-widest text-hud-textDim">
      <span class="inline-block w-2 h-2 bg-hud-amber animate-hud-pulse" />
      <span class="inline-block w-2 h-2 bg-hud-amber animate-hud-pulse" style="animation-delay:0.2s" />
      <span class="inline-block w-2 h-2 bg-hud-amber animate-hud-pulse" style="animation-delay:0.4s" />
      <span class="ml-3">LOADING</span>
    </div>

    <div v-else-if="posts.length === 0" class="text-center py-16 font-mono text-xs uppercase tracking-widest text-hud-textMuted">
      // NO_DATA
    </div>

    <div v-else class="space-y-3">
      <PostCard
        v-for="(post, i) in posts"
        :key="post.id"
        :post="post"
        :index="(page - 1) * pageSize + i + 1"
      />
    </div>

    <div v-if="!loading && total > pageSize" class="mt-8 flex items-center justify-center gap-4">
      <button class="hud-btn" :disabled="page === 1" @click="go(-1)">◀ PREV</button>
      <span class="font-mono text-xs uppercase tracking-widest text-hud-textDim">
        <span class="text-hud-amber">{{ String(page).padStart(2, '0') }}</span>
        <span class="mx-2 text-hud-textMuted">/</span>
        <span>{{ String(totalPages).padStart(2, '0') }}</span>
      </span>
      <button class="hud-btn" :disabled="page >= totalPages" @click="go(1)">NEXT ▶</button>
    </div>
  </div>
</template>
