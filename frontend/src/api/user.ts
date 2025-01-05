import request from '@/utils/request'

export interface LoginParams {
  phone?: string
  email?: string
  password?: string
  verifyCode?: string
}

export interface RegisterParams {
  phone?: string
  email?: string
  nickname: string
  password: string
  avatarUrl: string
}

export const login = (data: LoginParams) => {
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

export const register = (data: RegisterParams) => {
  return request({
    url: '/register',
    method: 'post',
    data
  })
}

export const sendSmsCode = (data: { phone: string }) => {
  return request({
    url: '/send-sms-code',
    method: 'post',
    data
  })
}

export const getUserInfo = () => {
  return request({
    url: '/user/info',
    method: 'get'
  })
} 