<template>
  <div class="file-detail-page animate-fade-in">
    <button class="back-btn" @click="$router.push('/upload')">← 返回文件列表</button>

    <div v-if="loading" class="card">
      <div class="skeleton" style="width:100%;height:28px;margin-bottom:12px;"></div>
      <div class="skeleton" style="width:60%;height:18px;margin-bottom:24px;"></div>
      <div class="skeleton" style="width:100%;height:200px;"></div>
    </div>

    <template v-else-if="file">
      <!-- 文件内容展示 -->
      <div class="card file-content-card">
        <div class="file-meta">
          <span class="file-type-badge">{{ file.file_type?.toUpperCase() }}</span>
          <span class="file-date">{{ file.upload_at }}</span>
        </div>
        <h1 class="file-title">{{ file.title }}</h1>
        
        <!-- AI摘要/文件内容 -->
        <div class="file-body-box">
          <div v-if="file.ai_summary" class="ai-summary-badge">✨ AI 摘要</div>
          <div class="file-body">{{ file.content || file.ai_summary || '(暂无文本内容)' }}</div>
        </div>
      </div>

      <!-- 模式切换 -->
      <div class="mode-switch-card">
        <div class="mode-switch">
          <button 
            :class="['mode-btn', { active: mode === 'summary' }]"
            @click="mode = 'summary'"
          >
            📝 主动总结练习
          </button>
          <button 
            :class="['mode-btn', { active: mode === 'feynman' }]"
            @click="mode = 'feynman'"
          >
            🎓 带我练习 (费曼学习法)
          </button>
        </div>
      </div>

      <!-- 模式A：主动总结练习 -->
      <div v-if="mode === 'summary'" class="card practice-card animate-slide-in">
        <h2 class="section-title">📝 主动总结</h2>
        <p class="section-desc">阅读上方内容，用金字塔原理进行总结</p>

        <!-- 语音控件 -->
        <div v-if="speech.isRecording.value" class="recording-indicator" style="margin-bottom:12px;">
          <span class="recording-dot"></span>
          {{ speech.isPaused.value ? '已暂停' : '正在录音...' }}
        </div>
        <div v-if="speech.error.value" class="speech-error">
          ⚠️ {{ speech.error.value }}
        </div>

        <textarea
          v-model="summaryText"
          class="textarea"
          placeholder="请输入或录制您的总结..."
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
            {{ submitting ? 'AI分析中...' : '提交总结' }}
          </button>
          <button class="btn btn-ghost" @click="clearSummary">清空</button>
        </div>

        <!-- 结果展示 -->
        <div v-if="summaryResult" class="result-panel animate-fade-in">
          <div class="tabs">
            <button v-for="tab in resultTabs" :key="tab.key" :class="['tab-btn', { active: activeTab === tab.key }]" @click="activeTab = tab.key">{{ tab.label }}</button>
          </div>
          <div class="result-box">{{ summaryResult[activeTab] }}</div>
        </div>
      </div>

      <!-- 模式B：费曼学习法对话 -->
      <div v-else-if="mode === 'feynman'" class="card feynman-card animate-slide-in">
        <div class="feynman-header">
          <div>
            <h2 class="section-title">🎓 费曼学习法导师</h2>
            <p class="section-desc">AI 导师将通过提问引导你深入理解</p>
          </div>
          <button v-if="messages.length === 0" class="btn btn-primary btn-sm" @click="startFeynman">开始学习</button>
          <button v-else class="btn btn-ghost btn-sm" @click="restartFeynman">重新开始</button>
        </div>

        <div class="chat-window" ref="chatWindow">
          <div v-if="messages.length === 0" class="empty-chat">
            <div class="icon">👋</div>
            <p>点击上方"开始学习"启动对话</p>
          </div>
          <div v-else class="messages-list">
            <div 
              v-for="(msg, idx) in messages" 
              :key="idx" 
              :class="['message-item', msg.role === 'user' ? 'msg-user' : 'msg-ai']"
            >
              <div class="msg-avatar">{{ msg.role === 'user' ? '我' : 'AI' }}</div>
              <div class="msg-bubble">
                <div v-if="msg.content" style="white-space: pre-wrap;">{{ msg.content }}</div>
                <div v-else class="typing-dots"><span>.</span><span>.</span><span>.</span></div>
              </div>
            </div>
          </div>
        </div>

        <div class="chat-input-area">
          <textarea 
            v-model="chatInput" 
            class="input chat-input" 
            placeholder="输入你的回答..." 
            rows="1"
            @keydown.enter.prevent="sendChatMessage"
          ></textarea>
          <button class="btn btn-primary send-btn" :disabled="sending || !sessionId" @click="sendChatMessage">发送</button>
        </div>
      </div>

    </template>
    
    <div v-else class="empty-state">
      <div class="icon">📄</div>
      <p>文件不存在</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, inject, watch } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api/index.js'
import { useSpeechRecognition } from '../composables/useSpeechRecognition.js'

const route = useRoute()
const showToast = inject('showToast')
const speech = useSpeechRecognition()

const file = ref(null)
const loading = ref(true)
const mode = ref('summary') // 'summary' | 'feynman'

// 主动总结状态
const summaryText = ref('')
const submitting = ref(false)
const summaryResult = ref(null)
const activeTab = ref('ai_optimized')
const resultTabs = [
  { key: 'original_text', label: '原始输入' },
  { key: 'ai_optimized', label: 'AI优化总结' },
  { key: 'ai_direct', label: 'AI直接总结' },
]

// 费曼对话状态
const sessionId = ref(null)
const messages = ref([])
const chatInput = ref('')
const sending = ref(false)
const chatWindow = ref(null)

