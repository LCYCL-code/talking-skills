<template>
  <div class="article-content-pane card">
    <div class="article-meta">
      <span class="tag" :class="`cat-${article.category}`">{{ article.category }}</span>
      <span class="tag source-tag">{{ article.source }}</span>
      <span class="article-date">{{ article.published_at }}</span>
      <button
        :class="['btn btn-sm fav-btn', article.is_favorite ? 'fav-active' : 'btn-ghost']"
        @click="$emit('toggleFav')"
      >{{ article.is_favorite ? '⭐ 已收藏' : '☆ 收藏' }}</button>
    </div>

    <h1 class="article-title">{{ showTranslated && translatedTitle ? translatedTitle : article.title }}</h1>

    <!-- 操作栏 -->
    <div class="action-bar">
      <a v-if="article.link" :href="article.link" target="_blank" class="btn btn-ghost btn-sm">阅读原文 ↗</a>

      <button
        v-if="!showTranslated"
        class="btn btn-sm btn-secondary translate-btn"
        :disabled="translating"
        @click="doTranslate"
      >
        <span v-if="translating" class="spin">⟳</span>
        {{ translating ? '翻译中...' : '🌐 翻译' }}
      </button>
      <button v-else class="btn btn-sm btn-ghost" @click="showTranslated = false">查看原文</button>
    </div>

    <div v-if="translateError" class="error-tip">{{ translateError }}</div>

    <div class="article-body">{{ showTranslated && translatedContent ? translatedContent : (article.content || article.summary) }}</div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { api } from '../api/index.js'

const props = defineProps({ article: Object })
defineEmits(['toggleFav'])
const showToast = inject('showToast')

const showTranslated = ref(false)
const translating = ref(false)
const translatedContent = ref('')
const translatedTitle = ref('')
const translateError = ref('')

async function doTranslate() {
  if (translatedContent.value) { showTranslated.value = true; return }
  translating.value = true
  translateError.value = ''
  try {
    const res = await api.translateArticle(props.article.id)
    translatedContent.value = res.translated_content || ''
    showTranslated.value = true
  } catch (e) {
    translateError.value = '翻译失败：' + (e.message || '请检查 API Key 配置')
    showToast('翻译失败', 'error')
  } finally {
    translating.value = false
  }
}
</script>

<style scoped>
.article-content-pane { height: 100%; box-sizing: border-box; }
.article-meta { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.source-tag { background: rgba(99,102,241,0.3); }
.article-date { color: var(--text-muted); font-size: 13px; }
.fav-btn { margin-left: auto; }
.fav-active { background: rgba(234,179,8,0.15); color: #eab308; border: 1px solid rgba(234,179,8,0.3); }
.article-title { font-size: 22px; font-weight: 700; line-height: 1.5; color: var(--text-primary); margin-bottom: 14px; }
.action-bar { display: flex; gap: 10px; align-items: center; margin-bottom: 16px; flex-wrap: wrap; }
.translate-btn { gap: 4px; }
.error-tip { color: var(--warning, #f59e0b); font-size: 13px; margin-bottom: 10px; padding: 8px 12px; background: rgba(245,158,11,0.1); border-radius: var(--radius-sm, 6px); }
.article-body { font-size: 15px; line-height: 1.85; color: var(--text-secondary); white-space: pre-wrap; word-break: break-word; }
.spin { display: inline-block; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
