<template>
  <div class="article-detail-page animate-fade-in" :class="{ 'split-active': !isMobile }">

    <!-- ===== 手机端：普通布局 ===== -->
    <template v-if="isMobile">
      <button class="back-btn" @click="$router.back()">← 返回文章列表</button>
      <div v-if="loading" class="card skeleton-wrap">
        <div class="skeleton" style="width:100%;height:28px;margin-bottom:12px;"></div>
        <div class="skeleton" style="width:60%;height:18px;margin-bottom:24px;"></div>
        <div class="skeleton" style="width:100%;height:200px;"></div>
      </div>
      <template v-else-if="article">
        <ArticleContentPane :article="article" @toggle-fav="toggleFav" style="margin-bottom:20px;" />
        <PracticePane :article="article" />
      </template>
    </template>

    <!-- ===== 桌面端：可拖拽分屏 ===== -->
    <template v-else>
      <div class="split-container" ref="splitContainer">
        <!-- 左栏：原文 -->
        <div class="split-pane pane-left" :style="{ width: leftWidth + '%' }">
          <div class="pane-content">
            <button class="back-btn" @click="$router.back()">← 返回文章列表</button>
            <div v-if="loading" class="card skeleton-wrap">
              <div class="skeleton" style="width:100%;height:28px;margin-bottom:12px;"></div>
              <div class="skeleton" style="width:100%;height:200px;"></div>
            </div>
            <ArticleContentPane v-else-if="article" :article="article" @toggle-fav="toggleFav" />
          </div>
        </div>

        <!-- 分隔拖拽条 -->
        <div
          class="split-divider"
          :class="{ dragging: isDragging }"
          @mousedown.prevent="startDrag"
          title="拖动调整分屏比例"
        >
          <div class="divider-handle"></div>
        </div>

        <!-- 右栏：练习 -->
        <div class="split-pane pane-right" :style="{ width: (100 - leftWidth - dividerPercent) + '%' }">
          <div class="pane-content">
            <template v-if="!loading && article">
              <PracticePane :article="article" />
            </template>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, inject } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api/index.js'
import ArticleContentPane from '../components/ArticleContentPane.vue'
import PracticePane from '../components/PracticePane.vue'

const route = useRoute()
const showToast = inject('showToast')

const article = ref(null)
const loading = ref(true)
const isMobile = ref(window.innerWidth < 900)

// ========== 分屏拖拽 ==========
const splitContainer = ref(null)
const dividerPercent = 0.6  // 拖拽条占宽度 0.6%
const leftWidth = ref(52)   // 左栏初始 52%
const isDragging = ref(false)
let startX = 0
let startLeft = 0

function startDrag(e) {
  isDragging.value = true
  startX = e.clientX
  startLeft = leftWidth.value
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
  document.body.style.cursor = 'col-resize'
  document.body.style.userSelect = 'none'
}

function onDrag(e) {
  if (!isDragging.value || !splitContainer.value) return
  const containerWidth = splitContainer.value.clientWidth
  const dx = e.clientX - startX
  const dxPercent = (dx / containerWidth) * 100
  const newLeft = Math.min(75, Math.max(25, startLeft + dxPercent))
  leftWidth.value = Math.round(newLeft * 100) / 100
}

function stopDrag() {
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.body.style.cursor = ''
  document.body.style.userSelect = ''
}

function handleResize() {
  isMobile.value = window.innerWidth < 900
}

async function toggleFav() {
  if (!article.value) return
  try {
    const result = await api.toggleFavorite(article.value.id)
    article.value.is_favorite = result.is_favorite ? 1 : 0
    showToast(article.value.is_favorite ? '已收藏' : '已取消收藏', 'success')
  } catch (e) {
    showToast('操作失败', 'error')
  }
}

onMounted(async () => {
  window.addEventListener('resize', handleResize)
  try {
    article.value = await api.getArticle(route.params.id)
  } catch (e) {
    showToast('加载失败', 'error')
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  stopDrag()
})
</script>

<style scoped>
.article-detail-page { height: 100%; }

/* 分屏容器 */
.split-container {
  display: flex;
  height: calc(100vh - 48px);
  overflow: hidden;
}

.split-pane {
  overflow-y: auto;
  flex-shrink: 0;
}

.pane-content {
  padding: 24px;
  min-height: 100%;
}

/* 拖拽分隔条 */
.split-divider {
  width: 6px;
  flex-shrink: 0;
  cursor: col-resize;
  background: var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
  position: relative;
}
.split-divider:hover,
.split-divider.dragging {
  background: var(--primary);
}
.divider-handle {
  width: 2px;
  height: 40px;
  border-radius: 2px;
  background: rgba(255,255,255,0.25);
}

/* 手机端 */
@media (max-width: 900px) {
  .pane-content { padding: 16px; }
}
</style>
