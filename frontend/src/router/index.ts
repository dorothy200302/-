import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/Home.vue')
      },
      {
        path: 'research',
        name: 'Research',
        component: () => import('@/views/research/ResearchList.vue')
      },
      {
        path: 'research/:id',
        name: 'ResearchDetail',
        component: () => import('@/views/research/ResearchDetail.vue')
      },
      {
        path: 'decision',
        name: 'Decision',
        component: () => import('@/views/decision/DecisionList.vue')
      },
      {
        path: 'decision/:id',
        name: 'DecisionDetail',
        component: () => import('@/views/decision/DecisionDetail.vue')
      },
      {
        path: 'goals',
        name: 'Goals',
        component: () => import('@/views/goals/GoalList.vue')
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 