// 语音同步
watch(speech.transcript, (val) => {
  if (mode.value === 'summary') {
    summaryText.value = val
  }
})

// === 主动总结逻辑 ===
function startRecording() { speech.start() }
function stopRecording() { speech.stop() }
function clearSummary() { speech.clear(); summaryText.value = ''; summaryResult.value = null }

async function submitSummary() {
  if (!summaryText.value.trim()) return
  submitting.value = true
  try {
    const res = await api.createFileSummary(file.value.id, summaryText.value)
    summaryResult.value = res
    activeTab.value = 'ai_optimized'
    showToast('分析完成', 'success')
  } catch (e) { showToast(e.message, 'error') }
  finally { submitting.value = false }
}

// === 费曼主要逻辑 ===
async function startFeynman() {
  try {
    const res = await api.createFeynmanSession({ file_id: file.value.id })
    sessionId.value = res.session_id
    messages.value = [{ role: 'assistant', content: res.first_message }]
  } catch (e) { showToast('启动失败: ' + e.message, 'error') }
}

async function restartFeynman() {
  if (!confirm('确定要重新开始对话吗？历史记录将清除(仅本地)')) return
  messages.value = []
  sessionId.value = null
  startFeynman()
}

async function sendChatMessage() {
  const content = chatInput.value.trim()
  if (!content || !sessionId.value || sending.value) return
  
  messages.value.push({ role: 'user', content })
  chatInput.value = ''
  scrollToBottom()
  sending.value = true

  // 占位
  const aiMsgIndex = messages.value.push({ role: 'assistant', content: '' }) - 1

  try {
    const res = await api.sendFeynmanMessage(sessionId.value, content)
    messages.value[aiMsgIndex].content = res.content
    scrollToBottom()
  } catch (e) {
    messages.value[aiMsgIndex].content = '[发送失败: ' + e.message + ']'
  } finally {
    sending.value = false
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (chatWindow.value) chatWindow.value.scrollTop = chatWindow.value.scrollHeight
  })
}

onMounted(async () => {
  try {
    file.value = await api.getUpload(route.params.id)
  } catch (e) {
    showToast('加载失败', 'error')
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.file-meta { margin-bottom: 12px; display: flex; align-items: center; gap: 10px; }
.file-type-badge { background: var(--bg-elevated); padding: 2px 8px; border-radius: 4px; font-size: 12px; color: var(--text-muted); }
.file-date { font-size: 12px; color: var(--text-muted); }
.file-title { font-size: 22px; font-weight: 700; color: var(--text-primary); margin-bottom: 16px; }
.file-body-box { background: var(--bg-surface); padding: 16px; border-radius: 8px; border: 1px solid var(--border); max-height: 300px; overflow-y: auto; position: relative; }
.ai-summary-badge { position: absolute; top: 10px; right: 10px; background: linear-gradient(135deg, #8b5cf6, #d946ef); color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 600; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
.file-body { font-size: 14px; line-height: 1.7; color: var(--text-secondary); white-space: pre-wrap; }

.mode-switch-card { margin: 20px 0; display: flex; justify-content: center; }
.mode-switch { background: var(--bg-surface); padding: 4px; border-radius: var(--radius-full); display: inline-flex; border: 1px solid var(--border); }
.mode-btn { padding: 8px 20px; border-radius: var(--radius-full); border: none; background: transparent; color: var(--text-secondary); font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.mode-btn.active { background: var(--primary); color: white; box-shadow: 0 2px 8px rgba(99,102,241,0.4); }

.feynman-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.chat-window { height: 400px; background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; overflow-y: auto; margin-bottom: 16px; display: flex; flex-direction: column; }
.empty-chat { text-align: center; margin: auto; color: var(--text-muted); }
.empty-chat .icon { font-size: 40px; margin-bottom: 10px; }
.messages-list { display: flex; flex-direction: column; gap: 16px; }
.message-item { display: flex; gap: 12px; max-width: 85%; }
.msg-user { align-self: flex-end; flex-direction: row-reverse; }
.msg-ai { align-self: flex-start; }
.msg-avatar { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0; font-weight: 600; }
.msg-user .msg-avatar { background: var(--primary); color: white; }
.msg-ai .msg-avatar { background: linear-gradient(135deg, #10b981, #059669); color: white; }
.msg-bubble { padding: 10px 14px; border-radius: 12px; font-size: 14px; line-height: 1.6; word-break: break-all; }
.msg-user .msg-bubble { background: var(--primary); color: white; border-bottom-right-radius: 2px; }
.msg-ai .msg-bubble { background: var(--bg-elevated); color: var(--text-primary); border: 1px solid var(--border); border-bottom-left-radius: 2px; }

.chat-input-area { display: flex; gap: 10px; }
.chat-input { flex: 1; resize: none; height: 42px; line-height: 1.5; padding: 10px 12px; }
.send-btn { height: 42px; padding: 0 24px; }
.typing-dots span { animation: pulse 1s infinite; display: inline-block; margin: 0 1px; }
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

.section-title { font-size: 18px; font-weight: 600; margin-bottom: 6px; }
.section-desc { font-size: 13px; color: var(--text-muted); margin-bottom: 16px; }
.btn-group { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
.speech-error { color: var(--warning); font-size: 13px; margin-bottom: 10px; padding: 8px 12px; background: rgba(245,158,11,0.1); border-radius: var(--radius-sm); }
.not-supported { font-size: 13px; color: var(--text-muted); align-self: center; }
.result-panel { margin-top: 24px; padding-top: 20px; border-top: 1px solid var(--border); }
</style>
