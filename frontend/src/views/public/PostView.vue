<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import { getPost } from '../../api/posts'
import { getComments, createComment } from '../../api/comments'

const route = useRoute()
const post = ref(null)
const comments = ref([])
const loading = ref(true)
const commentForm = ref({ author_name: '', author_email: '', content: '' })
const submitting = ref(false)
const submitted = ref(false)

async function load() {
  loading.value = true
  submitted.value = false
  try {
    const [p, c] = await Promise.all([
      getPost(route.params.slug),
      getComments(route.params.slug),
    ])
    post.value = p
    comments.value = c
  } finally {
    loading.value = false
  }
}

async function submitComment() {
  submitting.value = true
  try {
    await createComment(route.params.slug, commentForm.value)
    commentForm.value = { author_name: '', author_email: '', content: '' }
    submitted.value = true
  } finally {
    submitting.value = false
  }
}

onMounted(load)
watch(() => route.params.slug, load)
</script>

<template>
  <div>
    <div v-if="loading" class="text-center py-12 text-gray-400">加载中...</div>

    <article v-else-if="post">
      <img
        v-if="post.cover_image"
        :src="post.cover_image"
        :alt="post.title"
        class="w-full h-64 object-cover rounded-lg mb-6"
      />

      <div class="flex items-center gap-2 mb-3 flex-wrap">
        <span v-if="post.category" class="text-xs bg-blue-50 text-blue-600 px-2 py-0.5 rounded-full">
          {{ post.category.name }}
        </span>
        <span
          v-for="tag in post.tags"
          :key="tag.id"
          class="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded-full"
        >
          {{ tag.name }}
        </span>
      </div>

      <h1 class="text-3xl font-bold text-gray-900 mb-3">{{ post.title }}</h1>

      <div class="flex items-center gap-4 text-sm text-gray-400 mb-8 pb-6 border-b">
        <span>{{ new Date(post.created_at).toLocaleDateString('zh-CN') }}</span>
        <span>{{ post.views }} 次阅读</span>
      </div>

      <div
        class="prose prose-gray max-w-none"
        v-html="marked(post.content)"
      />

      <!-- 评论区 -->
      <section class="mt-12 pt-8 border-t">
        <h2 class="text-xl font-semibold text-gray-800 mb-6">
          评论 <span class="text-sm font-normal text-gray-400">{{ comments.length }} 条</span>
        </h2>

        <div v-if="comments.length === 0" class="text-gray-400 text-sm mb-8">暂无评论</div>
        <div v-else class="space-y-4 mb-8">
          <div
            v-for="c in comments"
            :key="c.id"
            class="bg-gray-50 rounded-lg p-4"
          >
            <div class="flex items-center justify-between mb-2">
              <span class="font-medium text-gray-700 text-sm">{{ c.author_name }}</span>
              <span class="text-xs text-gray-400">{{ new Date(c.created_at).toLocaleDateString('zh-CN') }}</span>
            </div>
            <p class="text-gray-600 text-sm">{{ c.content }}</p>
          </div>
        </div>

        <div v-if="submitted" class="bg-green-50 text-green-700 text-sm rounded p-3 mb-4">
          评论已提交，等待审核后显示。
        </div>

        <form v-else @submit.prevent="submitComment" class="space-y-3">
          <h3 class="text-base font-medium text-gray-700">发表评论</h3>
          <div class="grid grid-cols-2 gap-3">
            <input
              v-model="commentForm.author_name"
              required
              placeholder="姓名"
              class="border border-gray-200 rounded px-3 py-2 text-sm outline-none focus:border-blue-400"
            />
            <input
              v-model="commentForm.author_email"
              required
              type="email"
              placeholder="邮箱（不公开）"
              class="border border-gray-200 rounded px-3 py-2 text-sm outline-none focus:border-blue-400"
            />
          </div>
          <textarea
            v-model="commentForm.content"
            required
            placeholder="写下你的评论..."
            rows="4"
            class="w-full border border-gray-200 rounded px-3 py-2 text-sm outline-none focus:border-blue-400 resize-none"
          />
          <button
            type="submit"
            :disabled="submitting"
            class="bg-blue-500 text-white px-4 py-2 rounded text-sm hover:bg-blue-600 disabled:opacity-50"
          >
            {{ submitting ? '提交中...' : '提交评论' }}
          </button>
        </form>
      </section>
    </article>
  </div>
</template>
