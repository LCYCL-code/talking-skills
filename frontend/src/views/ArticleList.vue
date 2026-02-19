<template>
  <div class="article-list-page animate-fade-in">
    <div class="page-header">
      <div>
        <h1 class="page-title">读懂再说</h1>
        <p class="page-subtitle">读完一篇，用自己的话复述一遍。不能复述的，叫做「没看懂」。</p>
      </div>
      <div class="header-actions">
        <div class="status-toggle">
          <button
            v-for="s in readStatuses"
            :key="s"
            :class="['status-btn', { active: activeStatus === s }]"
            @click="setStatus(s)"
          >{{ s }}</button>
        </div>
        <div class="vertical-divider"></div>
        <button class="btn btn-ghost" @click="showRssModal = true">➕ 订阅</button>
        <button class="btn btn-primary" :disabled="refreshing" @click="refresh">
          <span v-if="refreshing" class="spin">⟳</span>
          {{ refreshing ? '刷新中...' : '刷新内容' }}
        </button>
      </div>
    </div>

    <RssModal :show="showRssModal" @close="showRssModal = false" />

    <!-- 第一行：内容类型 -->
    <div class="filter-row">
      <button
        v-for="t in contentTypes"
        :key="t"
        :class="['filter-btn', { active: activeType === t }]"
        @click="setType(t)"
      >{{ t }}</button>
    </div>

    <!-- 第二行：话题分类 -->
    <div class="filter-row filter-row-secondary">
      <button
        v-for="cat in categories"
        :key="cat"
        :class="['filter-btn filter-btn-sm', { active: activeCategory === cat }]"
        @click="setCategory(cat)"
      >{{ cat }}</button>
    </div>

    <!-- 结果统计 -->
    <div v-if="!loading" class="result-count">
      共 {{ articles.length }} 篇，其中 {{ unreadCount }} 篇未读
    </div>

    <!-- 加载骨架 -->
    <div v-if="loading" class="article-grid">
      <div v-for="n in 6" :key="n" class="card skeleton-card">
        <div class="skeleton" style="width:50%;height:12px;margin-bottom:12px;"></div>
        <div class="skeleton" style="width:90%;height:18px;margin-bottom:8px;"></div>
        <div class="skeleton" style="width:100%;height:14px;margin-bottom:6px;"></div>
        <div class="skeleton" style="width:70%;height:14px;"></div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else-if="!articles.length" class="empty-state">
      <div class="empty-icon">📭</div>
      <p class="empty-text">暂无文章，请点击刷新按钮获取内容</p>
      <button class="btn btn-primary" @click="refresh">立即刷新</button>
    </div>

    <!-- 文章卡片 -->
    <div v-else class="article-grid">
      <div
        v-for="article in articles"
        :key="article.id"
        class="article-card card"
        @click="goToArticle(article)"
      >
        <!-- 未读红点 -->
        <span v-if="!article.is_read" class="unread-dot"></span>

        <div class="card-top">
          <div class="card-tags">
            <span class="tag" :class="`cat-${article.category}`">{{ article.category }}</span>
            <span class="tag type-tag" :class="`type-${article.content_type || '文章'}`">
              {{ article.content_type || '文章' }}
            </span>
          </div>
          <span class="meta-source-top">{{ article.source }}</span>
        </div>

        <h3 class="card-title">{{ article.title }}</h3>
        <p class="card-summary">{{ article.summary }}</p>

        <div class="card-footer">
          <span class="meta-date">{{ article.published_at }}</span>
          <div class="card-actions">
            <button
              :class="['action-btn bookmark-btn', { active: article.read_later }]"
              @click.stop="toggleReadLater(article)"
              :title="article.read_later ? '取消稍后再看' : '稍后再看'"
            >🔖</button>
            <button
              :class="['action-btn fav-btn', { active: article.is_favorite }]"
              @click.stop="toggleFav(article)"
              :title="article.is_favorite ? '取消收藏' : '收藏'"
            >{{ article.is_favorite ? '⭐' : '☆' }}</button>
            <button
              class="action-btn del-btn"
              @click.stop="deleteCard(article)"
              title="删除"
            >🗑</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api/index.js'
import RssModal from '../components/RssModal.vue'

const router = useRouter()
const showToast = inject('showToast')

const showRssModal = ref(false)

const articles = ref([])
const loading = ref(false)
const refreshing = ref(false)

const contentTypes = ['全部', '文章', '简讯', '博客', '播客', '视频']
const readStatuses = ['全部', '未读', '已读']
const categories = ['全部', 'AI', '科技', '金融', '商业', '安全', '文化']

const activeType = ref('全部')
const activeStatus = ref('全部')
const activeCategory = ref('全部')

const unreadCount = computed(() => articles.value.filter(a => !a.is_read).length)

async function loadArticles() {
  loading.value = true
  try {
    articles.value = await api.getArticles(activeCategory.value, activeType.value, activeStatus.value)
  } catch (e) {
    showToast('加载失败：' + e.message, 'error')
  } finally {
    loading.value = false
  }
}

function setType(t) { activeType.value = t; loadArticles() }
function setStatus(s) { activeStatus.value = s; loadArticles() }
function setCategory(cat) { activeCategory.value = cat; loadArticles() }

async function refresh() {
  refreshing.value = true
  try {
    const result = await api.refreshArticles()
    showToast(result.message, 'success')
    await loadArticles()
  } catch (e) {
    showToast('刷新失败：' + e.message, 'error')
  } finally {
    refreshing.value = false
  }
}

