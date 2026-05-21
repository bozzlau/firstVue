<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { useRouter } from 'vue-router'
import { getPosts } from '../../api/posts'
import PostCard from '../../components/public/PostCard.vue'

const router = useRouter()

const tags = inject('tags', ref([]))
const categories = inject('categories', ref([]))
const totalPosts = inject('totalPosts', ref(0))

const tagCloud = computed(() => {
  if (!tags.value.length) return []
  const counts = tags.value.map(t => t.post_count ?? 0)
  const maxC = Math.max(...counts, 1)
  const minC = Math.min(...counts, 0)
  return tags.value.map(t => {
    const c = t.post_count ?? 0
    const ratio = maxC > minC
      ? (Math.log(c + 1) - Math.log(minC + 1)) / (Math.log(maxC + 1) - Math.log(minC + 1))
      : 0
    const size = 12 + ratio * 20
    const r = Math.round(232 * ratio + 138 * (1 - ratio))
    const g = Math.round(93 * ratio + 130 * (1 - ratio))
    const b = Math.round(58 * ratio + 120 * (1 - ratio))
    const alpha = 0.5 + ratio * 0.5
    return { ...t, size, color: `rgba(${r},${g},${b},${alpha})` }
  })
})

const recentPosts = ref([])
const featuredPost = computed(() => recentPosts.value[0] || null)

const posts = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const loading = ref(false)

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

async function load() {
  loading.value = true
  try {
    const data = await getPosts({ page: page.value, page_size: pageSize })
    posts.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const recentData = await getPosts({ page: 1, page_size: 3 })
  recentPosts.value = recentData.items
  await load()
})

