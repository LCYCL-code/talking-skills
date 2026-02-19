<template>
  <div class="hotspot-detail-page animate-fade-in">
    <button class="back-btn" @click="$router.back()">← 返回今日开吵</button>

    <div v-if="loading" class="card">
      <div class="skeleton" style="width:100%;height:28px;margin-bottom:12px;"></div>
      <div class="skeleton" style="width:100%;height:200px;"></div>
    </div>

    <template v-else-if="hotspot">
      <!-- 话题内容 -->
      <div class="card hotspot-content-card">
        <div class="hotspot-meta">
          <span :class="['platform-badge', platformClass(hotspot.platform)]">{{ hotspot.platform }}</span>
          <span class="hotspot-source">{{ hotspot.source }}</span>
          <span class="hotspot-date">{{ hotspot.published_at }}</span>
        </div>
        <h1 class="hotspot-title">{{ hotspot.title }}</h1>
        <div class="hotspot-body">{{ hotspot.content }}</div>
      </div>

      <!-- 评论列表（先展示） -->
      <div class="card comments-card">
        <h2 class="section-title">💬 评论 <span class="comment-count">{{ totalCommentCount }}</span></h2>

        <div v-if="comments.length" class="comments-list">
          <div v-for="c in comments" :key="c.id" class="comment-block">
            <!-- 主评论 -->
            <div class="comment-item">
              <div class="comment-avatar">{{ c.nickname?.[0] || '匿' }}</div>
              <div class="comment-content">
                <div class="comment-header">
                  <span class="comment-name">{{ c.nickname || '匿名用户' }}</span>
                  <span class="comment-time">{{ c.created_at }}</span>
                </div>
                <div class="comment-text">{{ c.content }}</div>
                <div class="comment-actions">
                  <button class="action-btn" @click="likeComment(c)">
                    👍 {{ c.likes || 0 }}
                  </button>
                  <button class="action-btn" @click="startReply(c)">
                    💬 回复
                  </button>
                </div>
              </div>
            </div>

            <!-- 子评论（二级回复） -->
            <div v-if="c.replies?.length" class="replies-list">
              <div v-for="r in c.replies" :key="r.id" class="comment-item reply-item">
                <div class="comment-avatar reply-avatar">{{ r.nickname?.[0] || '匿' }}</div>
                <div class="comment-content">
                  <div class="comment-header">
                    <span class="comment-name">{{ r.nickname || '匿名用户' }}</span>
                    <span class="comment-time">{{ r.created_at }}</span>
                  </div>
                  <div class="comment-text">{{ r.content }}</div>
                  <div class="comment-actions">
                    <button class="action-btn" @click="likeComment(r)">
                      👍 {{ r.likes || 0 }}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 行内回复框 -->
            <div v-if="replyingTo?.id === c.id" class="inline-reply">
              <textarea
                v-model="replyText"
                class="textarea textarea-sm"
                :placeholder="`回复 ${c.nickname || '匿名用户'}...`"
                rows="2"
                maxlength="500"
                ref="replyInput"
              ></textarea>
              <div class="reply-actions">
                <span class="char-count" :class="{ warn: replyText.length > 450 }">{{ replyText.length }}/500</span>
                <div>
                  <button class="btn btn-ghost btn-sm" @click="replyingTo = null; replyText = ''">取消</button>
                  <button class="btn btn-primary btn-sm" :disabled="!replyText.trim() || submitting" @click="postReply(c)">
                    {{ submitting ? '发送中...' : '发送' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state" style="padding:32px 0;">
          <p>还没有评论，快来发表第一条吧！</p>
        </div>
      </div>

      <!-- 发表评论（放在最下面） -->
      <div class="card comment-form-card">
        <h2 class="section-title">✏️ 发表你的观点</h2>
        <p class="tone-rule">😏 规矩：不说脏话，但阴阳怪气不限量供应。</p>

        <div v-if="!user" class="auth-hint">
          <span>登录后评论自动带上你的昵称 ✨</span>
          <router-link to="/login" class="btn btn-ghost btn-small">去登录</router-link>
        </div>

        <input
          v-if="!user"
          v-model="nickname"
          class="input"
          placeholder="你的昵称（可选，默认匿名用户）"
          maxlength="20"
          style="margin-bottom:10px;"
        />

        <div v-else class="logged-user-hint">
          <div class="user-avatar-sm">{{ user.nickname?.[0] || '?' }}</div>
          <span>{{ user.nickname }}</span>
        </div>

        <textarea v-model="commentText" class="textarea" placeholder="分享你的看法，尝试用金字塔原理表达：先说结论，再列理由..." rows="4" maxlength="500"></textarea>
        <div class="comment-form-footer">
          <span class="char-count" :class="{ warn: commentText.length > 450 }">{{ commentText.length }}/500</span>
          <button class="btn btn-primary" :disabled="submitting || !commentText.trim()" @click="postComment">
            <span v-if="submitting" class="spin">⟳</span>
            {{ submitting ? '发表中...' : '发表评论' }}
          </button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api/index.js'
import { useAuth } from '../composables/useAuth.js'

const route = useRoute()
const showToast = inject('showToast')
const { user } = useAuth()
const hotspot = ref(null)
const comments = ref([])
const loading = ref(true)
const nickname = ref('')
const commentText = ref('')
const submitting = ref(false)
const replyingTo = ref(null)
const replyText = ref('')
const replyInput = ref(null)

const totalCommentCount = computed(() => {
  let count = comments.value.length
  for (const c of comments.value) count += (c.replies?.length || 0)
  return count
})

function platformClass(p) {
  const map = { '微博': 'platform-weibo', '知乎': 'platform-zhihu', '小红书': 'platform-xiaohongshu', '抖音': 'platform-douyin' }
  return map[p] || ''
}

async function loadComments() {
  try { comments.value = await api.getComments(route.params.id) } catch (_) {}
}

async function postComment() {
  if (!commentText.value.trim()) { showToast('请输入评论内容', 'warning'); return }
  submitting.value = true
  try {
    await api.postComment(route.params.id, user.value?.nickname || nickname.value || '匿名用户', commentText.value)
    commentText.value = ''
    showToast('发表成功！', 'success')
    await loadComments()
  } catch (e) {
    showToast('发表失败：' + e.message, 'error')
  } finally {
    submitting.value = false
  }
}

function startReply(comment) {
  replyingTo.value = comment
  replyText.value = ''
  nextTick(() => {
    if (replyInput.value) {
      const el = Array.isArray(replyInput.value) ? replyInput.value[0] : replyInput.value
      el?.focus()
    }
  })
}

async function postReply(parent) {
  if (!replyText.value.trim()) return
  submitting.value = true
  try {
    await api.postComment(
      route.params.id,
      user.value?.nickname || nickname.value || '匿名用户',
      replyText.value,
      parent.id,
    )
    replyText.value = ''
    replyingTo.value = null
    showToast('回复成功！', 'success')
    await loadComments()
  } catch (e) {
    showToast('回复失败：' + e.message, 'error')
  } finally {
    submitting.value = false
  }
}

async function likeComment(comment) {
  try {
    const res = await api.likeComment(route.params.id, comment.id)
    comment.likes = res.likes
  } catch (e) {
    showToast('点赞失败', 'error')
  }
}

onMounted(async () => {
  try {
    hotspot.value = await api.getHotspot(route.params.id)
    await loadComments()
  } catch (_) {} finally {
    loading.value = false
  }
})
</script>

<style scoped>
.hotspot-content-card, .comments-card, .comment-form-card { margin-bottom: 20px; }
.hotspot-meta { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.platform-badge { padding: 3px 10px; border-radius: var(--radius-full); font-size: 12px; font-weight: 600; color: #fff; }
.hotspot-source { font-size: 13px; color: var(--text-muted); }
.hotspot-date { font-size: 13px; color: var(--text-muted); }
.hotspot-title { font-size: 24px; font-weight: 700; line-height: 1.5; margin-bottom: 20px; }
.hotspot-body { font-size: 15px; line-height: 1.8; color: var(--text-secondary); white-space: pre-wrap; }
.section-title { font-size: 18px; font-weight: 600; margin-bottom: 16px; }
.comment-count { font-size: 14px; color: var(--text-muted); font-weight: 400; margin-left: 6px; }
.comments-list { display: flex; flex-direction: column; gap: 24px; }
.comment-block { /* wrapper for comment + replies */ }
.comment-item { display: flex; gap: 14px; }
.comment-avatar {
  width: 38px; height: 38px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, #10b981, #06b6d4);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 15px; font-weight: 600;
}
.comment-content { flex: 1; min-width: 0; }
.comment-header { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.comment-name { font-size: 14px; font-weight: 600; }
.comment-time { font-size: 12px; color: var(--text-muted); }
.comment-text { font-size: 14px; line-height: 1.7; color: var(--text-secondary); }

/* 评论操作按钮 */
.comment-actions {
  display: flex;
  gap: 16px;
  margin-top: 8px;
}
.action-btn {
  background: none; border: none; cursor: pointer;
  font-size: 13px; color: var(--text-muted);
  padding: 2px 6px; border-radius: var(--radius-sm);
  transition: all 0.15s;
}
.action-btn:hover { color: var(--primary-light); background: rgba(16,185,129,0.08); }

/* 二级回复 */
.replies-list {
  margin-left: 52px;
  margin-top: 14px;
  padding-left: 16px;
  border-left: 2px solid var(--border);
  display: flex; flex-direction: column; gap: 14px;
}
.reply-item { }
.reply-avatar {
  width: 28px !important; height: 28px !important;
  font-size: 12px !important;
}

/* 行内回复框 */
.inline-reply {
  margin-left: 52px;
  margin-top: 10px;
}
.textarea-sm {
  font-size: 13px;
  padding: 8px 12px;
  min-height: 56px;
}
.reply-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
}
.reply-actions > div { display: flex; gap: 8px; }

/* 发表评论区 */
.auth-hint {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: rgba(16,185,129,0.08);
  border-radius: var(--radius-sm);
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 12px;
}
.btn-small { padding: 4px 12px; font-size: 12px; }
.logged-user-hint {
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 12px; font-size: 14px; font-weight: 600; color: var(--text-primary);
}
.user-avatar-sm {
  width: 28px; height: 28px; border-radius: 50%;
  background: linear-gradient(135deg, #10b981, #06b6d4);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 12px; font-weight: 600;
}
.comment-form-footer {
  display: flex; align-items: center; justify-content: space-between; margin-top: 12px;
}
.char-count { font-size: 12px; color: var(--text-muted); }
.char-count.warn { color: #f59e0b; }

/* 语气规则 */
.tone-rule {
  display: inline-block;
  font-size: 13px;
  color: var(--primary-light);
  background: rgba(16,185,129,0.08);
  border: 1px solid rgba(16,185,129,0.2);
  padding: 5px 14px;
  border-radius: var(--radius-full);
  margin-bottom: 12px;
}
</style>
