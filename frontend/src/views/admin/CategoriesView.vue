<script setup>
import { ref, onMounted } from 'vue'
import {
  adminGetCategories,
  adminCreateCategory,
  adminUpdateCategory,
  adminDeleteCategory,
} from '../../api/categories'

const categories = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const editing = ref(null)
const form = ref({ name: '', slug: '', description: '' })

async function load() {
  loading.value = true
  try {
    categories.value = await adminGetCategories()
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editing.value = null
  form.value = { name: '', slug: '', description: '' }
  dialogVisible.value = true
}

function openEdit(row) {
  editing.value = row
  form.value = { name: row.name, slug: row.slug, description: row.description || '' }
  dialogVisible.value = true
}

async function save() {
  if (editing.value) {
    await adminUpdateCategory(editing.value.id, form.value)
  } else {
    await adminCreateCategory(form.value)
  }
  dialogVisible.value = false
  load()
}

async function remove(id) {
  await adminDeleteCategory(id)
  load()
}

onMounted(load)
</script>

<template>
  <div>
    <div class="sticky top-0 z-10 bg-white border-b border-[#e3e8ef] px-7 h-14 flex items-center justify-between">
      <span class="text-[15px] font-semibold text-[#1a1f36]">分类管理</span>
      <el-button type="primary" size="small" @click="openCreate">+ 新建分类</el-button>
    </div>

    <div class="p-7">
      <div class="bg-white border border-[#e3e8ef] rounded-lg overflow-hidden">
        <el-table :data="categories" v-loading="loading" :border="false" style="width:100%">
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="slug" label="Slug" />
          <el-table-column prop="description" label="描述" show-overflow-tooltip />
          <el-table-column label="操作" width="140">
            <template #default="{ row }">
              <button
                class="inline-flex items-center px-2.5 py-1 rounded text-[12px] font-medium border border-[#c7c4ff] text-[#635bff] bg-white hover:bg-[#f0effe] transition-colors mr-1.5"
                @click="openEdit(row)"
              >编辑</button>
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

    <el-dialog v-model="dialogVisible" :title="editing ? '编辑分类' : '新建分类'" width="400px" :teleported="false">
      <el-form :model="form" label-position="top">
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="Slug"><el-input v-model="form.slug" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>
