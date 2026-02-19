<template>
  <div class="settings-page animate-fade-in">
    <h1 class="page-title">⚙️ 设置</h1>

    <!-- AI 模型配置 -->
    <section class="card">
      <div class="card-header">
        <h2 class="card-title">🤖 AI 模型配置</h2>
        <span :class="['status-badge', aiConfig.configured ? 'badge-ok' : 'badge-warn']">
          {{ aiConfig.configured ? `✅ 已连接: ${aiConfig.provider}` : '⚠️ 未配置' }}
        </span>
      </div>
      <div class="card-body">
        <p class="desc">配置 AI 服务后可解锁文章摘要、关键词提取和对话功能。支持所有兼容 OpenAI 格式的接口。</p>
        
        <!-- 快速预设 -->
        <div class="presets">
          <span class="preset-label">快速填充：</span>
          <button class="preset-btn" @click="applyPreset('zhipu')">智谱 AI</button>
          <button class="preset-btn" @click="applyPreset('deepseek')">DeepSeek</button>
          <button class="preset-btn" @click="applyPreset('moonshot')">Kimi (Moonshot)</button>
          <button class="preset-btn" @click="applyPreset('aliyun')">通义千问</button>
        </div>

        <div class="form-group">
          <label>API Base URL</label>
          <input v-model="form.baseUrl" class="input" placeholder="例如: https://open.bigmodel.cn/api/paas/v4/" />
        </div>

        <div class="form-group">
          <label>API Key</label>
          <div class="input-wrapper">
            <input
              v-model="form.apiKey"
              :type="showKey ? 'text' : 'password'"
              class="input"
              :placeholder="aiConfig.configured ? '已配置，输入新 Key 可覆盖' : '请输入 sk-xxxxxxxx'"
            />
            <button class="toggle-eye" @click="showKey = !showKey">{{ showKey ? '🙈' : '👁' }}</button>
          </div>
        </div>

        <div class="form-group">
          <label>模型名称 (Model Name)</label>
          <input v-model="form.modelName" class="input" placeholder="例如: glm-4-flash, deepseek-chat" />
        </div>

        <div class="form-actions">
          <div v-if="aiConfig.configured" class="current-info">
            当前模型: <code>{{ aiConfig.model_name }}</code>
          </div>
          <button class="btn btn-primary" :disabled="saving || !isValid" @click="saveConfig">
            {{ saving ? '保存中...' : '保存配置' }}
          </button>
        </div>
        
        <div class="provider-links">
          🔗 申请 Key: 
          <a href="https://open.bigmodel.cn/usercenter/apikeys" target="_blank">智谱AI</a> · 
          <a href="https://platform.deepseek.com/api_keys" target="_blank">DeepSeek</a> · 
          <a href="https://platform.moonshot.cn/console/api-keys" target="_blank">Moonshot</a> · 
          <a href="https://bailian.console.aliyun.com/" target="_blank">阿里云百炼</a>
        </div>
      </div>
    </section>

    <!-- RSS 订阅管理 -->
    <section class="card">
      <div class="card-header">
        <h2 class="card-title">📡 自定义 RSS 源</h2>
        <button class="btn btn-outline btn-sm" @click="showAddModal = true">+ 添加</button>
      </div>
      <div class="card-body" v-if="loadingSources">
        <p class="empty-text">加载中...</p>
      </div>
      <div class="card-body" v-else-if="sources.length === 0">
        <p class="empty-text">暂无自定义订阅源</p>
      </div>
      <div class="source-list" v-else>
        <div v-for="s in sources" :key="s.id" class="source-item">
          <div class="source-info">
            <div class="source-name">{{ s.name || s.url }}</div>
            <div class="source-meta">
              <span class="tag">{{ s.category }}</span>
              <span class="url-text">{{ s.url }}</span>
            </div>
          </div>
          <button class="del-btn" @click="removeSource(s)" title="删除">🗑</button>
        </div>
      </div>
    </section>

    <!-- 关于 -->
    <section class="card">
      <div class="card-header">
        <h2 class="card-title">ℹ️ 关于</h2>
      </div>
      <div class="card-body about-body">
        <p><strong>别吵架</strong> v1.0.0</p>
        <p class="desc">基于金字塔原理的智能表达训练平台</p>
      </div>
    </section>

    <!-- RSS 添加弹窗 -->
    <RssModal :show="showAddModal" @close="closeModal" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { api } from '../api/index.js'
import RssModal from '../components/RssModal.vue'

const showToast = inject('showToast', (msg) => alert(msg))

// ===== AI Config =====
const aiConfig = ref({ configured: false, provider: '未配置', model_name: '' })
const form = ref({ apiKey: '', baseUrl: '', modelName: '' })
const showKey = ref(false)
const saving = ref(false)

const isValid = computed(() => 
  form.value.baseUrl.trim() && 
  form.value.modelName.trim() && 
  (aiConfig.value.configured || form.value.apiKey.trim())
)

const PRESETS = {
  zhipu: {
    baseUrl: 'https://open.bigmodel.cn/api/paas/v4/',
    modelName: 'glm-4-flash'
  },
  deepseek: {
    baseUrl: 'https://api.deepseek.com',
    modelName: 'deepseek-chat'
  },
  moonshot: {
    baseUrl: 'https://api.moonshot.cn/v1',
    modelName: 'moonshot-v1-8k'
  },
  aliyun: {
    baseUrl: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    modelName: 'qwen-plus'
  }
}

function applyPreset(key) {
  const p = PRESETS[key]
  form.value.baseUrl = p.baseUrl
  form.value.modelName = p.modelName
}

