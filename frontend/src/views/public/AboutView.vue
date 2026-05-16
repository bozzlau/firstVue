<script setup>
import HudPanel from '../../components/public/HudPanel.vue'
import StatusDot from '../../components/public/StatusDot.vue'

const stack = [
  { label: 'FRONTEND', items: ['Vue 3', 'Vite', 'Tailwind', 'Pinia'] },
  { label: 'BACKEND', items: ['FastAPI', 'SQLAlchemy', 'Alembic', 'Pydantic'] },
  { label: 'INTEREST', items: ['学习', '记录', '思考'] },
]
</script>

<template>
  <div class="space-y-5">
    <HudPanel label="// IDENTITY" status="UPLINK STABLE">
      <div class="flex items-start gap-5">
        <div class="w-20 h-20 hud-frame flex items-center justify-center shrink-0 bg-hud-bg">
          <span class="font-mono text-2xl text-hud-amber">◆</span>
        </div>
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-3 mb-2">
            <h1 class="font-display text-2xl font-semibold text-hud-amberSoft">SUBJECT_001</h1>
            <StatusDot label="ACTIVE" />
          </div>
          <p class="text-sm text-hud-textDim leading-relaxed">
            这是一个用 FastAPI + Vue 3 构建的个人博客，记录学习与思考。
            前端走暗色 HUD 风格，后端走经典分层架构。
          </p>
          <div class="mt-4 grid grid-cols-2 gap-x-6 gap-y-1 font-mono text-[11px] uppercase tracking-wider">
            <div class="flex justify-between">
              <span class="text-hud-textMuted">CALLSIGN</span>
              <span class="text-hud-text">bozzlau</span>
            </div>
            <div class="flex justify-between">
              <span class="text-hud-textMuted">REGION</span>
              <span class="text-hud-text">CN / ZH</span>
            </div>
            <div class="flex justify-between">
              <span class="text-hud-textMuted">STATUS</span>
              <span class="text-hud-amber">LEARNING</span>
            </div>
            <div class="flex justify-between">
              <span class="text-hud-textMuted">LICENSE</span>
              <span class="text-hud-text">MIT</span>
            </div>
          </div>
        </div>
      </div>
    </HudPanel>

    <HudPanel label="// STACK_LOADOUT">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="g in stack" :key="g.label">
          <div class="font-mono text-[10px] uppercase tracking-widest text-hud-amber mb-2 pb-1 border-b border-hud-borderDim">
            ▸ {{ g.label }}
          </div>
          <ul class="space-y-1">
            <li
              v-for="it in g.items"
              :key="it"
              class="font-mono text-xs text-hud-textDim flex items-center gap-2"
            >
              <span class="text-hud-amber">·</span>
              <span>{{ it }}</span>
            </li>
          </ul>
        </div>
      </div>
    </HudPanel>

    <HudPanel label="// SYS_LOG">
      <div class="font-mono text-[11px] leading-6 text-hud-textDim space-y-0.5">
        <div><span class="text-hud-amber">[2026.05.16]</span> UI uplink upgraded to HUD v1.0</div>
        <div><span class="text-hud-amber">[2026.05.10]</span> Frontend module deployed</div>
        <div><span class="text-hud-amber">[2026.05.01]</span> FastAPI core online</div>
        <div><span class="text-hud-textMuted">[ ... ]</span></div>
      </div>
    </HudPanel>
  </div>
</template>
