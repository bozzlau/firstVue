<script setup>
import { useRouter } from 'vue-router'

defineProps({
  post: { type: Object, required: true },
})

const router = useRouter()
</script>

<template>
  <article
    class="bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
    @click="router.push(`/posts/${post.slug}`)"
  >
    <img
      v-if="post.cover_image"
      :src="post.cover_image"
      :alt="post.title"
      class="w-full h-48 object-cover"
    />
    <div class="p-5">
      <div class="flex items-center gap-2 mb-2 flex-wrap">
        <span
          v-if="post.category"
          class="text-xs bg-blue-50 text-blue-600 px-2 py-0.5 rounded-full"
        >
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

      <h2 class="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">{{ post.title }}</h2>
      <p v-if="post.summary" class="text-gray-500 text-sm line-clamp-3 mb-3">{{ post.summary }}</p>

      <div class="flex items-center justify-between text-xs text-gray-400">
        <span>{{ new Date(post.created_at).toLocaleDateString('zh-CN') }}</span>
        <span>{{ post.views }} 次阅读</span>
      </div>
    </div>
  </article>
</template>
