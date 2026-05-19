<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { adminGetPost, adminCreatePost, adminUpdatePost } from '../../api/posts'
import { adminGetCategories } from '../../api/categories'
import { adminGetTags } from '../../api/tags'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const loading = ref(false)
const saving = ref(false)
const categories = ref([])
const tags = ref([])

const form = ref({
  title: '',
  slug: '',
  summary: '',
  content: '',
  cover_image: '',
  published: false,
  category_id: null,
  tag_ids: [],
})

const containerRef = ref(null)
const sidebarWidth = ref(256)
const isDragging = ref(false)
const MIN_SIDEBAR = 128  // 当前 256px 的一半
const MIN_MAIN = 400     // 主内容区最小宽度（当前约 800px 的一半）

function startDrag(e) {
  e.preventDefault()
  const startX = e.clientX
  const startWidth = sidebarWidth.value

  document.body.style.cursor = 'col-resize'
  document.body.style.userSelect = 'none'
  isDragging.value = true

  function onMove(e) {
    const delta = startX - e.clientX
    const containerWidth = containerRef.value?.offsetWidth ?? 1000
    const maxSidebar = containerWidth - MIN_MAIN - 16
    sidebarWidth.value = Math.max(MIN_SIDEBAR, Math.min(startWidth + delta, maxSidebar))
  }

  function onUp() {
    isDragging.value = false
    document.body.style.cursor = ''
    document.body.style.userSelect = ''
    document.removeEventListener('mousemove', onMove)
    document.removeEventListener('mouseup', onUp)
  }

  document.addEventListener('mousemove', onMove)
  document.addEventListener('mouseup', onUp)
}

onMounted(async () => {
  loading.value = true
  try {
    const [cats, tgs] = await Promise.all([adminGetCategories(), adminGetTags()])
    categories.value = cats
    tags.value = tgs

    if (isEdit.value) {
      const post = await adminGetPost(route.params.id)
      form.value = {
        title: post.title,
        slug: post.slug,
        summary: post.summary || '',
        content: post.content,
        cover_image: post.cover_image || '',
        published: post.published,
        category_id: post.category?.id ?? null,
        tag_ids: post.tags.map((t) => t.id),
      }
    }
  } finally {
    loading.value = false
  }
})

async function save() {
  saving.value = true
  try {
    if (isEdit.value) {
      await adminUpdatePost(route.params.id, form.value)
    } else {
      await adminCreatePost(form.value)
    }
    router.push('/admin/posts')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div v-loading="loading" class="flex flex-col h-full">
    <!-- Topbar -->
    <div class="sticky top-0 z-10 bg-white border-b border-[#e3e8ef] px-7 h-14 flex items-center justify-between shrink-0">
      <div class="flex items-center gap-2 text-[13px]">
        <router-link to="/admin/posts" class="text-[#697386] hover:text-[#635bff] transition-colors no-underline">文章管理</router-link>
        <span class="text-[#e3e8ef]">/</span>
        <span class="text-[#1a1f36] font-medium">{{ isEdit ? '编辑文章' : '新建文章' }}</span>
      </div>
      <div class="flex gap-2">
        <el-button @click="router.push('/admin/posts')">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </div>
    </div>

    <!-- Editor area -->
    <div ref="containerRef" class="flex flex-1 min-h-0 overflow-hidden">
      <!-- Main -->
      <div class="flex-1 min-w-0 overflow-y-auto p-7 space-y-4" :style="{ minWidth: MIN_MAIN + 'px' }">
        <el-form :model="form" label-position="top">
          <div class="flex gap-3">
            <el-form-item label="标题" class="flex-[2]">
              <el-input v-model="form.title" />
            </el-form-item>
            <el-form-item label="Slug（URL 路径）" class="flex-1">
              <el-input v-model="form.slug" />
            </el-form-item>
          </div>
          <el-form-item label="摘要">
            <el-input v-model="form.summary" placeholder="一句话描述文章内容" />
          </el-form-item>
          <el-form-item label="正文">
            <MdEditor v-model="form.content" style="height: 500px" />
          </el-form-item>
        </el-form>
      </div>

      <!-- Drag handle -->
      <div
        class="w-3 shrink-0 cursor-col-resize flex items-center justify-center group"
        @mousedown="startDrag"
      >
        <div
          class="w-px h-full transition-colors"
          :class="isDragging ? 'bg-[#635bff]' : 'bg-[#e3e8ef] group-hover:bg-[#635bff]/50'"
        />
      </div>

      <!-- Sidebar -->
      <div
        class="shrink-0 overflow-y-auto border-l border-[#e3e8ef] bg-white"
        :style="{ width: sidebarWidth + 'px', minWidth: MIN_SIDEBAR + 'px' }"
      >
        <el-form :model="form" label-position="top" class="p-5 space-y-1">
          <!-- Publish settings -->
          <div class="text-[11px] font-semibold text-[#697386] uppercase tracking-wider mb-3">发布设置</div>
          <el-form-item label="发布状态">
            <el-switch v-model="form.published" active-text="已发布" inactive-text="草稿" />
          </el-form-item>

          <div class="border-t border-[#e3e8ef] my-4"></div>

          <!-- Meta -->
          <div class="text-[11px] font-semibold text-[#697386] uppercase tracking-wider mb-3">分类与标签</div>
          <el-form-item label="分类">
            <el-select v-model="form.category_id" clearable placeholder="选择分类" class="w-full" :teleported="false">
              <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="标签">
            <el-select v-model="form.tag_ids" multiple placeholder="选择标签" class="w-full" :teleported="false">
              <el-option v-for="tag in tags" :key="tag.id" :label="tag.name" :value="tag.id" />
            </el-select>
          </el-form-item>

          <div class="border-t border-[#e3e8ef] my-4"></div>

          <div class="text-[11px] font-semibold text-[#697386] uppercase tracking-wider mb-3">封面图</div>
          <el-form-item label="封面图 URL">
            <el-input v-model="form.cover_image" placeholder="https://..." />
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
