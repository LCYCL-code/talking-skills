<template>
  <div class="read-later-page animate-fade-in">
    <div class="page-header">
      <div>
        <h1 class="page-title">🔖 稍后再看</h1>
        <p class="page-subtitle">您保存的文章，随时继续阅读</p>
      </div>
    </div>

    <div v-if="loading" class="article-grid">
      <div v-for="n in 4" :key="n" class="card skeleton-card">
        <div class="skeleton" style="width:50%;height:12px;margin-bottom:12px;"></div>
        <div class="skeleton" style="width:90%;height:18px;margin-bottom:8px;"></div>
        <div class="skeleton" style="width:100%;height:14px;"></div>
      </div>
    </div>

    <div v-else-if="!articles.length" class="empty-state">
      <div class="empty-icon">🔖</div>
      <p class="empty-text">还没有保存任何文章</p>
      <p class="empty-hint">在文章列表点击 🔖 书签按钮即可保存</p>
      <router-link to="/articles" class="btn btn-primary" style="margin-top:16px;">去浏览文章</router-link>
    </div>

    <div v-else class="article-grid">
      <div
        v-for="article in articles"
        :key="article.id"
        class="article-card card"
        @click="goToArticle(article)"
      >
        <span v-if="!article.is_read" class="unread-dot"></span>

        <div class="card-top">
          <div class="card-tags">
            <span class="tag" :class="`cat-${article.category}`">{{ article.category }}</span>
            <span class="tag type-tag" :class="`type-${article.content_type || '文章'}`">
              {{ article.content_type || '文章' }}
            </span>
          </div>
          <button
            class="bookmark-btn bookmarked"
            @click.stop="removeReadLater(article)"
            title="移除"
          >🔖</button>
        </div>

        <h3 class="card-title">{{ article.title }}</h3>
        <p class="card-summary">{{ article.summary }}</p>

        <div class="card-footer">
          <span class="meta-source">{{ article.source }}</span>
          <span class="meta-dot">·</span>
          <span class="meta-date">{{ article.published_at }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api/index.js'

const router = useRouter()
const showToast = inject('showToast')

const articles = ref([])
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    articles.value = await api.getReadLater()
  } catch (e) {
    showToast('加载失败', 'error')
  } finally {
    loading.value = false
  }
}

async function removeReadLater(article) {
  try {
    await api.toggleReadLater(article.id)
    articles.value = articles.value.filter(a => a.id !== article.id)
    showToast('已移除', 'success')
  } catch (e) {
    showToast('操作失败', 'error')
  }
}

function goToArticle(article) {
  article.is_read = 1
  router.push(`/articles/${article.id}`)
}

onMounted(load)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.page-title { font-size: 24px; font-weight: 700; margin-bottom: 4px; }
.page-subtitle { color: var(--text-muted); font-size: 14px; }
.article-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
.article-card { position: relative; cursor: pointer; border: 1px solid var(--border); transition: transform var(--transition), box-shadow var(--transition); }
.article-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
.unread-dot { position: absolute; top: 12px; right: 12px; width: 8px; height: 8px; border-radius: 50%; background: #ef4444; box-shadow: 0 0 6px rgba(239,68,68,0.5); }
.card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.card-tags { display: flex; gap: 6px; }
.type-tag { font-size: 11px; }
.type-文章 { background: rgba(99,102,241,0.2); color: var(--primary-light); }
.type-简讯 { background: rgba(16,185,129,0.2); color: #34d399; }
.bookmark-btn { background: none; border: none; cursor: pointer; font-size: 16px; padding: 2px 4px; border-radius: 4px; opacity: 1; transition: opacity 0.15s; filter: hue-rotate(200deg) saturate(2); }
.bookmark-btn:hover { opacity: 0.6; }
.card-title { font-size: 15px; font-weight: 600; line-height: 1.5; margin-bottom: 8px; color: var(--text-primary); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.card-summary { font-size: 13px; color: var(--text-muted); line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 16px; }
.card-footer { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--text-muted); }
.skeleton-card { min-height: 160px; }
.empty-state { text-align: center; padding: 80px 20px; }
.empty-icon { font-size: 56px; margin-bottom: 16px; }
.empty-text { color: var(--text-secondary); font-size: 16px; margin-bottom: 8px; }
.empty-hint { color: var(--text-muted); font-size: 13px; }
</style>
