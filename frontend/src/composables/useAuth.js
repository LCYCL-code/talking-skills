import { ref } from 'vue'

const user = ref(null)
const loading = ref(false)

export function useAuth() {
    async function fetchUser() {
        try {
            const res = await fetch('/api/auth/me', { credentials: 'include' })
            if (res.ok) {
                user.value = await res.json()
            } else {
                user.value = null
            }
        } catch {
            user.value = null
        }
    }

    async function login(email, password) {
        loading.value = true
        try {
            const res = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ email, password }),
            })
            const data = await res.json()
            if (!res.ok) throw new Error(data.detail || '登录失败')
            user.value = data.user
            return data
        } finally {
            loading.value = false
        }
    }

    async function register(email, password, nickname) {
        loading.value = true
        try {
            const res = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, nickname }),
            })
            const data = await res.json()
            if (!res.ok) throw new Error(data.detail || '注册失败')
            return data
        } finally {
            loading.value = false
        }
    }

    async function logout() {
        await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' })
        user.value = null
    }

    return { user, loading, fetchUser, login, register, logout }
}
