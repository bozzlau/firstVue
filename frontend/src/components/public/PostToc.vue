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
  <section class="hud-frame">
    <header class="flex items-center justify-between border-b border-hud-borderDim h-7 px-3 bg-hud-amber/5">
      <span class="font-mono text-xs uppercase tracking-[0.18em] text-hud-amber">// CONTENTS</span>
      <button
        type="button"
        class="font-mono text-xs text-hud-textMuted hover:text-hud-amber transition-colors leading-none"
        aria-label="hide TOC"
        @click="close"
      >✕</button>
    </header>
    <nav class="py-2 max-h-[calc(100vh-9rem)] overflow-y-auto">
      <ul>
        <li v-for="item in itemsWithLabel" :key="item.id">
          <button
            type="button"
            class="relative w-full text-left flex items-start gap-2 py-1.5 transition-colors"
            :class="[
              item.depth === 3 ? 'pl-7 pr-3' : 'pl-3 pr-3',
              activeId === item.id
                ? 'text-hud-amber bg-hud-amber/10'
                : 'text-hud-textDim hover:text-hud-amberSoft hover:bg-hud-amber/5',
            ]"
            @click="jump(item)"
          >
            <span
              v-if="activeId === item.id"
              class="absolute left-0 top-0 bottom-0 w-[2px] bg-hud-amber"
              aria-hidden="true"
            />
            <span
              class="font-mono text-[11px] shrink-0 mt-[3px] w-5"
              :class="activeId === item.id ? 'text-hud-amber' : 'text-hud-textMuted'"
            >{{ item.label }}</span>
            <span class="text-sm leading-relaxed truncate">{{ item.text }}</span>
          </button>
        </li>
      </ul>
    </nav>
  </section>
</template>
