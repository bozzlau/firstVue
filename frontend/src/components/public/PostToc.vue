<script setup>
import { computed, inject, ref } from 'vue'

const props = defineProps({
  items: { type: Array, default: () => [] },
  activeId: { type: String, default: null },
})

const tocVisible = inject('tocVisible', ref(true))

const itemsWithLabel = computed(() => {
  let h2 = 0
  return props.items.map((item) => ({
    ...item,
    label: item.depth === 2 ? String(++h2).padStart(2, '0') : '·',
  }))
})

function jump(item) {
  const el = document.getElementById(item.id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function close() {
  tocVisible.value = false
}
</script>

<template>
  <section class="ed-panel">
    <header class="flex items-center justify-between mb-3">
      <span class="ed-panel-title">目录</span>
      <button
        type="button"
        class="text-xs text-ed-muted hover:text-ed-accent transition-colors leading-none"
        aria-label="hide TOC"
        @click="close"
      >✕</button>
    </header>
    <nav class="max-h-[calc(100vh-9rem)] overflow-y-auto -mx-1">
      <ul>
        <li v-for="item in itemsWithLabel" :key="item.id">
          <button
            type="button"
            class="relative w-full text-left flex items-start gap-2 py-1.5 px-2 rounded-lg transition-colors"
            :class="[
              item.depth === 3 ? 'pl-6' : 'pl-2',
              activeId === item.id
                ? 'text-ed-accent bg-ed-accent/8'
                : 'text-ed-muted hover:text-ed-fg hover:bg-ed-surface2',
            ]"
            @click="jump(item)"
          >
            <span
              v-if="activeId === item.id"
              class="absolute left-0 top-1 bottom-1 w-0.5 rounded-full bg-ed-accent"
              aria-hidden="true"
            />
            <span
              class="font-mono text-[10px] shrink-0 mt-[3px] w-5"
              :class="activeId === item.id ? 'text-ed-accent' : 'text-ed-muted'"
            >{{ item.label }}</span>
            <span class="text-sm leading-relaxed truncate font-sans">{{ item.text }}</span>
          </button>
        </li>
      </ul>
    </nav>
  </section>
</template>
