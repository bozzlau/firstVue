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
    <!-- Topbar -->
    <div class="sticky top-0 z-10 bg-white border-b border-[#e3e8ef] px-7 h-14 flex items-center justify-between">
      <span class="text-[15px] font-semibold text-[#1a1f36]">文章管理</span>
      <el-button type="primary" size="small" @click="router.push('/admin/posts/new')">+ 新建文章</el-button>
    </div>

    <div class="p-7">
      <!-- Toolbar -->
      <div class="flex items-center gap-3 mb-4">
        <el-input
          placeholder="搜索文章…"
          style="max-width: 260px"
          clearable
        />
        <el-checkbox v-model="includeDeleted" @change="load">显示已删除</el-checkbox>
      </div>

      <!-- Table card -->
      <div class="bg-white border border-[#e3e8ef] rounded-lg overflow-hidden">
        <el-table
          :data="posts"
          v-loading="loading"
          :border="false"
          style="width: 100%"
        >
          <el-table-column prop="title" label="标题" show-overflow-tooltip>
            <template #default="{ row }">
              <span :class="row.deleted_at ? 'line-through text-[#aab7c4]' : 'text-[#1a1f36]'">{{ row.title }}</span>
              <div class="text-[11px] text-[#697386] mt-0.5">{{ row.slug }}</div>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <span v-if="row.deleted_at" class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11.5px] font-medium bg-[#f0f4f8] text-[#697386]">
                <span class="w-1.5 h-1.5 rounded-full bg-[#aab7c4]"></span>已删除
              </span>
              <span v-else-if="row.published" class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11.5px] font-medium bg-[#e6f9f2] text-[#09b57a]">
                <span class="w-1.5 h-1.5 rounded-full bg-[#09b57a]"></span>已发布
              </span>
              <span v-else class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11.5px] font-medium bg-[#fff4e6] text-[#f59e0b]">
                <span class="w-1.5 h-1.5 rounded-full bg-[#f59e0b]"></span>草稿
              </span>
            </template>
          </el-table-column>
          <el-table-column label="分类" width="100">
            <template #default="{ row }">
              <span class="text-[13px] text-[#697386]">{{ row.category?.name || '—' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="views" label="浏览量" width="80">
            <template #default="{ row }">
              <span class="text-[13px] text-[#697386]">{{ row.views }}</span>
            </template>
          </el-table-column>
          <el-table-column label="创建时间" width="120">
            <template #default="{ row }">
              <span class="text-[13px] text-[#697386]">{{ new Date(row.created_at).toLocaleDateString('zh-CN') }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="160">
            <template #default="{ row }">
              <template v-if="!row.deleted_at">
                <button
                  class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#c7c4ff] text-[#635bff] bg-white hover:bg-[#f0effe] transition-colors mr-1.5"
                  @click="router.push(`/admin/posts/${row.id}`)"
                >编辑</button>
                <el-popconfirm title="确认删除？" @confirm="remove(row.id)" :teleported="false">
                  <template #reference>
                    <button class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#fecaca] text-[#e53e3e] bg-white hover:bg-[#fff5f5] transition-colors">删除</button>
                  </template>
                </el-popconfirm>
              </template>
              <button
                v-else
                class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#a7f3d0] text-[#09b57a] bg-white hover:bg-[#f0fdf9] transition-colors"
                @click="restore(row.id)"
              >恢复</button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- Pagination -->
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
  </div>
</template>
