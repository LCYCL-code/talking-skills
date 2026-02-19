const BASE = '/api'

async function req(path, options = {}) {
    const res = await fetch(BASE + path, {
        headers: { 'Content-Type': 'application/json', ...options.headers },
        ...options,
    })
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }))
        throw new Error(err.detail || '请求失败')
    }
    return res.json()
}

// 文章
export const api = {
    // 文章模块
    getArticles: (category = '全部', contentType = '全部', status = '全部') =>
        req(`/articles?category=${encodeURIComponent(category)}&content_type=${encodeURIComponent(contentType)}&status=${encodeURIComponent(status)}`),
    refreshArticles: () =>
        req('/articles/refresh', { method: 'POST', body: JSON.stringify({}) }),
    getArticle: (id) => req(`/articles/${id}`),
    toggleFavorite: (id) =>
        req(`/articles/${id}/favorite`, { method: 'POST', body: JSON.stringify({}) }),
    getFavorites: () => req('/articles/favorites'),
    translateArticle: (id) =>
        req(`/articles/${id}/translate`, { method: 'POST', body: JSON.stringify({}) }),
    getReadLater: () => req('/articles/read-later'),
    markRead: (id) => req(`/articles/${id}/read`, { method: 'POST', body: JSON.stringify({}) }),
    toggleReadLater: (id) =>
        req(`/articles/${id}/read-later`, { method: 'POST', body: JSON.stringify({}) }),
    deleteArticle: (id) =>
        req(`/articles/${id}`, { method: 'DELETE' }),

    // 自定义 RSS 订阅
    getCustomSources: () => req('/custom-sources'),
    addCustomSource: (data) =>
        req('/custom-sources', { method: 'POST', body: JSON.stringify(data) }),
    deleteCustomSource: (id) =>
        req(`/custom-sources/${id}`, { method: 'DELETE' }),

    // Auth
    register: (data) => req('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
    login: (data) => req('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
    logout: () => req('/auth/logout', { method: 'POST' }),
    getMe: () => req('/auth/me'),

    // 总结
    createSummary: (articleId, originalText) =>
        req('/summaries', {
            method: 'POST',
            body: JSON.stringify({ article_id: articleId, original_text: originalText }),
        }),
    getArticleSummaries: (articleId) => req(`/summaries/article/${articleId}`),
    deleteSummary: (id) => req(`/summaries/${id}`, { method: 'DELETE' }),

    // 上传
    getUploads: () => req('/uploads'),
    getUpload: (id) => req(`/uploads/${id}`),
    uploadFile: (formData) =>
        fetch(BASE + '/uploads', { method: 'POST', body: formData }).then((r) => {
            if (!r.ok) return r.json().then((e) => { throw new Error(e.detail) })
            return r.json()
        }),
    createFileSummary: (fileId, originalText) =>
        req(`/uploads/${fileId}/summary`, {
            method: 'POST',
            body: JSON.stringify({ original_text: originalText }),
        }),
    getFileSummaries: (fileId) => req(`/uploads/${fileId}/summaries`),
    deleteUpload: (id) => req(`/uploads/${id}`, { method: 'DELETE' }),

    // 费曼学习法
    createFeynmanSession: (payload) =>
        req('/feynman/sessions', { method: 'POST', body: JSON.stringify(payload) }),
    getFeynmanMessages: (sessionId) => req(`/feynman/sessions/${sessionId}/messages`),
    sendFeynmanMessage: (sessionId, content) =>
        req(`/feynman/sessions/${sessionId}/messages`, {
            method: 'POST',
            body: JSON.stringify({ content }),
        }),

    // 热点
    getHotspots: (platform = '全部', category = 'today') =>
        req(`/hotspots?platform=${encodeURIComponent(platform)}&category=${encodeURIComponent(category)}`),
    getHotspot: (id) => req(`/hotspots/${id}`),
    getComments: (id) => req(`/hotspots/${id}/comments`),
    postComment: (id, nickname, content, parentId = null) =>
        req(`/hotspots/${id}/comments`, {
            method: 'POST',
            body: JSON.stringify({ nickname, content, parent_id: parentId }),
        }),
    likeComment: (hotspotId, commentId) =>
        req(`/hotspots/${hotspotId}/comments/${commentId}/like`, { method: 'POST', body: JSON.stringify({}) }),

    // AI 设置
    getAiConfig: () => req('/settings/config'),
    saveAiConfig: (apiKey, baseUrl, modelName) => req('/settings/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_key: apiKey, base_url: baseUrl, model_name: modelName })
    }),
}
