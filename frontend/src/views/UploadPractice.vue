<template>
  <div class="upload-page animate-fade-in">
    <div class="page-header">
      <h1>上台前练一遍</h1>
      <p>答辩、汇报、课件……上传上来，先尞赢自己再上台。</p>
    </div>

    <!-- 上传区 -->
    <div class="card upload-card">
      <div
        class="drop-zone"
        :class="{ dragging: isDragging }"
        @dragover.prevent="isDragging = true"
        @dragleave="isDragging = false"
        @drop.prevent="onDrop"
        @click="$refs.fileInput.click()"
      >
        <div class="drop-icon">📂</div>
        <p class="drop-title">点击选择或拖拽文件到此处</p>
        <p class="drop-hint">支持 PDF、Word、PPT、TXT、图片，最大 10MB</p>
        <input
          ref="fileInput"
          type="file"
          style="display:none"
          accept=".pdf,.doc,.docx,.ppt,.pptx,.txt,.jpg,.jpeg,.png"
          @change="onFileSelect"
        />
      </div>

      <div v-if="selectedFile" class="selected-file">
        <span class="file-icon">{{ fileIcon(selectedFile.name) }}</span>
        <span class="file-name">{{ selectedFile.name }}</span>
        <span class="file-size">{{ (selectedFile.size / 1024).toFixed(1) }} KB</span>
        <button class="btn btn-danger btn-sm" @click="selectedFile = null">✕</button>
      </div>

      <div class="upload-form">
        <input
          v-model="title"
          class="input"
          placeholder="文件标题（必填）"
          style="margin-bottom: 12px;"
        />
        <button
          class="btn btn-primary btn-lg"
          :disabled="!selectedFile || !title.trim() || uploading"
          @click="doUpload"
          style="width:100%;"
        >
          <span v-if="uploading" class="spin">⟳</span>
          {{ uploading ? '上传中...' : '上传，然后开口' }}
        </button>
      </div>
    </div>

    <!-- 已上传文件列表 -->
    <div v-if="files.length" style="margin-top: 28px;">
      <h2 style="font-size:18px;font-weight:600;margin-bottom:16px;">🎤 我的练习材料</h2>
      <div class="files-grid">
        <div
          v-for="f in files"
          :key="f.id"
          class="card card-clickable file-card"
          @click="$router.push(`/upload/${f.id}`)"
        >
          <div class="file-type-icon">{{ fileIcon(f.filename) }}</div>
          <div class="file-info">
            <div class="file-title">{{ f.title }}</div>
          <div class="file-meta">{{ f.filename }} · {{ f.upload_at }}</div>
          </div>
          <span class="file-badge">{{ f.file_type?.toUpperCase() }}</span>
          <button class="btn-delete" title="删除" @click.stop="deleteFile(f)">
            🗑️
          </button>
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
const files = ref([])
const selectedFile = ref(null)
const title = ref('')
const uploading = ref(false)
const isDragging = ref(false)

function fileIcon(name = '') {
  const ext = name.split('.').pop().toLowerCase()
  const map = { pdf: '📄', doc: '📝', docx: '📝', ppt: '📊', pptx: '📊', txt: '📃', jpg: '🖼️', jpeg: '🖼️', png: '🖼️' }
  return map[ext] || '📁'
}

function onFileSelect(e) {
  const f = e.target.files[0]
  if (!f) return
  if (f.size > 10 * 1024 * 1024) { showToast('文件大小不能超过10MB', 'error'); return }
  selectedFile.value = f
  if (!title.value) title.value = f.name.replace(/\.[^.]+$/, '')
}

function onDrop(e) {
  isDragging.value = false
  const f = e.dataTransfer.files[0]
  if (!f) return
  if (f.size > 10 * 1024 * 1024) { showToast('文件大小不能超过10MB', 'error'); return }
  selectedFile.value = f
  if (!title.value) title.value = f.name.replace(/\.[^.]+$/, '')
}

async function doUpload() {
  if (!selectedFile.value || !title.value.trim()) return
  uploading.value = true
  try {
    const fd = new FormData()
    fd.append('file', selectedFile.value)
    fd.append('title', title.value)
    const res = await api.uploadFile(fd)
    showToast('上传成功！', 'success')
    router.push(`/upload/${res.id}`)
  } catch (e) {
    showToast('上传失败：' + e.message, 'error')
  } finally {
    uploading.value = false
  }
}

onMounted(async () => {
  try { files.value = await api.getUploads() } catch (_) {}
})

async function deleteFile(f) {
  if (!confirm(`确定要删除「${f.title}」吗？关联的练习记录也会一并删除。`)) return
  try {
    await api.deleteUpload(f.id)
    files.value = files.value.filter(item => item.id !== f.id)
    showToast('已删除', 'success')
  } catch (e) {
    showToast('删除失败：' + e.message, 'error')
  }
}
</script>

<style scoped>
.upload-card { margin-bottom: 8px; }
.drop-zone {
  border: 2px dashed var(--border);
  border-radius: var(--radius-md);
  padding: 48px 24px;
  text-align: center;
  cursor: pointer;
  transition: all var(--transition);
  margin-bottom: 20px;
}
.drop-zone:hover, .drop-zone.dragging {
  border-color: var(--primary);
  background: rgba(16,185,129,0.05);
}
.drop-icon { font-size: 48px; margin-bottom: 12px; }
.drop-title { font-size: 16px; font-weight: 600; margin-bottom: 6px; }
.drop-hint { font-size: 13px; color: var(--text-muted); }
.selected-file {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: var(--bg-surface);
  border-radius: var(--radius-sm);
  margin-bottom: 16px;
}
.file-icon { font-size: 20px; }
.file-name { flex: 1; font-size: 14px; }
.file-size { font-size: 12px; color: var(--text-muted); }
.files-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; }
.file-card { display: flex; align-items: center; gap: 14px; }
.file-type-icon { font-size: 32px; }
.file-info { flex: 1; min-width: 0; }
.file-title { font-size: 15px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.file-meta { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.file-badge { font-size: 11px; padding: 2px 8px; background: var(--bg-elevated); border-radius: var(--radius-full); color: var(--text-muted); flex-shrink: 0; }
.btn-delete {
  background: none; border: none; cursor: pointer; font-size: 16px;
  opacity: 0; transition: opacity 0.15s; padding: 4px 6px; flex-shrink: 0;
}
.file-card:hover .btn-delete { opacity: 0.6; }
.btn-delete:hover { opacity: 1 !important; }
</style>
