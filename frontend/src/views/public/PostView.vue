<script setup>
import { ref, onMounted, onUnmounted, watch, computed, inject, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { marked, Renderer } from 'marked'
import hljs from 'highlight.js/lib/core'
import javascript from 'highlight.js/lib/languages/javascript'
import typescript from 'highlight.js/lib/languages/typescript'
import python from 'highlight.js/lib/languages/python'
import bash from 'highlight.js/lib/languages/bash'
import css from 'highlight.js/lib/languages/css'
import xml from 'highlight.js/lib/languages/xml'
import json from 'highlight.js/lib/languages/json'
import sql from 'highlight.js/lib/languages/sql'
import go from 'highlight.js/lib/languages/go'
import rust from 'highlight.js/lib/languages/rust'
import java from 'highlight.js/lib/languages/java'
import cpp from 'highlight.js/lib/languages/cpp'
import yaml from 'highlight.js/lib/languages/yaml'
import markdown from 'highlight.js/lib/languages/markdown'

hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('js', javascript)
hljs.registerLanguage('typescript', typescript)
hljs.registerLanguage('ts', typescript)
hljs.registerLanguage('python', python)
hljs.registerLanguage('py', python)
hljs.registerLanguage('bash', bash)
hljs.registerLanguage('sh', bash)
hljs.registerLanguage('shell', bash)
hljs.registerLanguage('css', css)
hljs.registerLanguage('html', xml)
hljs.registerLanguage('xml', xml)
hljs.registerLanguage('json', json)
hljs.registerLanguage('sql', sql)
hljs.registerLanguage('go', go)
hljs.registerLanguage('rust', rust)
hljs.registerLanguage('java', java)
hljs.registerLanguage('cpp', cpp)
hljs.registerLanguage('c', cpp)
hljs.registerLanguage('yaml', yaml)
hljs.registerLanguage('yml', yaml)
hljs.registerLanguage('markdown', markdown)
hljs.registerLanguage('md', markdown)
import { getPost } from '../../api/posts'
import { getComments, createComment } from '../../api/comments'
import HudPanel from '../../components/public/HudPanel.vue'
import PostToc from '../../components/public/PostToc.vue'

const renderer = new Renderer()
renderer.code = ({ text, lang }) => {
  const language = hljs.getLanguage(lang) ? lang : null
  const highlighted = language
    ? hljs.highlight(text, { language }).value
    : hljs.highlightAuto(text).value
  const cls = language ?? 'plaintext'
  return `<pre><code class="hljs language-${cls}">${highlighted}</code></pre>`
}
marked.use({ renderer })

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
  document.querySelectorAll('.prose-ed h2[id], .prose-ed h3[id]').forEach((el) => {
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
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
})

function commentDate(c) {
  const d = new Date(c.created_at)
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

onMounted(load)
onUnmounted(() => {
  observer?.disconnect()
})
watch(() => route.params.slug, load)
</script>

<template>
  <div>
    <div v-if="loading" class="text-center py-20 text-ed-muted text-sm" style="min-height: calc(100vh - 56px);">加载中...</div>

    <article v-else-if="post">
      <header class="mb-10">
        <div class="flex items-center gap-3 mb-4 font-mono text-[13px] text-ed-muted uppercase tracking-wider">
          <span v-if="post.category" class="ed-tag">{{ post.category.name }}</span>
          <span>{{ dateStr }}</span>
          <span>·</span>
          <span>{{ post.views }} 次阅读</span>
        </div>
        <h1 class="font-serif text-3xl md:text-4xl lg:text-5xl font-bold text-ed-fg leading-tight mb-4" style="letter-spacing: -0.02em;">
          {{ post.title }}
        </h1>
        <p v-if="post.summary" class="text-lg text-ed-muted leading-relaxed mb-6">{{ post.summary }}</p>
        <div v-if="post.tags?.length" class="flex items-center gap-2 flex-wrap pt-4 border-t border-ed-border">
          <router-link v-for="tag in post.tags" :key="tag.id" :to="`/tag/${tag.slug}`" class="ed-tag">
            {{ tag.name }}
          </router-link>
        </div>
      </header>

      <img v-if="post.cover_image" :src="post.cover_image" :alt="post.title"
        class="w-full h-64 md:h-80 object-cover rounded-2xl mb-10 border border-ed-border" />

      <div class="prose-ed" v-html="renderedHtml" />

      <Teleport v-if="post && tocItems.length && tocVisible" to="#toc-mount">
        <PostToc :items="tocItems" :active-id="activeId" />
      </Teleport>

      <section class="mt-16 pt-10 border-t border-ed-border">
        <h2 class="font-serif text-2xl font-bold text-ed-fg mb-6">评论 <span class="font-mono text-base text-ed-muted font-normal">({{ comments.length }})</span></h2>

        <div v-if="comments.length" class="space-y-4 mb-8">
          <div v-for="c in comments" :key="c.id" class="ed-panel">
            <div class="flex items-center justify-between mb-2">
              <span class="font-semibold text-ed-fg text-sm">{{ c.author_name }}</span>
              <span class="font-mono text-[12px] text-ed-muted">{{ commentDate(c) }}</span>
            </div>
            <p class="text-sm text-ed-fg leading-relaxed whitespace-pre-line">{{ c.content }}</p>
          </div>
        </div>
        <div v-else class="text-ed-muted text-sm mb-8">暂无评论，来说第一句话吧。</div>

        <div v-if="submitted" class="ed-panel border-ed-accent/30 text-ed-accent text-sm mb-4">
          ✓ 评论已提交，等待审核后显示。
        </div>

        <form v-else @submit.prevent="submitComment" class="ed-panel space-y-4">
          <h3 class="font-serif text-lg font-semibold text-ed-fg">留下评论</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="flex flex-col gap-1">
              <label class="font-mono text-[13px] uppercase tracking-wider text-ed-muted">姓名</label>
              <input v-model="commentForm.author_name" required placeholder="你的名字" class="ed-input" />
            </div>
            <div class="flex flex-col gap-1">
              <label class="font-mono text-[13px] uppercase tracking-wider text-ed-muted">邮箱</label>
              <input v-model="commentForm.author_email" required type="email" placeholder="不会公开" class="ed-input" />
            </div>
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-mono text-[13px] uppercase tracking-wider text-ed-muted">内容</label>
            <textarea v-model="commentForm.content" required placeholder="写下你的想法..." rows="4"
              class="ed-input resize-none" />
          </div>
          <div class="flex justify-end">
            <button type="submit" :disabled="submitting" class="ed-btn-primary">
              {{ submitting ? '提交中...' : '提交评论 →' }}
            </button>
          </div>
        </form>
      </section>
    </article>
  </div>
</template>
