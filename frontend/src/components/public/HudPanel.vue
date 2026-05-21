<script setup>
defineProps({
  label: { type: String, default: '' },
  status: { type: String, default: '' },
  noPad: { type: Boolean, default: false },
})
</script>

<template>
  <section class="ed-panel">
    <header v-if="label || status" class="flex items-center justify-between mb-4">
      <span class="ed-panel-title">{{ label }}</span>
      <span v-if="status" class="font-mono text-[10px] uppercase tracking-wider text-ed-muted">{{ status }}</span>
    </header>
    <div :class="noPad ? '-mx-5 -mb-5' : ''">
      <slot />
    </div>
  </section>
</template>
