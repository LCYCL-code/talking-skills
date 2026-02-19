<template>
  <Teleport to="body">
    <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-box">
        <div class="modal-header">
          <h2 class="modal-title">➕ 管理 RSS 订阅</h2>
          <button class="close-btn" @click="$emit('close')">✕</button>
        </div>

        <!-- 添加表单 -->
        <div class="add-form card">
          <div class="form-row">
            <label>订阅链接 <span class="required">*</span></label>
            <input
              v-model="form.url"
              class="form-input"
              placeholder="https://example.com/feed.xml"
              @keyup.enter="submit"
            />
          </div>
          <div class="form-row">
            <label>来源名称 <span class="optional">（选填）</span></label>
            <input v-model="form.name" class="form-input" placeholder="不填则自动提取域名" />
          </div>
          <div class="form-row two-col">
            <div>
              <label>内容类型</label>
              <select v-model="form.content_type" class="form-input">
                <option v-for="t in contentTypes" :key="t">{{ t }}</option>
              </select>
            </div>
            <div>
              <label>话题分类</label>
              <select v-model="form.category" class="form-input">
                <option v-for="c in categories" :key="c">{{ c }}</option>
              </select>
            </div>
          </div>
          <button
            class="btn btn-primary"
            :disabled="!form.url.trim() || adding"
            @click="submit"
          >
            <span v-if="adding" class="spin">⟳</span>
            {{ adding ? '添加中...' : '确认添加' }}
          </button>
        </div>

        <!-- 已订阅列表 -->
        <div v-if="sources.length" class="source-list">
          <div class="section-title">我的自定义来源（{{ sources.length }}）</div>
          <div v-for="s in sources" :key="s.id" class="source-item">
            <div class="source-info">
              <span class="source-name">{{ s.name || s.url }}</span>
              <div class="source-tags">
                <span class="tag source-cat">{{ s.category }}</span>
                <span class="tag source-type">{{ s.content_type }}</span>
              </div>
            </div>
            <button class="del-btn" @click="remove(s)" title="删除">🗑</button>
          </div>
        </div>
        <div v-else class="empty-sources">还没有自定义订阅，添加后点"刷新内容"生效</div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch, inject } from 'vue'
import { api } from '../api/index.js'

const props = defineProps({ show: Boolean })
const emit = defineEmits(['close'])
const showToast = inject('showToast')

const contentTypes = ['文章', '简讯', '博客', '播客', '视频']
const categories = ['AI', '科技', '金融', '商业', '安全', '文化']

const form = ref({ url: '', name: '', content_type: '文章', category: '科技' })
const adding = ref(false)
const sources = ref([])

watch(() => props.show, async (val) => {
  if (val) {
    try { sources.value = await api.getCustomSources() } catch {}
  }
})

async function submit() {
  if (!form.value.url.trim()) return
  adding.value = true
  try {
    const newSource = await api.addCustomSource({
      url: form.value.url.trim(),
      name: form.value.name.trim(),
      content_type: form.value.content_type,
      category: form.value.category,
    })
    sources.value.unshift(newSource)
    form.value = { url: '', name: '', content_type: '文章', category: '科技' }
    showToast('添加成功，刷新内容后生效', 'success')
  } catch (e) {
    showToast(e.message || '添加失败', 'error')
  } finally {
    adding.value = false
  }
}

async function remove(s) {
  try {
    await api.deleteCustomSource(s.id)
    sources.value = sources.value.filter(x => x.id !== s.id)
    showToast('已删除', 'success')
  } catch {
    showToast('删除失败', 'error')
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0; z-index: 999;
  background: rgba(0,0,0,0.55); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
}
.modal-box {
  background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px;
  width: min(540px, 93vw); max-height: 85vh; overflow-y: auto;
  padding: 24px; display: flex; flex-direction: column; gap: 20px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.modal-header { display: flex; justify-content: space-between; align-items: center; }
.modal-title { font-size: 18px; font-weight: 700; }
.close-btn { background: none; border: none; font-size: 18px; cursor: pointer; color: var(--text-muted); padding: 4px 8px; border-radius: 6px; }
.close-btn:hover { background: var(--border); color: var(--text-primary); }

.add-form { display: flex; flex-direction: column; gap: 14px; }
.form-row { display: flex; flex-direction: column; gap: 6px; }
.form-row label { font-size: 13px; font-weight: 500; color: var(--text-secondary); }
.required { color: #ef4444; }
.optional { color: var(--text-muted); font-weight: 400; }
.form-input {
  background: var(--bg-surface, rgba(255,255,255,0.05));
  border: 1px solid var(--border); border-radius: 8px;
  padding: 9px 12px; color: var(--text-primary); font-size: 14px;
  outline: none; width: 100%; box-sizing: border-box;
  transition: border-color 0.15s;
}
.form-input:focus { border-color: var(--primary); }
.two-col { flex-direction: row; gap: 12px; }
.two-col > div { flex: 1; display: flex; flex-direction: column; gap: 6px; }

.section-title { font-size: 13px; font-weight: 600; color: var(--text-muted); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em; }
.source-list { display: flex; flex-direction: column; gap: 8px; }
.source-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px; background: rgba(255,255,255,0.04);
  border: 1px solid var(--border); border-radius: 10px;
}
.source-info { display: flex; flex-direction: column; gap: 4px; min-width: 0; flex: 1; }
.source-name { font-size: 14px; font-weight: 500; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.source-tags { display: flex; gap: 6px; }
.source-cat, .source-type { font-size: 11px; padding: 2px 8px; border-radius: 10px; }
.source-cat { background: rgba(99,102,241,0.2); color: var(--primary-light); }
.source-type { background: rgba(16,185,129,0.2); color: #34d399; }
.del-btn { background: none; border: none; cursor: pointer; font-size: 16px; padding: 4px 6px; border-radius: 6px; opacity: 0.5; transition: opacity 0.15s; flex-shrink: 0; margin-left: 8px; }
.del-btn:hover { opacity: 1; }
.empty-sources { text-align: center; color: var(--text-muted); font-size: 13px; padding: 16px; }
.spin { display: inline-block; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
