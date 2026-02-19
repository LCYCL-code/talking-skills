<template>
  <div class="practice-pane">
    <!-- 总结练习 -->
    <div class="card practice-card">
      <h2 class="section-title">✍️ 总结练习</h2>
      <p class="section-desc">用金字塔原理总结这篇文章，结论先行，逻辑清晰</p>

      <div v-if="speech.isRecording.value" class="recording-indicator">
        <span class="recording-dot"></span>
        {{ speech.isPaused.value ? '已暂停' : '正在录音...' }}
      </div>
      <div v-if="speech.error.value" class="speech-error">⚠️ {{ speech.error.value }}</div>

      <textarea
        v-model="summaryText"
        class="textarea"
        placeholder="请输入或录制您的总结...&#10;&#10;提示：先说结论！"
        rows="8"
      ></textarea>

      <div class="btn-group">
        <template v-if="!speech.isRecording.value">
          <button v-if="speech.isSupported.value" class="btn btn-secondary" @click="startRecording">🎤 开始录音</button>
          <span v-else class="not-supported">语音识别仅支持 Chrome/Edge</span>
        </template>
        <template v-else>
          <button v-if="!speech.isPaused.value" class="btn btn-secondary" @click="speech.pause()">⏸ 暂停</button>
          <button v-else class="btn btn-secondary" @click="speech.resume()">▶ 继续</button>
          <button class="btn btn-danger" @click="stopRecording">⏹ 停止录音</button>
        </template>

        <button class="btn btn-primary" :disabled="submitting || !summaryText.trim()" @click="submitSummary">
          <span v-if="submitting" class="spin">⟳</span>
          {{ submitting ? 'AI 分析中...' : '提交总结' }}
        </button>
        <button class="btn btn-ghost" @click="clearSummary">清空</button>
      </div>

      <!-- 结果展示 -->
      <div v-if="summaryResult" class="result-panel animate-fade-in">
        <div class="tabs">
          <button v-for="tab in resultTabs" :key="tab.key"
            :class="['tab-btn', { active: activeTab === tab.key }]"
            @click="activeTab = tab.key">{{ tab.label }}</button>
        </div>
        <div class="result-box">{{ summaryResult[activeTab] }}</div>
      </div>
    </div>

    <!-- 历史记录 -->
    <div v-if="histories.length" class="card history-card">
      <h2 class="section-title">📚 历史总结记录</h2>
      <div class="history-list">
        <div v-for="record in histories" :key="record.id" class="history-item">
          <div class="history-meta">
            <span class="history-time">{{ record.created_at }}</span>
            <button class="btn btn-danger btn-sm" @click="deleteHistory(record.id)">删除</button>
          </div>
          <div class="tabs mini-tabs">
            <button v-for="tab in resultTabs" :key="tab.key"
              :class="['tab-btn', { active: record._activeTab === tab.key }]"
              @click="record._activeTab = tab.key">{{ tab.label }}</button>
          </div>
          <div class="result-box">{{ record[record._activeTab || 'original_text'] }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api/index.js'
import { useSpeechRecognition } from '../composables/useSpeechRecognition.js'

const props = defineProps({ article: Object })
const route = useRoute()
const showToast = inject('showToast')
const speech = useSpeechRecognition()

const summaryText = ref('')
const submitting = ref(false)
const summaryResult = ref(null)
const activeTab = ref('ai_optimized')
const histories = ref([])

const resultTabs = [
  { key: 'original_text', label: '原始输入' },
  { key: 'ai_optimized', label: 'AI优化总结' },
  { key: 'ai_direct', label: 'AI直接总结' },
]

watch(speech.transcript, (val) => { summaryText.value = val })

function startRecording() { speech.start() }
function stopRecording() { speech.stop() }
function clearSummary() { speech.clear(); summaryText.value = ''; summaryResult.value = null }

async function submitSummary() {
  if (!summaryText.value.trim()) { showToast('请先输入或录制您的总结', 'warning'); return }
  // 自动停止录音
  if (speech.isRecording.value) { speech.stop() }
  submitting.value = true
  try {
    const result = await api.createSummary(props.article.id, summaryText.value)
    summaryResult.value = result
    activeTab.value = 'ai_optimized'
    await loadHistories()
    showToast('分析完成！', 'success')
  } catch (e) {
    showToast('提交失败：' + e.message, 'error')
  } finally {
    submitting.value = false
  }
}

async function loadHistories() {
  try {
    const list = await api.getArticleSummaries(route.params.id)
    histories.value = list.map((i) => ({ ...i, _activeTab: 'original_text' }))
  } catch (_) {}
}

async function deleteHistory(id) {
  try {
    await api.deleteSummary(id)
    showToast('已删除', 'success')
    await loadHistories()
  } catch (e) { showToast('删除失败', 'error') }
}

onMounted(loadHistories)
</script>

<style scoped>
.practice-pane { display: flex; flex-direction: column; gap: 20px; }
.section-title { font-size: 18px; font-weight: 600; margin-bottom: 6px; }
.section-desc { font-size: 13px; color: var(--text-muted); margin-bottom: 16px; }
.recording-indicator { margin-bottom: 12px; }
.speech-error { color: var(--warning); font-size: 13px; margin-bottom: 10px; padding: 8px 12px; background: rgba(245,158,11,0.1); border-radius: var(--radius-sm); }
.btn-group { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
.not-supported { font-size: 13px; color: var(--text-muted); align-self: center; }
.result-panel { margin-top: 24px; padding-top: 20px; border-top: 1px solid var(--border); }
.history-list { display: flex; flex-direction: column; gap: 20px; }
.history-meta { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.history-time { font-size: 13px; color: var(--text-muted); }
.mini-tabs { margin-bottom: 12px; }
</style>
