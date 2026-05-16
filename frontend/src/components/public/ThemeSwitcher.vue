<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useThemeStore } from '../../stores/theme'

const theme = useThemeStore()
const open = ref(false)
const wrapper = ref(null)

function toggle() {
  open.value = !open.value
}

function pick(key) {
  theme.setTheme(key)
  open.value = false
}

function onDocClick(e) {
  if (!wrapper.value) return
  if (!wrapper.value.contains(e.target)) open.value = false
}

function onEsc(e) {
  if (e.key === 'Escape') open.value = false
}

onMounted(() => {
  document.addEventListener('click', onDocClick)
  document.addEventListener('keydown', onEsc)
})
onUnmounted(() => {
  document.removeEventListener('click', onDocClick)
  document.removeEventListener('keydown', onEsc)
})
</script>

<template>
  <div ref="wrapper" class="relative">
    <button
      type="button"
      class="hud-tag flex items-center gap-1.5"
      :class="open ? 'border-hud-amber text-hud-amber bg-hud-amber/10' : ''"
      @click.stop="toggle"
    >
      <span class="text-hud-amber text-[11px]">◐</span>
      <span>THEME</span>
    </button>

    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 -translate-y-1"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-1"
    >
      <div
        v-if="open"
        class="hud-frame absolute right-0 top-full mt-2 w-64 z-30 bg-hud-surface shadow-2xl"
        @click.stop
      >
        <div class="flex items-center justify-between h-7 px-3 border-b border-hud-borderDim bg-hud-amber/5">
          <span class="font-mono text-[11px] uppercase tracking-[0.18em] text-hud-amber">// PALETTE</span>
          <span class="font-mono text-[10px] uppercase tracking-wider text-hud-textMuted">{{ theme.themes.length }} OPT</span>
        </div>
        <ul class="divide-y divide-hud-borderDim">
          <li v-for="(t, i) in theme.themes" :key="t.key">
            <button
              type="button"
              class="w-full flex items-center gap-3 px-3 py-2.5 text-left transition-colors group"
              :class="theme.current === t.key
                ? 'bg-hud-amber/10 text-hud-amber'
                : 'text-hud-text hover:bg-hud-amber/5'"
              @click="pick(t.key)"
            >
              <span
                class="font-mono text-[10px] w-7 shrink-0"
                :class="theme.current === t.key ? 'text-hud-amber' : 'text-hud-textMuted'"
              >
                <span v-if="theme.current === t.key">▸</span>
                <span v-else>·</span>
                {{ String(i + 1).padStart(2, '0') }}
              </span>

              <span class="flex items-center gap-1 shrink-0">
                <span
                  class="w-3.5 h-3.5 border border-hud-borderDim"
                  :style="{ background: t.swatch[1] }"
                />
                <span
                  class="w-3.5 h-3.5 border border-hud-borderDim"
                  :style="{ background: t.swatch[0] }"
                />
              </span>

              <span class="flex-1 min-w-0">
                <div class="text-sm truncate"
                  :class="theme.current === t.key ? 'text-hud-amberSoft' : 'group-hover:text-hud-amberSoft'"
                >
                  {{ t.name }}
                </div>
                <div class="font-mono text-[10px] uppercase tracking-wider text-hud-textMuted">
                  {{ t.key }} · {{ t.mode }}
                </div>
              </span>
            </button>
          </li>
        </ul>
        <div class="px-3 py-2 border-t border-hud-borderDim font-mono text-[10px] uppercase tracking-wider text-hud-textMuted">
          ▮ STORED IN local
        </div>
      </div>
    </transition>
  </div>
</template>
