<script setup>
import { ref, onMounted, onUnmounted, computed, provide, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getTags } from '../../api/tags'
import { getCategories } from '../../api/categories'
import { getPosts } from '../../api/posts'

const router = useRouter()
const route = useRoute()
const tags = ref([])
const categories = ref([])
const totalPosts = ref(0)
const searchQ = ref('')

const isArticle = computed(() => route.path.startsWith('/posts/'))
const tocVisible = ref(true)
provide('tocVisible', tocVisible)
provide('tags', tags)
provide('categories', categories)
provide('totalPosts', totalPosts)

const containerClass = 'mx-auto px-10 max-w-[1200px]'
const contentClass = computed(() =>
  isArticle.value ? 'mx-auto px-6 max-w-[1440px]' : 'mx-auto px-10 max-w-[1200px]'
)

const tagCloud = computed(() => {
  if (!tags.value.length) return []
  const counts = tags.value.map(t => t.post_count ?? 0)
  const maxC = Math.max(...counts, 1)
  const minC = Math.min(...counts, 0)
  return tags.value.map(t => {
    const c = t.post_count ?? 0
    const ratio = maxC > minC
      ? (Math.log(c + 1) - Math.log(minC + 1)) / (Math.log(maxC + 1) - Math.log(minC + 1))
      : 0
    const size = 11 + ratio * 14
    const r = Math.round(232 * ratio + 138 * (1 - ratio))
    const g = Math.round(93 * ratio + 130 * (1 - ratio))
    const b = Math.round(58 * ratio + 120 * (1 - ratio))
    const alpha = 0.5 + ratio * 0.5
    return { ...t, size, color: `rgba(${r},${g},${b},${alpha})` }
  })
})

const gridInner = computed(() => {
  if (isArticle.value) {
    return 'py-8 md:py-10 grid gap-8 grid-cols-1 xl:grid-cols-[220px_minmax(0,1fr)_260px]'
  }
  return 'pb-8 md:pb-10'
})

function onMouseMove(e) {
  document.documentElement.style.setProperty('--cursor-x', e.clientX + 'px')
  document.documentElement.style.setProperty('--cursor-y', e.clientY + 'px')
}

let revealObserver = null

onMounted(async () => {
  window.addEventListener('mousemove', onMouseMove)
  const [tgs, cats, postData] = await Promise.all([
    getTags(),
    getCategories(),
    getPosts({ page: 1, page_size: 1 }),
  ])
  tags.value = tgs
  categories.value = cats
  totalPosts.value = postData.total || 0
  revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible')
        revealObserver.unobserve(e.target)
      }
    })
  }, { threshold: 0.1 })
  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el))
})

watch(route, async () => {
  await nextTick()
  document.querySelectorAll('.reveal:not(.visible)').forEach(el => revealObserver?.observe(el))
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
  if (revealObserver) revealObserver.disconnect()
})

function doSearch() {
  if (searchQ.value.trim()) {
    router.push({ path: '/search', query: { q: searchQ.value.trim() } })
  }
}
</script>

