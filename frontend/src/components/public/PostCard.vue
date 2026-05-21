<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  post: { type: Object, required: true },
  index: { type: Number, default: null },
})

const router = useRouter()

const dateStr = computed(() => {
  const d = new Date(props.post.created_at)
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
})
</script>

<template>
  <article class="article-row" @click="router.push(`/posts/${post.slug}`)">
    <div class="article-row-tag">{{ post.tags?.[0]?.name || post.category?.name || '' }}</div>
    <div class="article-row-body">
      <div class="article-row-title">{{ post.title }}</div>
      <div v-if="post.summary" class="article-row-excerpt">{{ post.summary }}</div>
    </div>
    <div class="article-row-meta">
      <span>{{ dateStr }}</span>
    </div>
  </article>
</template>

<style scoped>
.article-row {
  display: grid;
  grid-template-columns: 80px 1fr auto;
  gap: 0 20px;
  align-items: baseline;
  padding: 22px 0;
  border-bottom: 1px solid rgb(var(--ed-border));
  cursor: pointer;
  transition: all 0.18s;
  position: relative;
}
.article-row::before {
  content: '';
  position: absolute;
  left: -16px;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, rgb(var(--ed-accent)), rgb(var(--ed-accent2)));
  border-radius: 2px;
  opacity: 0;
  transition: opacity 0.18s;
}
.article-row:hover::before { opacity: 1; }
.article-row:first-child { border-top: 1px solid rgb(var(--ed-border)); }
.article-row:hover { padding-left: 8px; }
.article-row-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  letter-spacing: 0.1em;
  color: rgb(var(--ed-muted));
  text-transform: uppercase;
  padding-top: 3px;
  transition: color 0.18s;
}
.article-row:hover .article-row-tag { color: rgb(var(--ed-accent)); }
.article-row-body { display: flex; flex-direction: column; gap: 5px; }
.article-row-title {
  font-family: 'Iowan Old Style', Charter, Georgia, serif;
  font-size: 20px;
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: -0.01em;
  color: rgb(var(--ed-fg));
  transition: color 0.18s;
}
.article-row:hover .article-row-title { color: rgb(var(--ed-accent)); }
.article-row-excerpt { font-size: 15px; color: rgb(var(--ed-muted)); line-height: 1.6; }
.article-row-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: rgb(var(--ed-muted));
  text-align: right;
  white-space: nowrap;
  padding-top: 3px;
}
@media (max-width: 600px) {
  .article-row { grid-template-columns: 60px 1fr; }
  .article-row-meta { display: none; }
  .article-row-title { font-size: 18px; }
}
</style>
