<script setup>
import { ref, onMounted } from 'vue'
import { adminGetTags, adminCreateTag, adminUpdateTag, adminDeleteTag } from '../../api/tags'

const tags = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const editing = ref(null)
const form = ref({ name: '', slug: '' })

async function load() {
  loading.value = true
  try {
    tags.value = await adminGetTags()
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editing.value = null
  form.value = { name: '', slug: '' }
  dialogVisible.value = true
}

function openEdit(row) {
  editing.value = row
  form.value = { name: row.name, slug: row.slug }
  dialogVisible.value = true
}

async function save() {
  if (editing.value) {
    await adminUpdateTag(editing.value.id, form.value)
  } else {
    await adminCreateTag(form.value)
  }
  dialogVisible.value = false
  load()
}

async function remove(id) {
  await adminDeleteTag(id)
  load()
}

onMounted(load)
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-semibold text-gray-800">标签管理</h2>
      <el-button type="primary" @click="openCreate">新建标签</el-button>
    </div>

    <el-table :data="tags" v-loading="loading" border>
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="slug" label="Slug" />
      <el-table-column label="操作" width="140">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-popconfirm title="确认删除？" @confirm="remove(row.id)">
            <template #reference>
              <el-button size="small" type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="editing ? '编辑标签' : '新建标签'" width="360px">
      <el-form :model="form" label-position="top">
        <el-form-item label="名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="Slug">
          <el-input v-model="form.slug" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>
