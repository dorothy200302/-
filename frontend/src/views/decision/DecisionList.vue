<template>
  <div class="decision-list">
    <div class="header">
      <h2>决策管理</h2>
      <el-button type="primary" @click="showCreateDialog">
        新建决策
      </el-button>
    </div>

    <el-table :data="decisionList" v-loading="loading">
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="type" label="类型">
        <template #default="{ row }">
          <el-tag>{{ getTypeLabel(row.type) }}</el-tag>
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
          <el-button link type="primary" @click="editDecision(row)">编辑</el-button>
          <el-button link type="danger" @click="deleteDecision(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建/编辑对话框 -->
    <el-dialog
      :title="dialogType === 'create' ? '新建决策' : '编辑决策'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入决策标题" />
        </el-form-item>
        
        <el-form-item label="类型" prop="type">
          <el-select v-model="formData.type" placeholder="请选择决策类型">
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
            placeholder="请输入决策描述"
          />
        </el-form-item>

        <el-form-item label="决策选项">
          <div v-for="(option, index) in formData.options" :key="index" class="option-item">
            <el-input v-model="option.title" placeholder="选项标题" />
            <el-input v-model="option.description" placeholder="选项描述" />
            <el-button type="danger" @click="removeOption(index)">删除</el-button>
          </div>
          <el-button type="primary" @click="addOption">添加选项</el-button>
        </el-form-item>

        <el-form-item label="决策标准">
          <div v-for="(criterion, index) in formData.criteria" :key="index" class="criterion-item">
            <el-input v-model="criterion.name" placeholder="标准名称" />
            <el-input-number v-model="criterion.weight" :min="1" :max="5" placeholder="权重" />
            <el-button type="danger" @click="removeCriterion(index)">删除</el-button>
          </div>
          <el-button type="primary" @click="addCriterion">添加标准</el-button>
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

const router = useRouter()
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const formRef = ref<FormInstance>()
const decisionList = ref([])

const typeOptions = [
  { value: 'product', label: '产品决策' },
  { value: 'strategy', label: '战略决策' },
  { value: 'investment', label: '投资决策' }
]

const formData = reactive({
  title: '',
  type: '',
  description: '',
  options: [],
  criteria: []
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  description: [{ required: true, message: '请输入描述', trigger: 'blur' }]
}

// 获取决策列表
const fetchList = async () => {
  loading.value = true
  try {
    // TODO: 调用后端API获取列表
    decisionList.value = []
  } catch (error) {
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

// 显示创建对话框
const showCreateDialog = () => {
  dialogType.value = 'create'
  Object.assign(formData, {
    title: '',
    type: '',
    description: '',
    options: [],
    criteria: []
  })
  dialogVisible.value = true
}

// 添加选项
const addOption = () => {
  formData.options.push({
    title: '',
    description: '',
    pros: [],
    cons: []
  })
}

// 删除选项
const removeOption = (index: number) => {
  formData.options.splice(index, 1)
}

// 添加标准
const addCriterion = () => {
  formData.criteria.push({
    name: '',
    weight: 1
  })
}

// 删除标准
const removeCriterion = (index: number) => {
  formData.criteria.splice(index, 1)
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    submitting.value = true
    
    if (dialogType.value === 'create') {
      // TODO: 调用创建API
      ElMessage.success('创建成功')
    } else {
      // TODO: 调用更新API
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
  router.push(`/decision/${row._id}`)
}

// 编辑
const editDecision = (row: any) => {
  dialogType.value = 'edit'
  Object.assign(formData, row)
  dialogVisible.value = true
}

// 删除
const deleteDecision = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该决策吗？', '提示', {
      type: 'warning'
    })
    
    // TODO: 调用删除API
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

onMounted(() => {
  fetchList()
})
</script>

<style scoped lang="scss">
.decision-list {
  padding: 20px;
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      margin: 0;
    }
  }
  
  .option-item,
  .criterion-item {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
    
    .el-input {
      flex: 1;
    }
  }
}
</style> 