async function toggleFav(article) {
  try {
    const result = await api.toggleFavorite(article.id)
    article.is_favorite = result.is_favorite ? 1 : 0
    showToast(article.is_favorite ? '已收藏' : '已取消收藏', 'success')
  } catch (e) {
    showToast('操作失败', 'error')
  }
}

async function toggleReadLater(article) {
  try {
    const result = await api.toggleReadLater(article.id)
    article.read_later = result.read_later ? 1 : 0
    showToast(article.read_later ? '已加入稍后再看' : '已移除', 'success')
  } catch (e) {
    showToast('操作失败', 'error')
  }
}

async function deleteCard(article) {
  if (!confirm(`确则删除《${article.title}》？`)) return
  try {
    await api.deleteArticle(article.id)
    articles.value = articles.value.filter(a => a.id !== article.id)
    showToast('已删除', 'success')
  } catch {
    showToast('删除失败', 'error')
  }
}

function goToArticle(article) {
  article.is_read = 1  // 乐观更新
  router.push(`/articles/${article.id}`)
}

onMounted(loadArticles)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
.page-title { font-size: 24px; font-weight: 700; margin-bottom: 4px; }
.page-subtitle { color: var(--text-muted); font-size: 14px; }
.header-actions { display: flex; gap: 10px; align-items: center; }
.status-toggle {
  display: flex; background: var(--bg-surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 2px;
}
.status-btn {
  background: none; border: none; padding: 4px 12px; font-size: 13px; color: var(--text-secondary);
  border-radius: 6px; cursor: pointer; transition: all 0.2s;
}
.status-btn:hover { color: var(--text-primary); }
.status-btn.active { background: var(--primary); color: #fff; font-weight: 500; }
.vertical-divider { width: 1px; height: 18px; background: var(--border); margin: 0 4px; }

.filter-row { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; }
.filter-btn {
  padding: 7px 16px; border-radius: 20px; border: 1px solid var(--border);
  background: transparent; color: var(--text-secondary); cursor: pointer;
  font-size: 14px; font-weight: 500; transition: all var(--transition);
}
.filter-btn:hover { border-color: var(--primary); color: var(--primary-light); }
.filter-btn.active { background: var(--primary); color: #fff; border-color: var(--primary); }
.filter-btn-sm { padding: 5px 14px; font-size: 13px; }

.result-count { font-size: 13px; color: var(--text-muted); margin-bottom: 16px; }

.article-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }

.article-card {
  position: relative; cursor: pointer;
  display: flex; flex-direction: column;
  transition: transform var(--transition), box-shadow var(--transition);
  border: 1px solid var(--border);
}
.article-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }

/* 未读红点 */
.unread-dot {
  position: absolute; top: 12px; right: 12px;
  width: 8px; height: 8px; border-radius: 50%;
  background: #ef4444; box-shadow: 0 0 6px rgba(239,68,68,0.5);
}

.card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.card-tags { display: flex; gap: 6px; flex-wrap: wrap; }
.type-tag { font-size: 11px; }
.type-文章 { background: rgba(99,102,241,0.2); color: var(--primary-light); }
.type-简讯 { background: rgba(16,185,129,0.2); color: #34d399; }
.type-博客 { background: rgba(245,158,11,0.2); color: #fbbf24; }
.type-播客 { background: rgba(236,72,153,0.2); color: #f472b6; }
.type-视频 { background: rgba(239,68,68,0.2); color: #f87171; }
.meta-source-top { font-size: 12px; color: var(--text-muted); font-weight: 500; white-space: nowrap; }

.card-title { font-size: 15px; font-weight: 600; line-height: 1.5; margin-bottom: 8px; color: var(--text-primary); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.card-summary { font-size: 13px; color: var(--text-muted); line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 14px; flex: 1; }
.card-footer { display: flex; align-items: center; justify-content: space-between; font-size: 12px; color: var(--text-muted); }
.meta-date { }
.card-actions { display: flex; align-items: center; gap: 8px; }
.action-btn {
  display: inline-flex; align-items: center; justify-content: center;
  width: 32px; height: 32px;
  background: transparent; border: 1px solid var(--border); border-radius: 6px;
  font-size: 16px; cursor: pointer; color: var(--text-secondary);
  transition: all 0.2s ease; opacity: 0.6;
}
.action-btn:hover { opacity: 1; transform: translateY(-1px); }

/* 书签 */
.bookmark-btn:hover { border-color: var(--primary); color: var(--primary); background: rgba(99,102,241,0.1); }
.bookmark-btn.active { opacity: 1; border-color: var(--primary); background: rgba(99,102,241,0.15); color: var(--primary); }

/* 收藏 */
.fav-btn:hover { border-color: #eab308; color: #eab308; background: rgba(234,179,8,0.1); }
.fav-btn.active { opacity: 1; border-color: #eab308; background: rgba(234,179,8,0.15); color: #eab308; }

/* 删除 */
.del-btn { opacity: 0; font-size: 15px; }
.article-card:hover .del-btn { opacity: 0.6; }
.del-btn:hover { opacity: 1 !important; border-color: #ef4444; color: #ef4444; background: rgba(239,68,68,0.1); }

.skeleton-card { min-height: 180px; }
.empty-state { text-align: center; padding: 80px 20px; }
.empty-icon { font-size: 56px; margin-bottom: 16px; }
.empty-text { color: var(--text-muted); margin-bottom: 24px; }
</style>
