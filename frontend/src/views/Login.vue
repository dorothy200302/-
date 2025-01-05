<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2 class="login-title">智策系统</h2>
      </template>
      
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="0"
      >
        <el-tabs v-model="loginType">
          <el-tab-pane label="手机号登录" name="phone">
            <el-form-item prop="phone">
              <el-input
                v-model="formData.phone"
                placeholder="请输入手机号"
                prefix-icon="Phone"
              />
            </el-form-item>
            
            <el-form-item prop="verifyCode">
              <div class="verify-code">
                <el-input
                  v-model="formData.verifyCode"
                  placeholder="请输入验证码"
                  prefix-icon="Key"
                />
                <el-button
                  type="primary"
                  :disabled="!!countdown"
                  @click="sendCode"
                >
                  {{ countdown ? `${countdown}s后重新获取` : '获取验证码' }}
                </el-button>
              </div>
            </el-form-item>
          </el-tab-pane>
          
          <el-tab-pane label="邮箱登录" name="email">
            <el-form-item prop="email">
              <el-input
                v-model="formData.email"
                placeholder="请输入邮箱"
                prefix-icon="Message"
              />
            </el-form-item>
            
            <el-form-item prop="password">
              <el-input
                v-model="formData.password"
                type="password"
                placeholder="请输入密码"
                prefix-icon="Lock"
                show-password
              />
            </el-form-item>
          </el-tab-pane>
        </el-tabs>
        
        <el-form-item>
          <el-button
            type="primary"
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
        
        <div class="form-footer">
          <el-link type="primary" @click="$router.push('/register')">
            注册账号
          </el-link>
          <el-link type="primary" @click="$router.push('/forgot-password')">
            忘记密码？
          </el-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import type { FormInstance } from 'element-plus'
import { Phone, Message, Key, Lock } from '@element-plus/icons-vue'
import { sendSmsCode } from '@/api/user'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const loginType = ref('phone')
const countdown = ref(0)

const formData = reactive({
  phone: '',
  email: '',
  password: '',
  verifyCode: ''
})

const rules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码不能少于6位', trigger: 'blur' }
  ],
  verifyCode: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为6位数字', trigger: 'blur' }
  ]
}

const startCountdown = () => {
  countdown.value = 60
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

const sendCode = async () => {
  try {
    await formRef.value?.validateField('phone')
    await sendSmsCode({ phone: formData.phone })
    startCountdown()
  } catch (error) {
    // 验证失败
  }
}

const handleLogin = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    const loginData = loginType.value === 'phone'
      ? { phone: formData.phone, verifyCode: formData.verifyCode }
      : { email: formData.email, password: formData.password }
      
    await userStore.login(loginData)
    await userStore.getUserInfo()
    router.push('/')
  } catch (error) {
    // 登录失败
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
  
  .login-card {
    width: 400px;
    
    .login-title {
      text-align: center;
      margin: 0;
    }
    
    .verify-code {
      display: flex;
      gap: 10px;
      
      .el-input {
        flex: 1;
      }
      
      .el-button {
        width: 120px;
      }
    }
    
    .login-btn {
      width: 100%;
    }
    
    .form-footer {
      display: flex;
      justify-content: space-between;
      margin-top: 20px;
    }
  }
}
</style> 