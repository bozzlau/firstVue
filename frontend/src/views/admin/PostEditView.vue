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
  <div v-loading="loading">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-semibold text-gray-800">{{ isEdit ? '编辑文章' : '新建文章' }}</h2>
      <div class="flex gap-2">
        <el-button @click="router.push('/admin/posts')">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </div>
    </div>

    <el-form :model="form" label-position="top">
      <div class="grid grid-cols-3 gap-4">
        <div class="col-span-2 space-y-4">
          <el-form-item label="标题">
            <el-input v-model="form.title" />
          </el-form-item>
          <el-form-item label="Slug（URL 路径）">
            <el-input v-model="form.slug" />
          </el-form-item>
          <el-form-item label="摘要">
            <el-input v-model="form.summary" type="textarea" :rows="2" />
          </el-form-item>
          <el-form-item label="正文">
            <MdEditor v-model="form.content" style="height: 500px" />
          </el-form-item>
        </div>

        <div class="space-y-4">
          <el-form-item label="发布状态">
            <el-switch v-model="form.published" active-text="已发布" inactive-text="草稿" />
          </el-form-item>
          <el-form-item label="分类">
            <el-select v-model="form.category_id" clearable placeholder="选择分类" class="w-full">
              <el-option
                v-for="cat in categories"
                :key="cat.id"
                :label="cat.name"
                :value="cat.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="标签">
            <el-select v-model="form.tag_ids" multiple placeholder="选择标签" class="w-full">
              <el-option
                v-for="tag in tags"
                :key="tag.id"
                :label="tag.name"
                :value="tag.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="封面图 URL">
            <el-input v-model="form.cover_image" placeholder="https://..." />
          </el-form-item>
        </div>
      </div>
    </el-form>
  </div>
</template>