<template>
  <div class="min-h-screen bg-ed-bg flex flex-col">
    <div class="cursor-glow" />

    <!-- Nav -->
    <nav class="sticky top-0 z-20 border-b border-ed-border"
         style="background: rgba(249,248,246,0.88); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);">
      <div :class="containerClass" class="h-14 flex items-center gap-8">
        <router-link to="/" class="font-serif text-lg font-bold text-ed-fg no-underline mr-auto shrink-0">
          生如夏花<span style="background: linear-gradient(135deg, rgb(var(--ed-accent)), rgb(var(--ed-accent2))); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">.</span>
        </router-link>
        <div class="hidden md:flex items-center gap-6">
          <router-link to="/" class="text-sm text-ed-muted hover:text-ed-fg transition-colors no-underline">文章</router-link>
          <router-link to="/about" class="text-sm text-ed-muted hover:text-ed-fg transition-colors no-underline">关于</router-link>
        </div>
        <form @submit.prevent="doSearch" class="flex items-center gap-2">
          <input v-model="searchQ" type="text" placeholder="搜索..." class="ed-input w-36 text-sm" />
        </form>
      </div>
    </nav>

    <!-- Main content -->
    <div class="flex-1" :class="isArticle ? contentClass : containerClass">
      <div :class="gridInner">
        <aside v-if="isArticle" class="hidden xl:block self-start sticky top-20">
          <div v-show="tocVisible" id="toc-mount" />
          <button v-show="!tocVisible" type="button"
            class="ed-tag flex items-center gap-1.5 bg-ed-surface w-full justify-center"
            @click="tocVisible = true">
            目录 ▶
          </button>
        </aside>

        <main class="min-w-0">
          <RouterView />
        </main>

        <!-- Right sidebar: categories + tag heatmap (article pages only) -->
        <aside v-if="isArticle" class="hidden xl:block self-start sticky top-20 space-y-4">
          <!-- Categories -->
          <div v-if="categories.length" class="ed-panel">
            <div class="ed-panel-title">分类</div>
            <ul class="space-y-1">
              <li v-for="cat in categories" :key="cat.id">
                <router-link
                  :to="`/category/${cat.slug}`"
                  class="flex items-center justify-between py-1.5 px-2 rounded-lg text-sm transition-colors no-underline"
                  :class="$route.params.slug === cat.slug && $route.path.startsWith('/category')
                    ? 'text-ed-accent bg-ed-accent/8'
                    : 'text-ed-muted hover:text-ed-fg hover:bg-ed-surface2'"
                >
                  <span>{{ cat.name }}</span>
                  <span class="font-mono text-[12px] opacity-60">{{ cat.post_count ?? 0 }}</span>
                </router-link>
              </li>
            </ul>
          </div>

          <!-- Tag heatmap -->
          <div v-if="tagCloud.length" class="ed-panel">
            <div class="ed-panel-title">标签热度</div>
            <div style="display:flex;flex-wrap:wrap;gap:6px 8px;align-items:baseline;line-height:1.4;">
              <router-link
                v-for="tag in tagCloud" :key="tag.id"
                :to="`/tag/${tag.slug}`"
                class="no-underline transition-opacity hover:opacity-80"
                :style="{ fontSize: tag.size + 'px', color: tag.color }"
                :title="`${tag.name} · ${tag.post_count ?? 0} 篇`"
              >{{ tag.name }}</router-link>
            </div>
          </div>
        </aside>
      </div>
    </div>

    <!-- Wave divider -->
    <div style="line-height:0; overflow:hidden;">
      <svg viewBox="0 0 1440 60" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" style="display:block;width:100%;">
        <path d="M0,30 C240,60 480,0 720,30 C960,60 1200,0 1440,30 L1440,60 L0,60 Z" fill="rgb(235,230,222)"/>
      </svg>
    </div>

    <!-- Footer -->
    <footer style="background: rgb(235,230,222); border-top: 1px solid rgb(var(--ed-border));" class="py-12">
      <div :class="containerClass" class="flex items-start justify-between flex-wrap gap-8">
        <div class="flex flex-col gap-2">
          <div class="font-serif text-xl font-bold" style="color: rgb(var(--ed-fg));">
            生如夏花<span style="background: linear-gradient(135deg, rgb(var(--ed-accent)), rgb(var(--ed-accent2))); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">.</span>
          </div>
          <div class="text-sm max-w-xs" style="color: rgb(var(--ed-muted));">写代码、写文字、写生活。<br>记录技术探索与内心流动。</div>
          <div class="font-mono text-[10px]" style="color: rgb(var(--ed-muted)); opacity: 0.6;">© {{ new Date().getFullYear() }}</div>
        </div>
        <div class="flex gap-3 flex-wrap items-center">
          <router-link to="/" class="font-mono text-[11px] uppercase tracking-wider no-underline px-3 py-1.5 rounded-full border transition-colors"
            style="color: rgb(var(--ed-muted)); border-color: rgb(var(--ed-border));"
            @mouseover="$event.target.style.color='rgb(var(--ed-fg))'; $event.target.style.borderColor='rgb(var(--ed-fg))'"
            @mouseleave="$event.target.style.color='rgb(var(--ed-muted))'; $event.target.style.borderColor='rgb(var(--ed-border))'">
            文章
          </router-link>
          <router-link to="/about" class="font-mono text-[11px] uppercase tracking-wider no-underline px-3 py-1.5 rounded-full border transition-colors"
            style="color: rgb(var(--ed-muted)); border-color: rgb(var(--ed-border));"
            @mouseover="$event.target.style.color='rgb(var(--ed-fg))'; $event.target.style.borderColor='rgb(var(--ed-fg))'"
            @mouseleave="$event.target.style.color='rgb(var(--ed-muted))'; $event.target.style.borderColor='rgb(var(--ed-border))'">
            关于
          </router-link>
        </div>
      </div>
    </footer>
  </div>
</template>