function go(delta) {
  const next = page.value + delta
  if (next < 1 || next > totalPages.value) return
  page.value = next
  load()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const pad = n => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

function scrollToArticles() {
  const el = document.getElementById('articles')
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <div>
    <!-- ── Hero ── -->
    <section class="hero-section reveal">
      <!-- Blobs -->
      <div style="position:absolute;width:480px;height:480px;background:radial-gradient(circle,rgba(232,93,58,0.18) 0%,transparent 70%);top:-120px;right:-80px;filter:blur(60px);pointer-events:none;animation:blob-float 9s ease-in-out infinite;"></div>
      <div style="position:absolute;width:360px;height:360px;background:radial-gradient(circle,rgba(245,166,35,0.14) 0%,transparent 70%);bottom:-60px;left:10%;filter:blur(60px);pointer-events:none;animation:blob-float 11s ease-in-out infinite;animation-delay:-3s;"></div>
      <div style="position:absolute;width:280px;height:280px;background:radial-gradient(circle,rgba(78,205,196,0.12) 0%,transparent 70%);top:40%;right:30%;filter:blur(60px);pointer-events:none;animation:blob-float 13s ease-in-out infinite;animation-delay:-6s;"></div>

      <div class="hero-inner">
        <!-- Left -->
        <div>
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:20px;">
            <div style="width:24px;height:1px;background:rgb(var(--ed-accent));"></div>
            <span style="font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:0.14em;color:rgb(var(--ed-accent));text-transform:uppercase;">独立开发者 · 写作者</span>
          </div>

          <h1 style="font-family:'Iowan Old Style',Charter,Georgia,serif;font-size:clamp(48px,6.5vw,88px);font-weight:700;line-height:1.0;letter-spacing:-0.03em;color:rgb(var(--ed-fg));margin-bottom:24px;">
            记录<span style="background:linear-gradient(135deg,rgb(var(--ed-accent)),rgb(var(--ed-accent2)));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">思考</span><br>与探索
          </h1>

          <p style="font-size:16px;color:rgb(var(--ed-muted));line-height:1.8;max-width:440px;margin-bottom:36px;">
            这里是我的数字花园，记录全栈开发、独立产品和生活思考。用文字留住那些值得被记住的瞬间。
          </p>

          <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <button
              @click="scrollToArticles"
              style="display:inline-flex;align-items:center;gap:8px;padding:11px 24px;background:linear-gradient(135deg,rgb(var(--ed-accent)),rgb(var(--ed-accent2)));color:#fff;border:none;border-radius:100px;font-size:14px;font-weight:600;cursor:pointer;box-shadow:0 4px 20px rgba(232,93,58,0.25);transition:transform 0.2s,box-shadow 0.2s;"
              @mouseenter="e => { e.currentTarget.style.transform='translateY(-2px)'; e.currentTarget.style.boxShadow='0 8px 28px rgba(232,93,58,0.35)'; }"
              @mouseleave="e => { e.currentTarget.style.transform=''; e.currentTarget.style.boxShadow='0 4px 20px rgba(232,93,58,0.25)'; }"
            >开始阅读 →</button>
            <router-link
              to="/about"
              style="display:inline-flex;align-items:center;gap:8px;padding:11px 24px;background:transparent;color:rgb(var(--ed-fg));border:1px solid rgb(var(--ed-border));border-radius:100px;font-size:14px;font-weight:500;text-decoration:none;transition:all 0.2s;"
              @mouseenter="e => { e.currentTarget.style.borderColor='rgb(var(--ed-fg))'; e.currentTarget.style.background='rgb(var(--ed-surface))'; }"
              @mouseleave="e => { e.currentTarget.style.borderColor='rgb(var(--ed-border))'; e.currentTarget.style.background='transparent'; }"
            >关于我</router-link>
          </div>
        </div>

        <!-- Right: hero card -->
        <div style="background:rgb(var(--ed-surface));border-radius:24px;padding:32px;box-shadow:0 2px 0 rgb(var(--ed-border)),0 20px 60px rgba(26,23,20,0.08);position:relative;overflow:hidden;">
          <div style="position:absolute;top:-40px;right:-40px;width:160px;height:160px;background:linear-gradient(135deg,rgba(232,93,58,0.12),rgba(245,166,35,0.08));border-radius:50%;animation:blob-morph 8s ease-in-out infinite;pointer-events:none;"></div>

          <div style="font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.12em;color:rgb(var(--ed-muted));text-transform:uppercase;margin-bottom:16px;position:relative;z-index:1;">最近更新</div>

          <div style="position:relative;z-index:1;">
            <div
              v-for="(post, i) in recentPosts"
              :key="post.id"
              :style="{
                padding: '14px 0',
                borderBottom: i < recentPosts.length - 1 ? '1px solid rgb(var(--ed-border))' : 'none',
                cursor: 'pointer',
                transition: 'all 0.2s',
                display: 'flex',
                alignItems: 'flex-start',
                gap: '12px'
              }"
              @click="router.push(`/posts/${post.slug}`)"
              @mouseenter="e => { e.currentTarget.style.paddingLeft='6px'; e.currentTarget.querySelector('.hci-dot').style.transform='scale(1.5)'; e.currentTarget.querySelector('.hci-title').style.color='rgb(var(--ed-accent))'; }"
              @mouseleave="e => { e.currentTarget.style.paddingLeft='0'; e.currentTarget.querySelector('.hci-dot').style.transform=''; e.currentTarget.querySelector('.hci-title').style.color='rgb(var(--ed-fg))'; }"
            >
              <div class="hci-dot" style="width:6px;height:6px;border-radius:50%;background:linear-gradient(135deg,rgb(var(--ed-accent)),rgb(var(--ed-accent2)));flex-shrink:0;margin-top:6px;transition:transform 0.2s;"></div>
              <div style="flex:1;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:rgb(var(--ed-accent));letter-spacing:0.08em;text-transform:uppercase;margin-bottom:3px;">
                  {{ post.tags?.[0]?.name || post.category?.name || '' }}
                </div>
                <div class="hci-title" style="font-family:'Iowan Old Style',Charter,Georgia,serif;font-size:15px;font-weight:600;line-height:1.35;color:rgb(var(--ed-fg));transition:color 0.15s;">
                  {{ post.title }}
                </div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:rgb(var(--ed-muted));margin-top:4px;">{{ formatDate(post.created_at) }}</div>
              </div>
            </div>
          </div>

          <!-- Stats -->
          <div style="display:flex;margin-top:24px;border-top:1px solid rgb(var(--ed-border));padding-top:20px;position:relative;z-index:1;">
            <div style="flex:1;text-align:center;">
              <span style="font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:700;color:rgb(var(--ed-fg));letter-spacing:-0.02em;display:block;">{{ totalPosts }}</span>
              <span style="font-size:13px;color:rgb(var(--ed-muted));letter-spacing:0.06em;text-transform:uppercase;margin-top:2px;display:block;">篇文章</span>
            </div>
            <div style="flex:1;text-align:center;border-left:1px solid rgb(var(--ed-border));">
              <span style="font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:700;color:rgb(var(--ed-fg));letter-spacing:-0.02em;display:block;">{{ tags.length }}</span>
              <span style="font-size:13px;color:rgb(var(--ed-muted));letter-spacing:0.06em;text-transform:uppercase;margin-top:2px;display:block;">个标签</span>
            </div>
            <div style="flex:1;text-align:center;border-left:1px solid rgb(var(--ed-border));">
              <span style="font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:700;color:rgb(var(--ed-fg));letter-spacing:-0.02em;display:block;">3</span>
              <span style="font-size:13px;color:rgb(var(--ed-muted));letter-spacing:0.06em;text-transform:uppercase;margin-top:2px;display:block;">年记录</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Category nav ── -->
    <nav style="border-bottom:1px solid rgb(var(--ed-border));background:rgb(var(--ed-bg));position:sticky;top:56px;z-index:10;">
      <div style="display:flex;align-items:center;overflow-x:auto;scrollbar-width:none;-ms-overflow-style:none;">
        <router-link
          to="/"
          style="display:flex;align-items:center;gap:5px;padding:12px 18px;white-space:nowrap;font-family:'JetBrains Mono',monospace;font-size:14px;letter-spacing:0.04em;cursor:pointer;border-bottom:2px solid transparent;transition:all 0.18s;flex-shrink:0;text-decoration:none;"
          :style="$route.path === '/' ? 'color:rgb(var(--ed-accent));border-bottom-color:rgb(var(--ed-accent));' : 'color:rgb(var(--ed-muted));'"
        >
          全部
          <span style="font-size:12px;background:rgb(var(--ed-surface2));border-radius:10px;padding:1px 6px;transition:all 0.18s;"
            :style="$route.path === '/' ? 'background:rgba(232,93,58,0.12);color:rgb(var(--ed-accent));' : 'color:rgb(var(--ed-muted));opacity:0.6;'">
            {{ totalPosts }}
          </span>
        </router-link>

        <router-link
          v-for="cat in categories"
          :key="cat.id"
          :to="`/category/${cat.slug}`"
          style="display:flex;align-items:center;gap:5px;padding:12px 18px;white-space:nowrap;font-family:'JetBrains Mono',monospace;font-size:14px;letter-spacing:0.04em;cursor:pointer;border-bottom:2px solid transparent;transition:all 0.18s;flex-shrink:0;text-decoration:none;"
          :style="$route.params.slug === cat.slug && $route.path.startsWith('/category') ? 'color:rgb(var(--ed-accent));border-bottom-color:rgb(var(--ed-accent));' : 'color:rgb(var(--ed-muted));'"
        >
          {{ cat.name }}
          <span style="font-size:12px;background:rgb(var(--ed-surface2));border-radius:10px;padding:1px 6px;transition:all 0.18s;"
            :style="$route.params.slug === cat.slug && $route.path.startsWith('/category') ? 'background:rgba(232,93,58,0.12);color:rgb(var(--ed-accent));' : 'color:rgb(var(--ed-muted));opacity:0.6;'">
            {{ cat.post_count ?? 0 }}
          </span>
        </router-link>
      </div>
    </nav>

    <!-- ── Featured article ── -->
    <section v-if="featuredPost" id="articles" style="padding-top:56px;">
      <div style="display:flex;align-items:center;justify-content:space-between;padding-bottom:28px;">
        <div class="ed-sec-title">精选文章</div>
        <a href="#articles-list" style="font-family:'JetBrains Mono',monospace;font-size:13px;color:rgb(var(--ed-muted));letter-spacing:0.06em;text-decoration:none;display:flex;align-items:center;gap:5px;transition:color 0.15s;"
          @mouseenter="e => e.currentTarget.style.color='rgb(var(--ed-accent))'"
          @mouseleave="e => e.currentTarget.style.color='rgb(var(--ed-muted))'">全部精选 →</a>
      </div>

      <div
        style="display:grid;grid-template-columns:1fr 1fr;border-radius:20px;overflow:hidden;box-shadow:0 2px 0 rgb(var(--ed-border)),0 24px 64px rgba(26,23,20,0.09);cursor:pointer;transition:transform 0.3s,box-shadow 0.3s;"
        class="featured-card-grid"
        @click="router.push(`/posts/${featuredPost.slug}`)"
        @mouseenter="e => { e.currentTarget.style.transform='translateY(-4px)'; e.currentTarget.style.boxShadow='0 2px 0 rgb(var(--ed-border)),0 32px 80px rgba(26,23,20,0.14)'; }"
        @mouseleave="e => { e.currentTarget.style.transform=''; e.currentTarget.style.boxShadow='0 2px 0 rgb(var(--ed-border)),0 24px 64px rgba(26,23,20,0.09)'; }"
      >
        <!-- Dark visual -->
        <div style="min-height:300px;position:relative;overflow:hidden;background:linear-gradient(135deg,#1a1714 0%,#2e2218 60%,#1a1c10 100%);display:flex;align-items:center;justify-content:center;">
          <div style="position:absolute;width:300px;height:300px;background:radial-gradient(circle,rgba(232,93,58,0.3) 0%,transparent 70%);border-radius:50%;top:-60px;right:-60px;animation:blob-float 10s ease-in-out infinite;pointer-events:none;"></div>
          <div style="position:absolute;width:200px;height:200px;background:radial-gradient(circle,rgba(78,205,196,0.2) 0%,transparent 70%);border-radius:50%;bottom:-40px;left:20px;animation:blob-float 13s ease-in-out infinite reverse;pointer-events:none;"></div>
          <div style="font-family:'Iowan Old Style',Charter,Georgia,serif;font-size:100px;font-weight:700;color:rgba(255,255,255,0.05);line-height:1;user-select:none;letter-spacing:-0.05em;position:relative;z-index:1;">
            {{ featuredPost.title.slice(0, 2) }}
          </div>
          <div v-if="featuredPost.category" style="position:absolute;bottom:20px;left:20px;font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.1em;color:rgba(255,255,255,0.5);text-transform:uppercase;background:rgba(0,0,0,0.4);padding:4px 8px;border-radius:4px;">
            {{ featuredPost.category.name }}
          </div>
        </div>

        <!-- Content -->
        <div style="background:rgb(var(--ed-surface));padding:40px 44px;display:flex;flex-direction:column;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.12em;color:rgb(var(--ed-accent));text-transform:uppercase;margin-bottom:16px;">
            {{ featuredPost.category?.name }}{{ featuredPost.tags?.[0] ? ' / ' + featuredPost.tags[0].name : '' }}
          </div>
          <div style="font-family:'Iowan Old Style',Charter,Georgia,serif;font-size:clamp(22px,2.8vw,34px);font-weight:700;line-height:1.2;letter-spacing:-0.02em;color:rgb(var(--ed-fg));margin-bottom:16px;flex:1;transition:color 0.15s;"
            @mouseenter="e => e.currentTarget.style.color='rgb(var(--ed-accent))'"
            @mouseleave="e => e.currentTarget.style.color='rgb(var(--ed-fg))'">
            {{ featuredPost.title }}
          </div>
          <div style="font-size:14px;color:rgb(var(--ed-muted));line-height:1.75;margin-bottom:32px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;">
            {{ featuredPost.summary }}
          </div>
          <div style="display:flex;align-items:center;justify-content:space-between;padding-top:20px;border-top:1px solid rgb(var(--ed-border));">
            <span style="font-family:'JetBrains Mono',monospace;font-size:13px;color:rgb(var(--ed-muted));">{{ formatDate(featuredPost.created_at) }}</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:13px;color:rgb(var(--ed-accent));letter-spacing:0.06em;display:flex;align-items:center;gap:5px;">阅读全文 →</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Articles list ── -->
    <section id="articles-list" style="padding-top:56px;padding-bottom:72px;">
      <div style="display:flex;align-items:center;justify-content:space-between;padding-bottom:28px;" class="reveal">
        <div class="ed-sec-title">最新文章</div>
        <span style="font-family:'JetBrains Mono',monospace;font-size:13px;color:rgb(var(--ed-muted));">{{ total }} 篇</span>
      </div>

      <div class="articles-heatmap-wrap" style="display:grid;grid-template-columns:2fr 1fr;gap:48px;align-items:start;">
        <!-- Articles -->
        <div>
          <div v-if="loading" style="text-align:center;padding:64px 0;color:rgb(var(--ed-muted));font-size:14px;">加载中...</div>
          <div v-else-if="posts.length === 0" style="text-align:center;padding:64px 0;color:rgb(var(--ed-muted));font-size:14px;">暂无文章</div>
          <div v-else>
            <PostCard v-for="(post, i) in posts" :key="post.id" :post="post" :index="(page-1)*pageSize+i+1" />
          </div>

          <div v-if="!loading && total > pageSize" style="margin-top:32px;display:flex;align-items:center;justify-content:center;gap:16px;">
            <button
              :disabled="page === 1"
              style="display:inline-flex;align-items:center;gap:8px;padding:10px 22px;background:transparent;border:1px solid rgb(var(--ed-border));border-radius:100px;font-size:13px;cursor:pointer;color:rgb(var(--ed-fg));transition:all 0.2s;"
              :style="page === 1 ? 'opacity:0.35;cursor:not-allowed;' : ''"
              @click="go(-1)"
              @mouseenter="e => { if(page>1){ e.currentTarget.style.borderColor='rgb(var(--ed-fg))'; } }"
              @mouseleave="e => e.currentTarget.style.borderColor='rgb(var(--ed-border))'"
            >← 上一页</button>
            <span style="font-family:'JetBrains Mono',monospace;font-size:14px;color:rgb(var(--ed-muted));">{{ page }} / {{ totalPages }}</span>
            <button
              :disabled="page >= totalPages"
              style="display:inline-flex;align-items:center;gap:8px;padding:10px 22px;background:transparent;border:1px solid rgb(var(--ed-border));border-radius:100px;font-size:13px;cursor:pointer;color:rgb(var(--ed-fg));transition:all 0.2s;"
              :style="page >= totalPages ? 'opacity:0.35;cursor:not-allowed;' : ''"
              @click="go(1)"
              @mouseenter="e => { if(page<totalPages){ e.currentTarget.style.borderColor='rgb(var(--ed-fg))'; } }"
              @mouseleave="e => e.currentTarget.style.borderColor='rgb(var(--ed-border))'"
            >下一页 →</button>
          </div>
        </div>

        <!-- Heatmap panel -->
        <div v-if="tagCloud.length" class="heatmap-panel" style="position:sticky;top:120px;background:rgb(var(--ed-surface));border-radius:16px;padding:24px;box-shadow:0 2px 0 rgb(var(--ed-border)),0 12px 40px rgba(26,23,20,0.06);">
          <div class="heatmap-title">话题热度</div>
          <div style="display:flex;flex-wrap:wrap;gap:8px 10px;align-items:baseline;line-height:1.4;">
            <router-link
              v-for="tag in tagCloud" :key="tag.id"
              :to="`/tag/${tag.slug}`"
              class="heatmap-tag"
              :style="{ fontSize: tag.size + 'px', color: tag.color }"
              :title="`${tag.name} · ${tag.post_count ?? 0} 篇`"
            >{{ tag.name }}</router-link>
          </div>
          <div style="margin-top:20px;padding-top:16px;border-top:1px solid rgb(var(--ed-border));display:flex;align-items:center;justify-content:space-between;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:12px;color:rgb(var(--ed-muted));letter-spacing:0.06em;">少</span>
            <div style="display:flex;gap:3px;align-items:center;">
              <div style="width:8px;height:8px;border-radius:50%;background:rgb(138,130,120);opacity:0.4;"></div>
              <div style="width:8px;height:8px;border-radius:50%;background:rgb(138,130,120);opacity:0.7;"></div>
              <div style="width:8px;height:8px;border-radius:50%;background:rgb(245,166,35);opacity:0.8;"></div>
              <div style="width:8px;height:8px;border-radius:50%;background:rgb(232,93,58);"></div>
            </div>
            <span style="font-family:'JetBrains Mono',monospace;font-size:12px;color:rgb(var(--ed-muted));letter-spacing:0.06em;">多</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero-section {
  position: relative;
  overflow: hidden;
  padding: 72px 0 72px;
  margin-left: calc(-50vw + 50%);
  margin-right: calc(-50vw + 50%);
}
.hero-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;
}
.articles-heatmap-wrap {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 48px;
  align-items: start;
}
.heatmap-panel {
  position: sticky;
  top: 120px;
  background: rgb(var(--ed-surface));
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 0 rgb(var(--ed-border)), 0 12px 40px rgba(26,23,20,0.06);
}
.heatmap-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  letter-spacing: 0.12em;
  color: rgb(var(--ed-muted));
  text-transform: uppercase;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.heatmap-title::before {
  content: '';
  width: 16px;
  height: 2px;
  background: linear-gradient(90deg, rgb(var(--ed-accent)), rgb(var(--ed-accent2)));
  border-radius: 2px;
}
.heatmap-tag {
  font-family: Inter, -apple-system, sans-serif;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, filter 0.2s;
  display: inline-block;
  text-decoration: none;
}
.heatmap-tag:hover { transform: scale(1.12); filter: brightness(1.15); }
@media (max-width: 900px) {
  .hero-inner { grid-template-columns: 1fr; gap: 40px; }
  .articles-heatmap-wrap { grid-template-columns: 1fr; gap: 40px; }
  .heatmap-panel { position: static; }
}
@media (max-width: 480px) {
  .hero-inner h1 { font-size: clamp(38px, 11vw, 56px) !important; }
}
.featured-card-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
}
@media (max-width: 768px) {
  .featured-card-grid { grid-template-columns: 1fr; }
}
</style>
