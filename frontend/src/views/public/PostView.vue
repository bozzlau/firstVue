<script setup>
import { ref, onMounted, onUnmounted, watch, computed, inject, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import { getPost } from '../../api/posts'
import { getComments, createComment } from '../../api/comments'
import HudPanel from '../../components/public/HudPanel.vue'
import PostToc from '../../components/public/PostToc.vue'

const route = useRoute()
const post = ref(null)
const comments = ref([])
const loading = ref(true)
const commentForm = ref({ author_name: '', author_email: '', content: '' })
const submitting = ref(false)
const submitted = ref(false)

const tocVisible = inject('tocVisible', ref(true))
const activeId = ref(null)

const tocItems = computed(() => {
  if (!post.value?.content) return []
  const tokens = marked.lexer(post.value.content)
  const items = []
  let i = 0
  for (const t of tokens) {
    if (t.type === 'heading' && (t.depth === 2 || t.depth === 3)) {
      items.push({ id: `heading-${i}`, text: t.text, depth: t.depth })
      i++
    }
  }
  return items
})

const renderedHtml = computed(() => {
  if (!post.value?.content) return ''
  let i = 0
  return marked(post.value.content).replace(
    /<(h[23])>/g,
    (_, tag) => `<${tag} id="heading-${i++}">`,
  )
})

let observer = null
const visibleIds = new Set()

function setupObserver() {
  observer?.disconnect()
  visibleIds.clear()
  if (!tocItems.value.length) return
  observer = new IntersectionObserver(
    (entries) => {
      for (const e of entries) {
        if (e.isIntersecting) visibleIds.add(e.target.id)
        else visibleIds.delete(e.target.id)
      }
      if (visibleIds.size > 0) {
        const order = tocItems.value.map((t) => t.id)
        let topmost = null
        let topmostIdx = Infinity
        for (const id of visibleIds) {
          const idx = order.indexOf(id)
          if (idx >= 0 && idx < topmostIdx) {
            topmostIdx = idx
            topmost = id
          }
        }
        if (topmost) activeId.value = topmost
      }
    },
    { rootMargin: '-80px 0px -70% 0px', threshold: 0 },
  )
  document.querySelectorAll('.prose-hud h2[id], .prose-hud h3[id]').forEach((el) => {
    observer.observe(el)
  })
}

async function load() {
  loading.value = true
  submitted.value = false
  observer?.disconnect()
  activeId.value = null
  try {
    const [p, c] = await Promise.all([
      getPost(route.params.slug),
      getComments(route.params.slug),
    ])
    post.value = p
    comments.value = c
  } finally {
    loading.value = false
  }
  await nextTick()
  setupObserver()
}

async function submitComment() {
  submitting.value = true
  try {
    await createComment(route.params.slug, commentForm.value)
    commentForm.value = { author_name: '', author_email: '', content: '' }
    submitted.value = true
  } finally {
    submitting.value = false
  }
}

const code = computed(() => post.value ? String(post.value.id).padStart(3, '0') : '000')
const dateStr = computed(() => {
  if (!post.value) return ''
  const d = new Date(post.value.created_at)
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}.${pad(d.getMonth() + 1)}.${pad(d.getDate())}`
})

function commentDate(c) {
  const d = new Date(c.created_at)
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}.${pad(d.getMonth() + 1)}.${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

onMounted(load)
onUnmounted(() => {
  observer?.disconnect()
})
watch(() => route.params.slug, load)
</script>

<template>
  <div>
    <div v-if="loading" class="text-center py-16 font-mono text-xs uppercase tracking-widest text-hud-textDim">
      [ FETCHING ▮▮▮ ]
    </div>

    <article v-else-if="post">
      <header class="hud-frame mb-8">
        <div class="flex items-center justify-between h-7 px-4 border-b border-hud-borderDim bg-hud-amber/5">
          <div class="flex items-center gap-3 font-mono text-[11px] uppercase tracking-wider">
            <span class="text-hud-amber">[POST_{{ code }}]</span>
            <span class="text-hud-textMuted">·</span>
            <span class="text-hud-textDim">◆ {{ dateStr }}</span>
            <span class="text-hud-textMuted">·</span>
            <span class="text-hud-textDim">▸ {{ post.views }} VIEWS</span>
          </div>
          <span
            v-if="post.category"
            class="font-mono text-[10px] uppercase tracking-wider text-hud-amber border border-hud-amberDim/60 px-1.5 py-0.5"
          >
            {{ post.category.name }}
          </span>
        </div>

        <div class="p-6">
          <h1 class="font-display text-3xl md:text-4xl font-bold text-hud-amberSoft leading-tight mb-3">
            {{ post.title }}
          </h1>
          <p v-if="post.summary" class="text-sm text-hud-textDim mb-4 leading-relaxed">
            {{ post.summary }}
          </p>
          <div v-if="post.tags?.length" class="flex items-center gap-2 flex-wrap pt-3 border-t border-hud-borderDim">
            <span class="font-mono text-[10px] uppercase tracking-widest text-hud-textMuted">// TAGS</span>
            <router-link
              v-for="tag in post.tags"
              :key="tag.id"
              :to="`/tag/${tag.slug}`"
              class="hud-tag"
            >
              {{ tag.name }}
            </router-link>
          </div>
        </div>
      </header>

      <img
        v-if="post.cover_image"
        :src="post.cover_image"
        :alt="post.title"
        class="w-full h-64 object-cover border border-hud-borderDim mb-8"
      />

      <div
        class="prose-hud"
        v-html="renderedHtml"
      />

      <Teleport v-if="post && tocItems.length && tocVisible" to="#toc-mount">
        <PostToc :items="tocItems" :active-id="activeId" />
      </Teleport>

      <section class="mt-16">
        <HudPanel
          :label="`// TRANSMISSIONS`"
          :status="`${String(comments.length).padStart(2, '0')} RECEIVED`"
        >
          <div v-if="comments.length === 0" class="font-mono text-xs uppercase tracking-widest text-hud-textMuted py-4 text-center">
            // NO_TRANSMISSIONS
          </div>
          <div v-else class="space-y-3 mb-2">
            <div
              v-for="c in comments"
              :key="c.id"
              class="relative border border-hud-borderDim bg-hud-bg/40 p-3 group"
            >
              <span class="hud-glow-bar" />
              <div class="flex items-center justify-between mb-1.5 font-mono text-[10px] uppercase tracking-wider">
                <span class="text-hud-amber">[USER] {{ c.author_name }}</span>
                <span class="text-hud-textMuted">{{ commentDate(c) }}</span>
              </div>
              <p class="text-sm text-hud-text leading-relaxed whitespace-pre-line">{{ c.content }}</p>
            </div>
          </div>
        </HudPanel>

        <div v-if="submitted" class="mt-4 hud-frame border-hud-amber/60 p-3 font-mono text-xs uppercase tracking-wider text-hud-amber">
          ✓ TRANSMISSION_QUEUED // PENDING REVIEW
        </div>

        <form v-else @submit.prevent="submitComment" class="mt-4">
          <HudPanel label="// COMPOSE_TRANSMISSION">
            <div class="space-y-3">
              <div class="grid grid-cols-2 gap-3">
                <div class="flex items-center gap-2">
                  <span class="font-mono text-[10px] uppercase text-hud-textMuted shrink-0">▸ NAME</span>
                  <input
                    v-model="commentForm.author_name"
                    required
                    placeholder="callsign"
                    class="hud-input flex-1"
                  />
                </div>
                <div class="flex items-center gap-2">
                  <span class="font-mono text-[10px] uppercase text-hud-textMuted shrink-0">▸ MAIL</span>
                  <input
                    v-model="commentForm.author_email"
                    required
                    type="email"
                    placeholder="not_public@host"
                    class="hud-input flex-1"
                  />
                </div>
              </div>
              <div>
                <div class="font-mono text-[10px] uppercase text-hud-textMuted mb-1">▸ MESSAGE</div>
                <textarea
                  v-model="commentForm.content"
                  required
                  placeholder="type your transmission ____"
                  rows="4"
                  class="w-full bg-hud-bg/40 border border-hud-borderDim text-hud-text font-sans text-sm
                         px-3 py-2 outline-none transition-colors duration-200 resize-none
                         placeholder:text-hud-textMuted focus:border-hud-amber"
                />
              </div>
              <div class="flex items-center justify-between">
                <span class="font-mono text-[10px] uppercase text-hud-textMuted">
                  <span class="text-hud-amber animate-hud-blink">▮</span>
                  STATUS: {{ submitting ? 'TRANSMITTING' : 'READY' }}
                </span>
                <button
                  type="submit"
                  :disabled="submitting"
                  class="hud-btn"
                >
                  {{ submitting ? '[ SENDING... ]' : '[ TRANSMIT ▸ ]' }}
                </button>
              </div>
            </div>
          </HudPanel>
        </form>
      </section>
    </article>
  </div>
</template>