async function loadAiConfig() {
  try {
    const res = await api.getAiConfig()
    aiConfig.value = res
    if (res.configured) {
      form.value.baseUrl = res.base_url
      form.value.modelName = res.model_name
      // API Key 不回显，只用 placeholder
    }
  } catch (e) {
    console.error('Failed to load AI config:', e)
  }
}

async function saveConfig() {
  if (!form.value.apiKey.trim() && !aiConfig.value.configured) {
    showToast('首次配置请填写 API Key', 'warning')
    return
  }
  
  saving.value = true
  try {
    await api.saveAiConfig(
      form.value.apiKey, 
      form.value.baseUrl, 
      form.value.modelName
    )
    showToast('AI 配置已保存！', 'success')
    form.value.apiKey = '' // 清空输入框
    await loadAiConfig()   // 重新加载状态
  } catch (e) {
    showToast('保存失败：' + (e.message || '未知错误'), 'error')
  } finally {
    saving.value = false
  }
}

// ===== RSS 源 =====
const sources = ref([])
const loadingSources = ref(false)
const showAddModal = ref(false)

async function loadSources() {
  loadingSources.value = true
  try {
    sources.value = await api.getCustomSources()
  } catch (e) {
    console.error('Failed to load sources:', e)
    sources.value = []
  } finally {
    loadingSources.value = false
  }
}

async function removeSource(s) {
  if (!confirm(`确定删除 "${s.name}" 吗？`)) return
  try {
    await api.deleteCustomSource(s.id)
    sources.value = sources.value.filter(x => x.id !== s.id)
    showToast('已删除', 'success')
  } catch (e) {
    showToast('删除失败', 'error')
  }
}

function closeModal() {
  showAddModal.value = false
  loadSources()
}

onMounted(() => {
  loadAiConfig()
  loadSources()
})
</script>

<style scoped>
.settings-page { max-width: 700px; margin: 0 auto; padding-bottom: 40px; }
.page-title { font-size: 24px; font-weight: 700; margin-bottom: 24px; color: var(--text-primary); }

/* Card */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  margin-bottom: 20px;
  overflow: hidden;
}
.card-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 24px; border-bottom: 1px solid var(--border);
}
.card-title { font-size: 15px; font-weight: 600; color: var(--text-primary); }
.card-body { padding: 20px 24px; }

/* Status badge */
.status-badge { font-size: 12px; padding: 3px 10px; border-radius: 12px; font-weight: 500; }
.badge-ok { background: rgba(16,185,129,0.12); color: #10b981; }
.badge-warn { background: rgba(239,68,68,0.1); color: #ef4444; }

/* AI Form */
.desc { font-size: 13px; color: var(--text-secondary); margin-bottom: 16px; line-height: 1.5; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 13px; font-weight: 500; color: var(--text-primary); margin-bottom: 6px; }
.input-wrapper { position: relative; }
.input {
  width: 100%; padding: 10px 14px; border-radius: 8px;
  border: 1px solid var(--border); background: var(--bg-surface);
  color: var(--text-primary); font-size: 14px; box-sizing: border-box;
  transition: border-color 0.2s;
}
.input:focus { outline: none; border-color: var(--primary); }
.toggle-eye {
  position: absolute; right: 10px; top: 50%; transform: translateY(-50%);
  background: none; border: none; cursor: pointer; font-size: 16px;
}

/* Presets */
.presets { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
.preset-label { font-size: 12px; color: var(--text-muted); }
.preset-btn {
  background: var(--bg-surface); border: 1px solid var(--border);
  padding: 4px 10px; border-radius: 6px; font-size: 12px;
  color: var(--text-secondary); cursor: pointer; transition: all 0.2s;
}
.preset-btn:hover { border-color: var(--primary); color: var(--primary); background: rgba(16,185,129,0.05); }

/* Actions */
.form-actions { display: flex; justify-content: space-between; align-items: center; margin-top: 24px; }
.current-info { font-size: 13px; color: var(--text-muted); }
.current-info code { background: rgba(0,0,0,0.2); padding: 2px 6px; border-radius: 4px; color: var(--text-primary); }

.provider-links { margin-top: 16px; font-size: 12px; color: var(--text-muted); }
.provider-links a { color: var(--primary); text-decoration: none; margin: 0 4px; }
.provider-links a:hover { text-decoration: underline; }

/* Buttons */
.btn { border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 500; transition: all 0.2s; }
.btn-primary { padding: 10px 24px; background: var(--primary); color: white; }
.btn-primary:hover { opacity: 0.9; }
.btn-primary:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-outline { padding: 6px 14px; background: transparent; border: 1px solid var(--border); color: var(--text-secondary); }
.btn-outline:hover { border-color: var(--primary); color: var(--primary); }
.btn-sm { font-size: 13px; }

/* Source list (unchanged styles) */
.source-list { display: flex; flex-direction: column; }
.source-item { display: flex; justify-content: space-between; align-items: center; padding: 14px 24px; border-bottom: 1px solid var(--border); }
.source-item:last-child { border-bottom: none; }
.source-name { font-size: 14px; font-weight: 500; color: var(--text-primary); margin-bottom: 4px; }
.source-meta { display: flex; gap: 8px; align-items: center; }
.tag { font-size: 11px; padding: 2px 8px; border-radius: 4px; background: rgba(99,102,241,0.1); color: var(--primary); }
.url-text { font-size: 12px; color: var(--text-muted); max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.del-btn { background: none; border: none; cursor: pointer; opacity: 0.4; font-size: 16px; transition: all 0.2s; }
.del-btn:hover { opacity: 1; color: #ef4444; }
.empty-text { text-align: center; color: var(--text-muted); font-size: 13px; padding: 10px 0; }
.about-body p { margin-bottom: 6px; }
</style>
