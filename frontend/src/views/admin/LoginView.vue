<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = ref({ username: '', password: '' })
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(form.value.username, form.value.password)
    router.push('/admin/dashboard')
  } catch {
    error.value = '用户名或密码错误'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="admin-scope min-h-screen bg-[#f6f9fc] flex items-center justify-center px-4">
    <div class="w-full max-w-sm">
      <!-- Card -->
      <div class="bg-white border border-[#e3e8ef] rounded-[10px] shadow-[0_4px_24px_rgba(0,0,0,0.08)] px-8 py-8">
        <!-- Logo + Title -->
        <div class="flex items-center gap-3 mb-6">
          <div class="w-8 h-8 rounded-lg bg-[#635bff] flex items-center justify-center text-white font-bold text-base shrink-0">B</div>
          <div>
            <div class="text-base font-semibold text-[#1a1f36]">博客管理后台</div>
            <div class="text-[12px] text-[#697386]">请使用管理员账号登录</div>
          </div>
        </div>

        <el-form :model="form" @submit.prevent="handleLogin" label-position="top">
          <el-form-item label="用户名">
            <el-input v-model="form.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              show-password
            />
          </el-form-item>

          <el-alert
            v-if="error"
            :title="error"
            type="error"
            show-icon
            :closable="false"
            class="mb-4"
          />

          <el-button
            type="primary"
            native-type="submit"
            :loading="loading"
            class="w-full !mt-2"
          >
            登录
          </el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>
