<template>
  <div class="auth-page">
    <div class="auth-card animate-fade-in">
      <div class="auth-logo">
        <span class="logo-icon">🎯</span>
        <h1>Talking Skills</h1>
        <p class="auth-subtitle">登录你的账号</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label>邮箱</label>
          <input
            v-model="email"
            type="email"
            class="input"
            placeholder="your@email.com"
            required
            autocomplete="email"
          />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input
            v-model="password"
            type="password"
            class="input"
            placeholder="输入密码"
            required
            autocomplete="current-password"
          />
        </div>

        <div v-if="error" class="error-msg">{{ error }}</div>

        <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
          {{ loading ? '登录中...' : '登 录' }}
        </button>
      </form>

      <div class="auth-footer">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth.js'

const router = useRouter()
const { login, loading } = useAuth()
const email = ref('')
const password = ref('')
const error = ref('')

async function handleLogin() {
  error.value = ''
  try {
    await login(email.value, password.value)
    router.push('/articles')
  } catch (e) {
    error.value = e.message
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-dark);
  padding: 20px;
}
.auth-card {
  width: 100%;
  max-width: 400px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 40px 32px;
}
.auth-logo {
  text-align: center;
  margin-bottom: 32px;
}
.auth-logo .logo-icon { font-size: 40px; }
.auth-logo h1 {
  font-size: 22px;
  font-weight: 700;
  margin-top: 8px;
  background: linear-gradient(135deg, var(--primary-light), #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.auth-subtitle {
  color: var(--text-muted);
  font-size: 14px;
  margin-top: 6px;
}
.auth-form { display: flex; flex-direction: column; gap: 18px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}
.btn-full { width: 100%; padding: 12px; font-size: 15px; margin-top: 8px; }
.error-msg {
  color: #ef4444;
  font-size: 13px;
  padding: 10px 14px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: var(--radius-sm);
}
.auth-footer {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
  color: var(--text-muted);
}
.auth-footer a {
  color: var(--primary-light);
  text-decoration: none;
  font-weight: 600;
}
.auth-footer a:hover { text-decoration: underline; }
</style>
