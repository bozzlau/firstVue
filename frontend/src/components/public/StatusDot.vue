<script setup>
defineProps({
  label: { type: String, default: '' },
  color: { type: String, default: 'amber' },
})
</script>

<template>
  <span class="inline-flex items-center gap-2 font-mono text-xs uppercase tracking-wider">
    <span
      class="inline-block w-1.5 h-1.5 rounded-full animate-hud-pulse"
      :class="{
        'bg-hud-amber shadow-[0_0_6px_#ffb700]': color === 'amber',
        'bg-hud-warn shadow-[0_0_6px_#ff3344]': color === 'warn',
        'bg-hud-textMuted': color === 'dim',
      }"
    />
    <span v-if="label" class="text-hud-textDim">{{ label }}</span>
  </span>
</template>
