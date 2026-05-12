<script setup>
import { ref, onMounted } from 'vue'
import { adminGetComments, adminUpdateComment, adminDeleteComment } from '../../api/comments'

const comments = ref([])
const loading = ref(false)
const filter = ref('all')

async function load() {
  loading.value = true
  try {
    comments.value = await adminGetComments()
  } finally {
    loading.value = false
  }
}

const filtered = () => {
  if (filter.value === 'pending') return comments.value.filter((c) => !c.approved)
  if (filter.value === 'approved') return comments.value.filter((c) => c.approved)
  return comments.value
}

async function approve(id) {
  await adminUpdateComment(id, { approved: true })
  load()
}

async function remove(id) {
  await adminDeleteComment(id)
  load()
}

onMounted(load)
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-semibold text-gray-800">评论管理</h2>
      <el-radio-group v-model="filter">
        <el-radio-button value="all">全部</el-radio-button>
        <el-radio-button value="pending">待审核</el-radio-button>
        <el-radio-button value="approved">已通过</el-radio-button>
      </el-radio-group>
    </div>

    <el-table :data="filtered()" v-loading="loading" border>
      <el-table-column prop="author_name" label="作者" width="100" />
      <el-table-column prop="author_email" label="邮箱" width="180" show-overflow-tooltip />
      <el-table-column prop="content" label="内容" show-overflow-tooltip />
      <el-table-column prop="post_id" label="文章ID" width="80" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.approved ? 'success' : 'warning'" size="small">
            {{ row.approved ? '已通过' : '待审核' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button
            v-if="!row.approved"
            size="small"
            type="success"
            @click="approve(row.id)"
          >
            通过
          </el-button>
          <el-popconfirm title="确认删除？" @confirm="remove(row.id)">
            <template #reference>
              <el-button size="small" type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
