<template>
    <div class="decision-support-container">
      <h1 class="page-title">项目地平线：决策支持与实施</h1>
      
      <div class="card-grid">
        <div class="card">
          <h2 class="card-title">项目概览</h2>
          <p class="card-description">当前状态和关键指标</p>
          <div class="progress-container">
            <div class="progress-header">
              <span>整体进度</span>
              <span>{{ progress }}%</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
            </div>
          </div>
          <div class="status-indicators">
            <div class="status-item">
              <div class="status-dot on-track"></div>
              <span>正常</span>
            </div>
            <div class="status-item">
              <div class="status-dot at-risk"></div>
              <span>风险</span>
            </div>
            <div class="status-item">
              <div class="status-dot delayed"></div>
              <span>延迟</span>
            </div>
          </div>
        </div>
  
        <div class="card">
          <h2 class="card-title">决策支持</h2>
          <p class="card-description">辅助决策工具</p>
          <div class="tabs">
            <button 
              :class="['tab-button', { active: activeTab === 'analysis' }]"
              @click="activeTab = 'analysis'"
            >
              分析
            </button>
            <button 
              :class="['tab-button', { active: activeTab === 'simulation' }]"
              @click="activeTab = 'simulation'"
            >
              模拟
            </button>
          </div>
          <div v-if="activeTab === 'analysis'" class="tab-content">
            <p>运行数据分析以支持决策。</p>
            <button class="action-button">开始分析</button>
          </div>
          <div v-else class="tab-content">
            <p>模拟场景以预测结果。</p>
            <button class="action-button">运行模拟</button>
          </div>
        </div>
  
        <div class="card">
          <h2 class="card-title">快速操作</h2>
          <p class="card-description">常用工具和报告</p>
          <div class="quick-actions">
            <button class="action-button outline">生成报告</button>
            <button class="action-button outline">团队会议</button>
            <button class="action-button outline">更新预测</button>
            <button class="action-button outline">风险评估</button>
          </div>
        </div>
      </div>
  
      <div class="card-grid">
        <div class="card">
          <h2 class="card-title">实施进度</h2>
          <p class="card-description">任务完成状态</p>
          <div class="chart-container">
            <div v-for="(task, index) in projectData" :key="index" class="chart-bar">
              <div class="bar-label">{{ task.name }}</div>
              <div class="bar-track">
                <div class="bar-fill" :style="{ width: `${task.completed}%` }"></div>
              </div>
              <div class="bar-value">{{ task.completed }}%</div>
            </div>
          </div>
        </div>
  
        <div class="card">
          <h2 class="card-title">添加新任务</h2>
          <p class="card-description">为项目创建新任务</p>
          <form @submit.prevent="addTask" class="task-form">
            <div class="form-group">
              <label for="taskName">任务名称</label>
              <input id="taskName" v-model="newTask.name" type="text" placeholder="输入任务名称" required>
            </div>
            <div class="form-group">
              <label for="taskDescription">描述</label>
              <input id="taskDescription" v-model="newTask.description" type="text" placeholder="任务简要描述" required>
            </div>
            <div class="form-group">
              <label for="taskAssignee">负责人</label>
              <input id="taskAssignee" v-model="newTask.assignee" type="text" placeholder="分配给团队成员" required>
            </div>
            <button type="submit" class="action-button">添加任务</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive } from 'vue'
  
  const progress = ref(68)
  const activeTab = ref('analysis')
  
  const projectData = reactive([
    { name: '任务 1', completed: 65, remaining: 35 },
    { name: '任务 2', completed: 40, remaining: 60 },
    { name: '任务 3', completed: 80, remaining: 20 },
    { name: '任务 4', completed: 20, remaining: 80 },
    { name: '任务 5', completed: 50, remaining: 50 },
  ])
  
  const newTask = reactive({
    name: '',
    description: '',
    assignee: ''
  })
  
  const addTask = () => {
    projectData.push({
      name: newTask.name,
      completed: 0,
      remaining: 100
    })
    newTask.name = ''
    newTask.description = ''
    newTask.assignee = ''
  }
  </script>
  
  <style scoped>
  .decision-support-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    font-family: Arial, sans-serif;
  }
  
  .page-title {
    font-size: 2rem;
    color: #333;
    margin-bottom: 2rem;
  }
  
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .card-title {
    font-size: 1.25rem;
    color: #333;
    margin-bottom: 0.5rem;
  }
  
  .card-description {
    color: #666;
    font-size: 0.875rem;
    margin-bottom: 1rem;
  }
  
  .progress-container {
    margin-bottom: 1rem;
  }
  
  .progress-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }
  
  .progress-bar {
    height: 8px;
    background-color: #e0e0e0;
    border-radius: 4px;
    overflow: hidden;
  }
  
  .progress-fill {
    height: 100%;
    background-color: #4caf50;
    transition: width 0.3s ease;
  }
  
  .status-indicators {
    display: flex;
    justify-content: space-between;
  }
  
  .status-item {
    display: flex;
    align-items: center;
  }
  
  .status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 0.5rem;
  }
  
  .on-track { background-color: #4caf50; }
  .at-risk { background-color: #ffc107; }
  .delayed { background-color: #f44336; }
  
  .tabs {
    display: flex;
    margin-bottom: 1rem;
  }
  
  .tab-button {
    flex: 1;
    padding: 0.5rem;
    border: none;
    background: none;
    cursor: pointer;
    border-bottom: 2px solid transparent;
  }
  
  .tab-button.active {
    border-bottom-color: #2196f3;
    color: #2196f3;
  }
  
  .tab-content {
    margin-top: 1rem;
  }
  
  .action-button {
    width: 100%;
    padding: 0.75rem;
    border: none;
    border-radius: 4px;
    background-color: #2196f3;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .action-button:hover {
    background-color: #1976d2;
  }
  
  .action-button.outline {
    background-color: transparent;
    border: 1px solid #2196f3;
    color: #2196f3;
  }
  
  .action-button.outline:hover {
    background-color: rgba(33, 150, 243, 0.1);
  }
  
  .quick-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
  }
  
  .chart-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .chart-bar {
    display: flex;
    align-items: center;
  }
  
  .bar-label {
    width: 60px;
    margin-right: 1rem;
  }
  
  .bar-track {
    flex-grow: 1;
    height: 8px;
    background-color: #e0e0e0;
    border-radius: 4px;
    overflow: hidden;
  }
  
  .bar-fill {
    height: 100%;
    background-color: #2196f3;
  }
  
  .bar-value {
    width: 40px;
    text-align: right;
    margin-left: 1rem;
  }
  
  .task-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
  }
  
  .form-group label {
    margin-bottom: 0.25rem;
    color: #666;
  }
  
  .form-group input {
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  </style>