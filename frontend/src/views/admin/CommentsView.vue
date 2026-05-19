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
    <div class="sticky top-0 z-10 bg-white border-b border-[#e3e8ef] px-7 h-14 flex items-center justify-between">
      <span class="text-[15px] font-semibold text-[#1a1f36]">评论管理</span>
      <!-- Tab filter -->
      <div class="flex rounded-md border border-[#e3e8ef] overflow-hidden">
        <button
          v-for="opt in [{value:'all',label:'全部'},{value:'pending',label:'待审核'},{value:'approved',label:'已通过'}]"
          :key="opt.value"
          class="px-3 py-1.5 text-[12.5px] font-medium transition-colors"
          :class="filter === opt.value
            ? 'bg-[#635bff] text-white'
            : 'bg-white text-[#697386] hover:bg-[#f6f9fc]'"
          @click="filter = opt.value"
        >{{ opt.label }}</button>
      </div>
    </div>

    <div class="p-7">
      <div class="bg-white border border-[#e3e8ef] rounded-lg overflow-hidden">
        <el-table :data="filtered()" v-loading="loading" :border="false" style="width:100%">
          <el-table-column prop="author_name" label="作者" width="100" />
          <el-table-column prop="author_email" label="邮箱" width="180" show-overflow-tooltip />
          <el-table-column prop="content" label="内容" show-overflow-tooltip />
          <el-table-column prop="post_id" label="文章ID" width="80" />
          <el-table-column label="状态" width="90">
            <template #default="{ row }">
              <span v-if="row.approved" class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11.5px] font-medium bg-[#e6f9f2] text-[#09b57a]">
                <span class="w-1.5 h-1.5 rounded-full bg-[#09b57a]"></span>已通过
              </span>
              <span v-else class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11.5px] font-medium bg-[#fff4e6] text-[#f59e0b]">
                <span class="w-1.5 h-1.5 rounded-full bg-[#f59e0b]"></span>待审核
              </span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="160">
            <template #default="{ row }">
              <button
                v-if="!row.approved"
                class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#a7f3d0] text-[#09b57a] bg-white hover:bg-[#f0fdf9] transition-colors mr-1.5"
                @click="approve(row.id)"
              >通过</button>
              <el-popconfirm title="确认删除？" @confirm="remove(row.id)" :teleported="false">
                <template #reference>
                  <button class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#fecaca] text-[#e53e3e] bg-white hover:bg-[#fff5f5] transition-colors">删除</button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>
