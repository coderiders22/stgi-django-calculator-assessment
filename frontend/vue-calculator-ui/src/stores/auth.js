import { reactive } from 'vue'
import api from '@/services/api'

export const auth = reactive({
  loading: true,
  isAuthenticated: false,
  username: null,

  async init() {
    try {
      const res = await api.get('/auth/me/')
      if (res.data.is_authenticated) {
        this.isAuthenticated = true
        this.username = res.data.username
      } else {
        this.isAuthenticated = false
        this.username = null
      }
    } catch {
      this.isAuthenticated = false
      this.username = null
    } finally {
      this.loading = false
    }
  },

  logoutLocal() {
    this.isAuthenticated = false
    this.username = null
  }
})
