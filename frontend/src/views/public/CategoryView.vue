<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getPosts } from '../../api/posts'
import PostCard from '../../components/public/PostCard.vue'

const route = useRoute()
const posts = ref([])
const total = ref(0)
const loading = ref(false)

async function load() {
  loading.value = true
  try {
    const data = await getPosts({ category: route.params.slug, page: 1, page_size: 20 })
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
    <div class="hud-frame mb-6">
      <div class="flex items-center justify-between gap-3 h-9 px-4 border-b border-hud-borderDim bg-hud-amber/5">
        <div class="flex items-center gap-3 font-mono text-[11px] uppercase tracking-[0.18em]">
          <span class="text-hud-amber">▶ FILTER</span>
          <span class="text-hud-textMuted">·</span>
          <span class="text-hud-textDim">CATEGORY</span>
          <span class="text-hud-textMuted">·</span>
          <span class="text-hud-amberSoft">{{ route.params.slug }}</span>
        </div>
        <span class="font-mono text-[11px] uppercase tracking-wider text-hud-textDim">
          <span class="text-hud-amber">{{ String(total).padStart(3, '0') }}</span> ENTRIES
        </span>
      </div>
    </div>

    <div v-if="loading" class="text-center py-16 font-mono text-xs uppercase tracking-widest text-hud-textDim">
      [ LOADING ▮▮▮ ]
    </div>
    <div v-else-if="posts.length === 0" class="text-center py-16 font-mono text-xs uppercase tracking-widest text-hud-textMuted">
      // NO_DATA · CATEGORY_EMPTY
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
