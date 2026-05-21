<script setup>
const stack = [
  { label: '前端', items: ['Vue 3', 'Vite', 'Tailwind', 'Pinia'] },
  { label: '后端', items: ['FastAPI', 'SQLAlchemy', 'Alembic', 'Pydantic'] },
  { label: '兴趣', items: ['学习', '记录', '思考'] },
]

const timeline = [
  { date: '2026.05.16', text: '前端界面升级为编辑风格' },
  { date: '2026.05.10', text: '前端模块上线' },
  { date: '2026.05.01', text: 'FastAPI 后端核心完成' },
]
</script>

<template>
  <div class="space-y-10">
    <!-- Identity -->
    <section class="reveal">
      <div class="font-mono text-[11px] uppercase tracking-wider text-ed-muted mb-2">关于</div>
      <h1 class="font-serif text-4xl font-bold text-ed-fg mb-6" style="letter-spacing:-0.02em;">
        你好，我是<span style="background:linear-gradient(135deg,rgb(var(--ed-accent)),rgb(var(--ed-accent2)));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">博主</span>
      </h1>
      <p class="text-base text-ed-muted leading-relaxed max-w-xl mb-8">
        这是一个用 FastAPI + Vue 3 构建的个人博客，记录学习与思考。
        写代码、写文字、写生活，在数字世界寻找真实的重量。
      </p>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div v-for="item in [
          { label: '昵称', value: 'bozzlau' },
          { label: '地区', value: 'CN / ZH' },
          { label: '状态', value: '学习中', accent: true },
          { label: '协议', value: 'MIT' },
        ]" :key="item.label"
          class="ed-panel text-center py-4">
          <div class="font-mono text-[10px] uppercase tracking-wider text-ed-muted mb-1">{{ item.label }}</div>
          <div class="font-semibold text-sm" :class="item.accent ? 'text-ed-accent' : 'text-ed-fg'">{{ item.value }}</div>
        </div>
      </div>
    </section>

    <!-- Stack -->
    <section class="reveal">
      <div class="ed-sec-title mb-6">技术栈</div>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div v-for="g in stack" :key="g.label" class="ed-panel">
          <div class="font-mono text-[10px] uppercase tracking-wider text-ed-accent mb-3">{{ g.label }}</div>
          <ul class="space-y-1.5">
            <li v-for="it in g.items" :key="it" class="flex items-center gap-2 text-sm text-ed-fg">
              <span class="w-1 h-1 rounded-full bg-ed-accent shrink-0"></span>
              {{ it }}
            </li>
          </ul>
        </div>
      </div>
    </section>

    <!-- Timeline -->
    <section class="reveal">
      <div class="ed-sec-title mb-6">更新日志</div>
      <div class="space-y-3">
        <div v-for="item in timeline" :key="item.date"
          class="flex items-start gap-4 py-3 border-b border-ed-border last:border-0">
          <time class="font-mono text-[11px] text-ed-muted shrink-0 pt-0.5">{{ item.date }}</time>
          <span class="text-sm text-ed-fg">{{ item.text }}</span>
        </div>
      </div>
    </section>
  </div>
</template>
