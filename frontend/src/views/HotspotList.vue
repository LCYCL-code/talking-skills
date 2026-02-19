<template>
  <div class="hotspot-list-page animate-fade-in">
    <div class="page-header">
      <h1>今日开吵</h1>
      <p>主动出击，别做沉默的多数。有话说，就现在说。</p>
      <p class="tone-rule">😏 规矩：不说脏话，但阴阳怪气不限量供应。</p>
    </div>

    <!-- 两大专栏切换 -->
    <div class="section-tabs">
      <button :class="['tab-btn', { active: activeSection === 'today' }]" @click="switchSection('today')">
        🔥 今日热点
      </button>
      <button :class="['tab-btn', { active: activeSection === 'classic' }]" @click="switchSection('classic')">
        ♻️ 经典复现
      </button>
    </div>

    <!-- 今日热点的平台筛选 -->
    <div v-if="activeSection === 'today'" class="filter-bar">
      <button
        v-for="p in platforms"
        :key="p"
        :class="['filter-btn', { active: selectedPlatform === p }]"
        @click="selectPlatform(p)"
      >{{ p }}</button>
    </div>

    <!-- 经典复现说明 -->
    <div v-if="activeSection === 'classic'" class="classic-hint">
      <span>💡</span> 这些辩题没有对错，只有说不说得清楚。选一个，练习表达你的立场。
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="hotspot-grid">
      <div v-for="i in 5" :key="i" class="card">
        <div class="skeleton" style="width:80px;height:24px;margin-bottom:12px;"></div>
        <div class="skeleton" style="width:100%;height:22px;margin-bottom:8px;"></div>
        <div class="skeleton" style="width:100%;height:48px;"></div>
      </div>
    </div>

    <!-- 列表 -->
    <div v-else-if="hotspots.length" class="hotspot-grid">
      <div
        v-for="h in hotspots"
        :key="h.id"
        class="card card-clickable hotspot-card"
        @click="$router.push(`/hotspots/${h.id}`)"
      >
        <div class="hotspot-header">
          <span :class="['platform-badge', platformClass(h.platform)]">{{ h.platform }}</span>
          <span class="hotspot-source">{{ h.source }}</span>
          <span class="hotspot-date">{{ h.published_at }}</span>
        </div>
        <h3 class="hotspot-title">{{ h.title }}</h3>
        <p class="hotspot-preview">{{ h.content }}</p>
        <div class="hotspot-footer">
          <span class="join-discuss">⚡ {{ activeSection === 'classic' ? '开吵这道题 →' : '去吵一架 →' }}</span>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <div class="icon">{{ activeSection === 'classic' ? '♻️' : '🔥' }}</div>
      <p>{{ activeSection === 'classic' ? '经典辩题加载中…' : '暂无热点话题' }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { api } from '../api/index.js'

const platforms = ['全部', '微博', '知乎', '小红书', '抖音']
const selectedPlatform = ref('全部')
const activeSection = ref('today')
const hotspots = ref([])
const loading = ref(true)
const showToast = inject('showToast')

function platformClass(p) {
  const map = { '微博': 'platform-weibo', '知乎': 'platform-zhihu', '小红书': 'platform-xiaohongshu', '抖音': 'platform-douyin', '经典辩题': 'platform-classic' }
  return map[p] || ''
}

async function fetchHotspots() {
  loading.value = true
  try {
    hotspots.value = await api.getHotspots(selectedPlatform.value, activeSection.value)
  } catch (e) {
    showToast('加载失败', 'error')
  } finally {
    loading.value = false
  }
}

function selectPlatform(p) {
  selectedPlatform.value = p
  fetchHotspots()
}

function switchSection(section) {
  activeSection.value = section
  selectedPlatform.value = '全部'
  fetchHotspots()
}

onMounted(fetchHotspots)
</script>

<style scoped>
/* 专栏切换 */
.section-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 20px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 4px;
  width: fit-content;
}
.tab-btn {
  background: none;
  border: none;
  padding: 10px 24px;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition);
}
.tab-btn:hover { color: var(--text-primary); }
.tab-btn.active {
  background: var(--primary);
  color: #fff;
  box-shadow: 0 2px 8px rgba(16,185,129,0.3);
}

/* 经典辩题提示 */
.classic-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(16,185,129,0.08);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: var(--radius-sm);
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 20px;
}

/* 平台筛选 */
.filter-bar { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }

/* 经典辩题badge */
.platform-classic { background: linear-gradient(135deg, #10b981, #06b6d4); }

/* 列表 */
.hotspot-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 18px; }
.hotspot-card { display: flex; flex-direction: column; gap: 10px; }
.hotspot-header { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.platform-badge { padding: 3px 10px; border-radius: var(--radius-full); font-size: 12px; font-weight: 600; color: #fff; }
.hotspot-source { font-size: 12px; color: var(--text-muted); }
.hotspot-date { margin-left: auto; font-size: 12px; color: var(--text-muted); }
.hotspot-title { font-size: 17px; font-weight: 600; line-height: 1.5; }
.hotspot-preview {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}
.hotspot-footer { margin-top: auto; }
.join-discuss { font-size: 13px; color: var(--primary-light); font-weight: 500; }

/* 语气规则 */
.tone-rule {
  display: inline-block;
  font-size: 13px;
  color: var(--primary-light);
  background: rgba(16,185,129,0.08);
  border: 1px solid rgba(16,185,129,0.2);
  padding: 5px 14px;
  border-radius: var(--radius-full);
  margin-top: 8px;
}
</style>
