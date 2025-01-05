import { defineStore } from 'pinia'
import { login, getUserInfo } from '@/api/user'

interface UserState {
  token: string
  userInfo: any
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    token: localStorage.getItem('token') || '',
    userInfo: null
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  
  actions: {
    async login(data: { phone?: string; email?: string; password?: string; verifyCode?: string }) {
      try {
        const res = await login(data)
        this.token = res.data.token
        localStorage.setItem('token', res.data.token)
        return res
      } catch (error) {
        throw error
      }
    },
    
    async getUserInfo() {
      try {
        const res = await getUserInfo()
        this.userInfo = res.data
        return res
      } catch (error) {
        throw error
      }
    },
    
    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
    }
  }
}) 