import { Router } from 'vue-router'
import { useUserStore } from '@/store/user'

const whiteList = ['/login', '/register', '/forgot-password']

export function setupRouterGuard(router: Router) {
  router.beforeEach(async (to, from, next) => {
    const userStore = useUserStore()
    
    if (userStore.token) {
      if (to.path === '/login') {
        next('/')
      } else {
        if (!userStore.userInfo) {
          try {
            await userStore.getUserInfo()
            next()
          } catch (error) {
            userStore.logout()
            next(`/login?redirect=${to.path}`)
          }
        } else {
          next()
        }
      }
    } else {
      if (whiteList.includes(to.path)) {
        next()
      } else {
        next(`/login?redirect=${to.path}`)
      }
    }
  })
} 