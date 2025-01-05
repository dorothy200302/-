<template>
  <div class="research-container">
    <div class="header">
      <h2>调研管理</h2>
      <el-button type="primary" @click="showCreateDialog">
        新建调研
      </el-button>
    </div>

    <el-table :data="researchList" v-loading="loading">
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="research_type" label="类型">
        <template #default="{ row }">
          <el-tag>{{ getTypeLabel(row.research_type) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="create_time" label="创建时间" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button link @click="viewDetail(row)">查看</el-button>
          <el-button link type="primary" @click="editResearch(row)">编辑</el-button>
          <el-button link type="danger" @click="deleteResearch(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建/编辑对话框 -->
    <el-dialog
      :title="dialogType === 'create' ? '新建调研' : '编辑调研'"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入调研标题" />
        </el-form-item>
        
        <el-form-item label="类型" prop="research_type">
          <el-select v-model="formData.research_type" placeholder="请选择调研类型">
            <el-option
              v-for="item in typeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            rows="4"
            placeholder="请输入调研描述"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { FormInstance } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getResearchList, createResearch, updateResearch, deleteResearch } from '@/api/research'

const router = useRouter()
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const formRef = ref<FormInstance>()
const researchList = ref([])

const typeOptions = [
  { value: 'market', label: '市场调研' },
  { value: 'user', label: '用户调研' },
  { value: 'competitor', label: '竞品分析' }
]

const formData = reactive({
  title: '',
  research_type: '',
  description: '',
  data_sources: []
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  research_type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  description: [{ required: true, message: '请输入描述', trigger: 'blur' }]
}

// 获取列表数据
const fetchList = async () => {
  try {
    loading.value = true
    const res = await getResearchList()
    researchList.value = res.data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchList()
})

// 显示创建对话框
const showCreateDialog = () => {
  dialogType.value = 'create'
  dialogVisible.value = true
  formData.title = ''
  formData.research_type = ''
  formData.description = ''
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    submitting.value = true
    
    if (dialogType.value === 'create') {
      await createResearch(formData)
      ElMessage.success('创建成功')
    } else {
      await updateResearch(formData)
      ElMessage.success('更新成功')
    }
    
    dialogVisible.value = false
    fetchList()
  } catch (error) {
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 查看详情
const viewDetail = (row: any) => {
  router.push(`/research/${row._id}`)
}

// 编辑
const editResearch = (row: any) => {
  dialogType.value = 'edit'
  Object.assign(formData, row)
  dialogVisible.value = true
}

// 删除
const deleteResearch = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该调研吗？', '提示', {
      type: 'warning'
    })
    
    await deleteResearch(row._id)
    ElMessage.success('删除成功')
    fetchList()
  } catch (error) {
    console.error(error)
  }
}

// 工具函数
const getTypeLabel = (type: string) => {
  return typeOptions.find(item => item.value === type)?.label || type
}

const getStatusLabel = (status: string) => {
  const statusMap: Record<string, string> = {
    draft: '草稿',
    in_progress: '进行中',
    completed: '已完成'
  }
  return statusMap[status] || status
}

const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    draft: 'info',
    in_progress: 'warning',
    completed: 'success'
  }
  return typeMap[status] || ''
}
</script>

<style scoped lang="scss">
.research-container {
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      margin: 0;
    }
  }
}
</style> 