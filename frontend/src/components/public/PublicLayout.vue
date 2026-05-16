<script setup>
import { ref, onMounted, onUnmounted, computed, provide } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getCategories } from '../../api/categories'
import { getTags } from '../../api/tags'
import { getPosts } from '../../api/posts'
import HudPanel from './HudPanel.vue'
import StatusDot from './StatusDot.vue'
import ThemeSwitcher from './ThemeSwitcher.vue'

const router = useRouter()
const route = useRoute()
const categories = ref([])
const tags = ref([])
const totalPosts = ref(0)
const searchQ = ref('')
const now = ref(new Date())

const isArticle = computed(() => route.path.startsWith('/posts/'))
const tocVisible = ref(true)
provide('tocVisible', tocVisible)

const containerClass = computed(() =>
  isArticle.value && tocVisible.value
    ? 'mx-auto px-4 md:px-6 max-w-6xl xl:w-[90%] xl:max-w-[1600px]'
    : 'mx-auto px-4 md:px-6 max-w-6xl',
)

const gridInner = computed(() =>
  isArticle.value && tocVisible.value
    ? 'py-8 md:py-10 grid gap-8 grid-cols-1 lg:grid-cols-[minmax(0,1fr)_240px] xl:grid-cols-[200px_minmax(0,1fr)_240px]'
    : 'py-8 md:py-10 grid gap-8 grid-cols-1 lg:grid-cols-[minmax(0,1fr)_240px]',
)

const clock = computed(() => {
  const d = now.value
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}.${pad(d.getMonth() + 1)}.${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
})

let timer = null

onMounted(async () => {
  timer = setInterval(() => { now.value = new Date() }, 1000)
  const [cats, tgs, postData] = await Promise.all([
    getCategories(),
    getTags(),
    getPosts({ page: 1, page_size: 1 }),
  ])
  categories.value = cats
  tags.value = tgs
  totalPosts.value = postData.total || 0
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

function doSearch() {
  if (searchQ.value.trim()) {
    router.push({ path: '/search', query: { q: searchQ.value.trim() } })
  }
}
</script>

<template>
  <div class="hud-grid-bg min-h-screen text-hud-text">
    <nav class="sticky top-0 z-20 backdrop-blur bg-hud-bg/85 border-b border-hud-border">
      <div :class="containerClass" class="h-12 flex items-center gap-6">
        <router-link to="/" class="flex items-center gap-2 no-underline shrink-0">
          <span class="font-mono text-hud-amber tracking-widest">▮▮▮</span>
          <span class="font-display font-bold tracking-wider text-hud-text text-sm">BLOG.SYS</span>
          <span class="font-mono text-[10px] text-hud-textMuted">v1.0</span>
        </router-link>

        <div class="hidden md:flex items-center gap-5 text-xs">
          <StatusDot label="ONLINE" />
          <span class="font-mono uppercase tracking-wider text-hud-textDim">
            <span class="text-hud-amber">{{ String(totalPosts).padStart(3, '0') }}</span> POSTS
          </span>
          <span class="font-mono uppercase tracking-wider text-hud-textMuted">{{ clock }}</span>
        </div>

        <div class="flex-1" />

        <form @submit.prevent="doSearch" class="flex items-center gap-2 group">
          <span class="font-mono text-hud-amber text-lg leading-none">⌕</span>
          <input
            v-model="searchQ"
            type="text"
            placeholder="search ____"
            class="hud-input w-44"
          />
        </form>

        <ThemeSwitcher />

        <router-link
          to="/about"
          class="hud-tag no-underline"
          :class="route.path === '/about' ? 'border-hud-amber text-hud-amber' : ''"
        >
          /ABOUT
        </router-link>
      </div>
    </nav>

    <button
      v-if="isArticle && !tocVisible"
      type="button"
      class="hidden xl:flex fixed left-4 top-20 z-30 hud-tag bg-hud-surface items-center gap-1.5"
      @click="tocVisible = true"
    >
      <span class="text-hud-amber">◀</span>
      <span>TOC</span>
    </button>

    <div :class="containerClass">
      <div :class="gridInner">
        <aside
          v-if="isArticle && tocVisible"
          class="hidden xl:block self-start sticky top-20"
        >
          <div id="toc-mount" />
        </aside>

        <main class="min-w-0">
          <RouterView />
        </main>

        <aside class="hidden lg:block space-y-5 self-start sticky top-20">
          <HudPanel
            v-if="categories.length"
            label="// CATEGORY"
            :status="`${String(categories.length).padStart(2, '0')} ITEMS`"
            no-pad
          >
            <ul class="divide-y divide-hud-borderDim">
              <li v-for="(cat, i) in categories" :key="cat.id">
                <router-link
                  :to="`/category/${cat.slug}`"
                  class="flex items-center justify-between px-3 py-2 no-underline transition-colors hover:bg-hud-amber/5 group"
                  :class="route.params.slug === cat.slug && route.path.startsWith('/category') ? 'bg-hud-amber/10' : ''"
                >
                  <span class="flex items-center gap-2 min-w-0">
                    <span class="font-mono text-[11px] text-hud-textMuted">{{ String(i + 1).padStart(2, '0') }}</span>
                    <span
                      class="text-base truncate"
                      :class="route.params.slug === cat.slug && route.path.startsWith('/category')
                        ? 'text-hud-amber'
                        : 'text-hud-text group-hover:text-hud-amberSoft'"
                    >{{ cat.name }}</span>
                  </span>
                  <span class="font-mono text-[11px] text-hud-textMuted group-hover:text-hud-amber">▸</span>
                </router-link>
              </li>
            </ul>
          </HudPanel>

          <HudPanel
            v-if="tags.length"
            label="// TAGS"
            :status="`${String(tags.length).padStart(2, '0')} TAGS`"
          >
            <div class="flex flex-wrap gap-1.5">
              <router-link
                v-for="tag in tags"
                :key="tag.id"
                :to="`/tag/${tag.slug}`"
                class="hud-tag text-xs"
                :class="route.params.slug === tag.slug && route.path.startsWith('/tag') ? 'border-hud-amber text-hud-amber bg-hud-amber/10' : ''"
              >
                {{ tag.name }}
              </router-link>
            </div>
          </HudPanel>

          <div class="font-mono text-[11px] text-hud-textMuted leading-relaxed px-1">
            <div>SYS // BLOG.SYS v1.0</div>
            <div>UPLINK // <span class="text-hud-amber">STABLE</span></div>
            <div>SECURE // <span class="text-hud-amber">[OK]</span></div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>
