<template>
  <div class="favorites-page animate-fade-in">
    <div class="page-header">
      <h1>我的收藏</h1>
    </div>

    <div v-if="loading" class="article-grid">
      <div v-for="i in 4" :key="i" class="card">
        <div class="skeleton" style="width:80px;height:20px;margin-bottom:12px;"></div>
        <div class="skeleton" style="width:100%;height:22px;margin-bottom:8px;"></div>
        <div class="skeleton" style="width:100%;height:60px;"></div>
      </div>
    </div>

    <div v-else-if="articles.length" class="article-grid">
      <div
        v-for="a in articles"
        :key="a.id"
        class="article-card card card-clickable"
        @click="$router.push(`/articles/${a.id}`)"
      >
        <div class="card-tags">
          <span class="tag" :class="`cat-${a.category}`">{{ a.category }}</span>
          <span class="tag source-tag">{{ a.source }}</span>
          <span class="article-date">{{ a.published_at }}</span>
        </div>
        <h3 class="article-title">{{ a.title }}</h3>
        <p class="article-summary">{{ a.summary }}</p>
        <div class="card-actions">
          <button class="btn btn-primary btn-sm" @click.stop="$router.push(`/articles/${a.id}`)">阅读并练习</button>
          <button class="btn btn-danger btn-sm" @click.stop="removeFav(a)">取消收藏</button>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <div class="icon">⭐</div>
      <p>暂无收藏内容</p>
      <button class="btn btn-primary" style="margin-top:16px;" @click="$router.push('/articles')">去浏览文章</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { api } from '../api/index.js'

const showToast = inject('showToast')
const articles = ref([])
const loading = ref(true)

async function loadFavorites() {
  loading.value = true
  try { articles.value = await api.getFavorites() } catch (e) { showToast('加载失败', 'error') }
  finally { loading.value = false }
}

async function removeFav(a) {
  try {
    await api.toggleFavorite(a.id)
    showToast('已取消收藏', 'success')
    articles.value = articles.value.filter((x) => x.id !== a.id)
  } catch (e) { showToast('操作失败', 'error') }
}

onMounted(loadFavorites)
</script>

<style scoped>
.article-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 18px; }
.article-card { display: flex; flex-direction: column; gap: 10px; }
.card-tags { display: flex; align-items: center; flex-wrap: wrap; gap: 6px; }
.source-tag { background: rgba(99,102,241,0.3); }
.article-date { margin-left: auto; font-size: 12px; color: var(--text-muted); }
.article-title { font-size: 16px; font-weight: 600; line-height: 1.5; }
.article-summary { font-size: 13px; color: var(--text-secondary); line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; flex: 1; }
.card-actions { display: flex; gap: 8px; margin-top: auto; }
</style>
