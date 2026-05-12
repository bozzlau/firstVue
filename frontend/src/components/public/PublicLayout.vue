<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getCategories } from '../../api/categories'
import { getTags } from '../../api/tags'

const router = useRouter()
const route = useRoute()
const categories = ref([])
const tags = ref([])
const searchQ = ref('')

onMounted(async () => {
  const [cats, tgs] = await Promise.all([getCategories(), getTags()])
  categories.value = cats
  tags.value = tgs
})

function doSearch() {
  if (searchQ.value.trim()) {
    router.push({ path: '/search', query: { q: searchQ.value.trim() } })
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
        <router-link to="/" class="font-bold text-gray-900 text-lg no-underline">我的博客</router-link>

        <div class="flex items-center gap-4">
          <form @submit.prevent="doSearch" class="flex">
            <input
              v-model="searchQ"
              type="text"
              placeholder="搜索文章..."
              class="border border-gray-200 rounded-l px-3 py-1.5 text-sm outline-none focus:border-blue-400 w-40"
            />
            <button
              type="submit"
              class="bg-blue-500 text-white px-3 py-1.5 rounded-r text-sm hover:bg-blue-600"
            >
              搜索
            </button>
          </form>
          <router-link to="/about" class="text-sm text-gray-600 hover:text-gray-900 no-underline">关于</router-link>
        </div>
      </div>
    </nav>

    <div class="max-w-5xl mx-auto px-4 py-8 flex gap-8">
      <main class="flex-1 min-w-0">
        <RouterView />
      </main>

      <aside class="w-56 shrink-0 space-y-6">
        <div v-if="categories.length">
          <h3 class="text-sm font-semibold text-gray-700 mb-3">分类</h3>
          <ul class="space-y-1">
            <li v-for="cat in categories" :key="cat.id">
              <router-link
                :to="`/category/${cat.slug}`"
                class="text-sm text-gray-600 hover:text-blue-600 no-underline"
                :class="route.params.slug === cat.slug ? 'text-blue-600 font-medium' : ''"
              >
                {{ cat.name }}
              </router-link>
            </li>
          </ul>
        </div>

        <div v-if="tags.length">
          <h3 class="text-sm font-semibold text-gray-700 mb-3">标签</h3>
          <div class="flex flex-wrap gap-2">
            <router-link
              v-for="tag in tags"
              :key="tag.id"
              :to="`/tag/${tag.slug}`"
              class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded hover:bg-blue-50 hover:text-blue-600 no-underline"
            >
              {{ tag.name }}
            </router-link>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>
