import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePostStore = defineStore('post', () => {
  const posts = ref([])
  const currentPost = ref(null)
  const total = ref(0)

  function setPosts(data) {
    posts.value = data.items
    total.value = data.total
  }

  function setCurrentPost(post) {
    currentPost.value = post
  }

  function clear() {
    posts.value = []
    currentPost.value = null
    total.value = 0
  }

  return { posts, currentPost, total, setPosts, setCurrentPost, clear }
})
