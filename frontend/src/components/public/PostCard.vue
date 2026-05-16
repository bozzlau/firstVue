<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  post: { type: Object, required: true },
  index: { type: Number, default: null },
})

const router = useRouter()

const code = computed(() => {
  const n = props.index != null ? props.index : props.post.id
  return String(n).padStart(3, '0')
})

const dateStr = computed(() => {
  const d = new Date(props.post.created_at)
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}.${pad(d.getMonth() + 1)}.${pad(d.getDate())}`
})
</script>

<template>
  <article
    class="hud-frame bg-hud-surface cursor-pointer group transition-colors hover:bg-hud-surfaceAlt animate-hud-fade-up"
    @click="router.push(`/posts/${post.slug}`)"
  >
    <span class="hud-glow-bar" />
    <div class="flex items-center justify-between gap-3 px-4 h-7 border-b border-hud-borderDim bg-hud-amber/[0.04]">
      <div class="flex items-center gap-3 font-mono text-[11px] uppercase tracking-wider min-w-0">
        <span class="text-hud-amber">[{{ code }}]</span>
        <span class="text-hud-textMuted">◆</span>
        <span class="text-hud-textDim">{{ dateStr }}</span>
        <span class="text-hud-textMuted">·</span>
        <span class="text-hud-textDim">▸ {{ post.views }}</span>
      </div>
      <span
        v-if="post.category"
        class="font-mono text-[10px] uppercase tracking-wider text-hud-amber border border-hud-amberDim/60 px-1.5 py-0.5 shrink-0"
      >
        {{ post.category.name }}
      </span>
    </div>

    <div class="flex gap-4 p-4">
      <div class="flex-1 min-w-0">
        <h2 class="font-display text-xl font-semibold text-hud-text leading-snug mb-2 line-clamp-2 group-hover:text-hud-amberSoft transition-colors">
          {{ post.title }}
        </h2>
        <p
          v-if="post.summary"
          class="text-sm text-hud-textDim leading-relaxed line-clamp-2"
        >
          {{ post.summary }}
        </p>
      </div>

      <img
        v-if="post.cover_image"
        :src="post.cover_image"
        :alt="post.title"
        class="w-24 h-20 object-cover border border-hud-borderDim shrink-0 grayscale group-hover:grayscale-0 transition-all"
      />
    </div>

    <div class="flex items-center gap-2 px-4 pb-3">
      <div class="flex-1 h-px bg-gradient-to-r from-hud-amber/40 via-hud-amberDim/40 to-transparent" />
      <div v-if="post.tags?.length" class="flex items-center gap-3 font-mono text-[10px] uppercase tracking-wider text-hud-textMuted shrink-0">
        <span
          v-for="(tag, i) in post.tags"
          :key="tag.id"
          class="flex items-center gap-3"
        >
          <span class="hover:text-hud-amber transition-colors">{{ tag.name }}</span>
          <span v-if="i < post.tags.length - 1" class="text-hud-borderDim">·</span>
        </span>
      </div>
    </div>
  </article>
</template>
