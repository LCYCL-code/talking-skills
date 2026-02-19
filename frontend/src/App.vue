<template>
  <div class="app-wrapper">
    <!-- 侧边导航 -->
    <nav class="sidebar" v-if="!$route.meta.hideSidebar">
      <div class="sidebar-logo">
        <span class="logo-icon">💬</span>
        <span class="logo-text">别吵架</span>
      </div>

      <div class="sidebar-menu">
        <router-link to="/" class="menu-item" active-class="active" exact>
          <span class="menu-icon">🏠</span>
          <span>首页</span>
        </router-link>
        <router-link to="/articles" class="menu-item" active-class="active">
          <span class="menu-icon">📰</span>
          <span>读懂再说</span>
        </router-link>
        <router-link to="/upload" class="menu-item" active-class="active">
          <span class="menu-icon">🎤</span>
          <span>练自己的</span>
        </router-link>
        <router-link to="/hotspots" class="menu-item" active-class="active">
          <span class="menu-icon">🔥</span>
          <span>今日开吵</span>
        </router-link>
        <router-link to="/favorites" class="menu-item" active-class="active">
          <span class="menu-icon">⭐</span>
          <span>我的素材</span>
        </router-link>
        <router-link to="/read-later" class="menu-item" active-class="active">
          <span class="menu-icon">🔖</span>
          <span>待刷清单</span>
        </router-link>
      </div>

      <div class="sidebar-bottom">
        <router-link to="/settings" class="menu-item" active-class="active">
          <span class="menu-icon">⚙️</span>
          <span>设置</span>
        </router-link>

        <!-- 用户状态 -->
        <div v-if="user" class="user-card">
          <div class="user-avatar">{{ user.nickname?.[0] || '?' }}</div>
          <div class="user-info">
            <span class="user-name">{{ user.nickname }}</span>
            <button class="btn-logout" @click="handleLogout">登出</button>
          </div>
        </div>
        <router-link v-else to="/login" class="menu-item login-btn">
          <span class="menu-icon">👤</span>
          <span>登录 / 注册</span>
        </router-link>
      </div>
    </nav>

    <!-- 主内容区 -->
    <main class="main-content" :class="{ 'full-width': $route.meta.hideSidebar }">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 移动端底部导航 -->
    <nav class="bottom-nav" v-if="!$route.meta.hideSidebar">
      <router-link to="/" class="bottom-item" active-class="active" exact>
        <span>🏠</span><span>首页</span>
      </router-link>
      <router-link to="/articles" class="bottom-item" active-class="active">
        <span>📰</span><span>读懂</span>
      </router-link>
      <router-link to="/upload" class="bottom-item" active-class="active">
        <span>🎤</span><span>练自己</span>
      </router-link>
      <router-link to="/hotspots" class="bottom-item" active-class="active">
        <span>🔥</span><span>开吵</span>
      </router-link>
      <router-link to="/favorites" class="bottom-item" active-class="active">
        <span>⭐</span><span>素材</span>
      </router-link>
      <router-link to="/settings" class="bottom-item" active-class="active">
        <span>⚙️</span><span>设置</span>
      </router-link>
    </nav>

    <!-- Toast 通知 -->
    <teleport to="body">
      <div class="toast-container">
        <transition-group name="toast">
          <div
            v-for="toast in toasts"
            :key="toast.id"
            :class="['toast', `toast-${toast.type}`]"
          >{{ toast.message }}</div>
        </transition-group>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, provide, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from './composables/useAuth.js'

const router = useRouter()
const { user, fetchUser, logout } = useAuth()

onMounted(() => fetchUser())

async function handleLogout() {
  await logout()
  router.push('/login')
}

const toasts = ref([])

function showToast(message, type = 'info', duration = 3000) {
  const id = Date.now()
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }, duration)
}

provide('showToast', showToast)
</script>

<style scoped>
.app-wrapper {
  display: flex;
  min-height: 100vh;
}

/* ===== 侧边栏 ===== */
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: var(--nav-width);
  background: var(--bg-surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  padding: 0;
  z-index: 100;
  overflow: hidden;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 24px 20px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 12px;
}
.logo-icon { font-size: 24px; }
.logo-text {
  font-size: 16px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-light), #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.sidebar-menu { flex: 1; padding: 0 12px; }
.sidebar-bottom { padding: 12px; border-top: 1px solid var(--border); }

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 14px;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all var(--transition);
  margin-bottom: 4px;
}
.menu-item:hover { background: var(--bg-elevated); color: var(--text-primary); }
.menu-item.active {
  background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(79,70,229,0.15));
  color: var(--primary-light);
  border: 1px solid rgba(99,102,241,0.2);
}
.menu-icon { font-size: 18px; width: 22px; text-align: center; }

.sidebar-tip {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px;
  background: rgba(99,102,241,0.08);
  border-radius: var(--radius-sm);
  color: var(--text-muted);
  font-size: 11px;
  line-height: 1.5;
  margin-top: 8px;
}

/* ===== 主内容 ===== */
.main-content {
  margin-left: var(--nav-width);
  flex: 1;
  padding: 32px;
  min-height: 100vh;
}
.main-content.full-width { margin-left: 0; padding: 0; }

/* ===== 移动端底部导航 ===== */
.bottom-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--bg-surface);
  border-top: 1px solid var(--border);
  padding: 8px 0;
  z-index: 100;
}
.bottom-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  color: var(--text-muted);
  text-decoration: none;
  font-size: 11px;
  flex: 1;
  padding: 4px 0;
  transition: color var(--transition);
}
.bottom-item span:first-child { font-size: 20px; }
.bottom-item.active { color: var(--primary-light); }

/* ===== 页面切换动画 ===== */
.fade-enter-active, .fade-leave-active { transition: opacity 0.08s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* ===== Toast 动画 ===== */
.toast-enter-active, .toast-leave-active { transition: all 0.3s; }
.toast-enter-from { opacity: 0; transform: translateX(20px); }
.toast-leave-to { opacity: 0; transform: translateX(20px); }

/* ===== 用户卡片 ===== */
.user-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  margin-top: 8px;
  background: rgba(99,102,241,0.08);
  border-radius: var(--radius-sm);
}
.user-avatar {
  width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 14px; font-weight: 600;
}
.user-info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.user-name { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.btn-logout {
  background: none; border: none; color: var(--text-muted); font-size: 11px;
  cursor: pointer; padding: 0; text-align: left;
}
.btn-logout:hover { color: #ef4444; }
.login-btn {
  margin-top: 8px;
  background: rgba(99,102,241,0.1);
  border: 1px dashed rgba(99,102,241,0.3);
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .sidebar { display: none; }
  .bottom-nav { display: flex; }
  .main-content { margin-left: 0; padding: 20px 16px 80px; }
}
</style>
