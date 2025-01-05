export interface UserInfo {
  id: string
  nickname: string
  phone?: string
  email?: string
  avatarUrl: string
  createTime: string
  lastLoginTime?: string
}

export interface LoginResponse {
  token: string
  userInfo: UserInfo
}

export interface ApiResponse<T = any> {
  code: number
  data: T
  message: string
} 