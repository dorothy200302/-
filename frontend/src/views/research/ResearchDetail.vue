<template>
  <div class="research-detail">
    <div class="header">
      <h2>{{ research.title }}</h2>
      <div class="status">
        <el-tag :type="getStatusType(research.status)">
          {{ getStatusLabel(research.status) }}
        </el-tag>
      </div>
    </div>

    <el-descriptions class="mt-4" :column="2" border>
      <el-descriptions-item label="类型">
        {{ getTypeLabel(research.research_type) }}
      </el-descriptions-item>
      <el-descriptions-item label="创建时间">
        {{ research.create_time }}
      </el-descriptions-item>
      <el-descriptions-item label="描述" :span="2">
        {{ research.description }}
      </el-descriptions-item>
    </el-descriptions>

    <div class="section mt-4">
      <h3>调研发现</h3>
      <div v-for="finding in research.findings" :key="finding.id" class="finding-card">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>{{ finding.title }}</span>
              <span class="source">来源: {{ finding.source }}</span>
            </div>
          </template>
          <p>{{ finding.content }}</p>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const research = ref<any>({})

// ... 实现其他逻辑
</script> 