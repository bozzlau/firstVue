<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { adminGetPosts, adminDeletePost, adminRestorePost } from '../../api/posts'

const router = useRouter()
const posts = ref([])
const total = ref(0)
const loading = ref(false)
const page = ref(1)
const pageSize = ref(10)
const includeDeleted = ref(false)

async function load() {
  loading.value = true
  try {
    const data = await adminGetPosts({
      page: page.value,
      page_size: pageSize.value,
      include_deleted: includeDeleted.value,
    })
    posts.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

async function remove(id) {
  await adminDeletePost(id)
  load()
}

async function restore(id) {
  await adminRestorePost(id)
  load()
}

onMounted(load)
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-semibold text-gray-800">文章管理</h2>
      <div class="flex items-center gap-3">
        <el-checkbox v-model="includeDeleted" @change="load">显示已删除</el-checkbox>
        <el-button type="primary" @click="router.push('/admin/posts/new')">新建文章</el-button>
      </div>
    </div>

    <el-table :data="posts" v-loading="loading" border>
      <el-table-column prop="title" label="标题" show-overflow-tooltip>
        <template #default="{ row }">
          <span :class="row.deleted_at ? 'line-through text-gray-400' : ''">{{ row.title }}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag v-if="row.deleted_at" type="danger" size="small">已删除</el-tag>
          <el-tag v-else-if="row.published" type="success" size="small">已发布</el-tag>
          <el-tag v-else type="info" size="small">草稿</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="分类" width="100">
        <template #default="{ row }">{{ row.category?.name || '—' }}</template>
      </el-table-column>
      <el-table-column prop="views" label="浏览量" width="80" />
      <el-table-column label="创建时间" width="160">
        <template #default="{ row }">{{ new Date(row.created_at).toLocaleDateString('zh-CN') }}</template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <template v-if="!row.deleted_at">
            <el-button size="small" @click="router.push(`/admin/posts/${row.id}`)">编辑</el-button>
            <el-popconfirm title="确认删除？" @confirm="remove(row.id)">
              <template #reference>
                <el-button size="small" type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
          <el-button v-else size="small" type="warning" @click="restore(row.id)">恢复</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="mt-4 flex justify-end">
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @change="load"
      />
    </div>
  </div>
</template>
