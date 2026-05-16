<script setup>
defineProps({
  label: { type: String, default: '' },
  status: { type: String, default: '' },
  noPad: { type: Boolean, default: false },
})
</script>

<template>
  <section class="hud-frame">
    <header
      v-if="label || status"
      class="flex items-center justify-between border-b border-hud-borderDim h-7 px-3 bg-hud-amber/5"
    >
      <span class="font-mono text-[11px] uppercase tracking-[0.18em] text-hud-amber">{{ label }}</span>
      <span v-if="status" class="font-mono text-[10px] uppercase tracking-wider text-hud-textMuted">{{ status }}</span>
    </header>
    <div :class="noPad ? '' : 'p-4'">
      <slot />
    </div>
  </section>
</template>
