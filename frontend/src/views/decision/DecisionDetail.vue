<template>
  <div class="decision-detail">
    <div class="header">
      <h2>{{ decision.title }}</h2>
      <div class="status">
        <el-tag :type="getStatusType(decision.status)">
          {{ getStatusLabel(decision.status) }}
        </el-tag>
      </div>
    </div>

    <el-descriptions class="mt-4" :column="2" border>
      <el-descriptions-item label="类型">
        {{ getTypeLabel(decision.type) }}
      </el-descriptions-item>
      <el-descriptions-item label="创建时间">
        {{ decision.create_time }}
      </el-descriptions-item>
      <el-descriptions-item label="描述" :span="2">
        {{ decision.description }}
      </el-descriptions-item>
    </el-descriptions>

    <div class="section mt-4">
      <h3>决策选项</h3>
      <el-row :gutter="20">
        <el-col :span="8" v-for="option in decision.options" :key="option.title">
          <el-card class="option-card">
            <template #header>
              <div class="card-header">
                <span>{{ option.title }}</span>
                <el-tag :type="option.isRecommended ? 'success' : ''">
                  {{ option.isRecommended ? '推荐' : '备选' }}
                </el-tag>
              </div>
            </template>
            <p class="description">{{ option.description }}</p>
            <div class="pros-cons">
              <div class="pros">
                <h4>优势</h4>
                <ul>
                  <li v-for="(pro, index) in option.pros" :key="index">
                    {{ pro }}
                  </li>
                </ul>
              </div>
              <div class="cons">
                <h4>劣势</h4>
                <ul>
                  <li v-for="(con, index) in option.cons" :key="index">
                    {{ con }}
                  </li>
                </ul>
              </div>
            </div>
            <div class="scores mt-2">
              <h4>评分</h4>
              <el-table :data="getScoresList(option.criteria_scores)" border>
                <el-table-column prop="criterion" label="标准" />
                <el-table-column prop="score" label="得分">
                  <template #default="{ row }">
                    <el-rate v-model="row.score" disabled />
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="section mt-4">
      <h3>决策分析</h3>
      <el-card>
        <template #header>
          <div class="card-header">
            <span>AI 分析建议</span>
            <el-button type="primary" @click="refreshAnalysis">
              刷新分析
            </el-button>
          </div>
        </template>
        <div class="analysis-content">
          <div class="recommendation">
            <h4>推荐方案</h4>
            <p>{{ decision.analysis?.recommendation?.best_option }}</p>
            <p class="confidence">
              置信度: {{ decision.analysis?.recommendation?.confidence }}
            </p>
            <p class="reasoning">
              {{ decision.analysis?.recommendation?.reasoning }}
            </p>
          </div>
          <div class="risk-analysis mt-4">
            <h4>风险分析</h4>
            <el-table :data="decision.analysis?.risk_analysis" border>
              <el-table-column prop="factor" label="风险因素" />
              <el-table-column prop="level" label="风险等级">
                <template #default="{ row }">
                  <el-tag :type="getRiskLevelType(row.level)">
                    {{ row.level }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="mitigation" label="应对措施" />
            </el-table>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const decision = ref<any>({})
const loading = ref(false)

const fetchDecisionDetail = async () => {
  loading.value = true
  try {
    // TODO: 调用后端API获取决策详情
    decision.value = {
      title: '产品定价决策',
      type: 'product',
      status: 'in_progress',
      description: '关于新产品定价策略的决策分析',
      create_time: '2024-01-05',
      options: [
        {
          title: '高端定价',
          description: '采用高端定价策略',
          isRecommended: true,
          pros: ['利润率高', '品牌形象好'],
          cons: ['市场规模受限', '竞争压力大'],
          criteria_scores: {
            '利润率': 5,
            '市场规模': 3,
            '竞争风险': 4
          }
        },
        {
          title: '中端定价',
          description: '采用中端定价策略',
          isRecommended: false,
          pros: ['市场规模大', '竞争优势明显'],
          cons: ['利润率一般', '品牌提升困难'],
          criteria_scores: {
            '利润率': 3,
            '市场规模': 4,
            '竞争风险': 3
          }
        }
      ],
      analysis: {
        recommendation: {
          best_option: '高端定价',
          confidence: '高',
          reasoning: '基于当前市场环境和产品特性，高端定价策略更有利于品牌建设和长期发展。'
        },
        risk_analysis: [
          {
            factor: '市场接受度',
            level: '中',
            mitigation: '加强产品价值传递，强化品牌营销'
          },
          {
            factor: '竞争对手反应',
            level: '高',
            mitigation: '准备替代方案，保持策略灵活性'
          }
        ]
      }
    }
  } catch (error) {
    ElMessage.error('获取决策详情失败')
  } finally {
    loading.value = false
  }
}

const refreshAnalysis = async () => {
  try {
    // TODO: 调用后端API刷新分析
    ElMessage.success('分析已更新')
  } catch (error) {
    ElMessage.error('更新分析失败')
  }
}

const getTypeLabel = (type: string) => {
  const typeMap: Record<string, string> = {
    product: '产品决策',
    strategy: '战略决策',
    investment: '投资决策'
  }
  return typeMap[type] || type
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

const getRiskLevelType = (level: string) => {
  const typeMap: Record<string, string> = {
    低: 'success',
    中: 'warning',
    高: 'danger'
  }
  return typeMap[level] || ''
}

const getScoresList = (scores: Record<string, number>) => {
  return Object.entries(scores).map(([criterion, score]) => ({
    criterion,
    score
  }))
}

onMounted(() => {
  fetchDecisionDetail()
})
</script>

<style scoped lang="scss">
.decision-detail {
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

  .section {
    margin-top: 30px;

    h3 {
      margin-bottom: 20px;
    }
  }

  .option-card {
    margin-bottom: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .description {
      color: #666;
      margin-bottom: 15px;
    }

    .pros-cons {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;

      h4 {
        margin-bottom: 10px;
      }

      ul {
        padding-left: 20px;
        margin: 0;
      }
    }
  }

  .analysis-content {
    .recommendation {
      .confidence {
        color: #409EFF;
        font-weight: bold;
      }

      .reasoning {
        color: #666;
        margin-top: 10px;
      }
    }
  }

  .mt-2 {
    margin-top: 10px;
  }

  .mt-4 {
    margin-top: 20px;
  }
}
</style> 