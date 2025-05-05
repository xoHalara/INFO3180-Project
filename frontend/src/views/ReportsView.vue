<template>
  <div class="reports-container">
    <div class="welcome-banner">
      <h1>User Reports</h1>
      <p class="welcome-subtitle">Manage and review user reports</p>
    </div>
    
    <div class="reports-content">
      <!-- Stats Overview -->
      <div class="stats-overview">
        <div class="stat-card">
          <span class="material-icons">assignment</span>
          <div class="stat-info">
            <h3>Total Reports</h3>
            <p>{{ reports.length }}</p>
          </div>
        </div>
        <div class="stat-card">
          <span class="material-icons">warning</span>
          <div class="stat-info">
            <h3>Active Reports</h3>
            <p>{{ reports.filter(r => !r.dismissed).length }}</p>
          </div>
        </div>
        <div class="stat-card">
          <span class="material-icons">check_circle</span>
          <div class="stat-info">
            <h3>Resolved Reports</h3>
            <p>{{ reports.filter(r => r.dismissed).length }}</p>
          </div>
        </div>
      </div>

      <!-- Sorting and Filtering -->
      <div class="controls-section">
        <div class="sorting-controls">
          <div class="sort-group">
            <label for="sort-by">
              <span class="material-icons">sort</span>
              Sort by:
            </label>
            <select v-model="sortBy" id="sort-by" @change="fetchSortedReports" class="sort-select">
              <option value="created_at">Date Created</option>
              <option value="reporter_name">Reporter Name</option>
              <option value="reported_user_name">Reported User Name</option>
              <option value="reason">Reason</option>
            </select>
          </div>
          
          <div class="sort-group">
            <label for="order">
              <span class="material-icons">arrow_upward</span>
              Order:
            </label>
            <select v-model="order" id="order" @change="fetchSortedReports" class="sort-select">
              <option value="desc">Descending</option>
              <option value="asc">Ascending</option>
            </select>
          </div>
        </div>

        <div class="filter-controls">
          <button 
            class="filter-btn" 
            :class="{ active: filterStatus === 'all' }"
            @click="filterStatus = 'all'"
          >
            <span class="material-icons">all_inbox</span>
            All
          </button>
          <button 
            class="filter-btn" 
            :class="{ active: filterStatus === 'active' }"
            @click="filterStatus = 'active'"
          >
            <span class="material-icons">warning</span>
            Active
          </button>
          <button 
            class="filter-btn" 
            :class="{ active: filterStatus === 'resolved' }"
            @click="filterStatus = 'resolved'"
          >
            <span class="material-icons">check_circle</span>
            Resolved
          </button>
        </div>
      </div>
      
      <!-- Loading state -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading reports...</p>
      </div>
      
      <!-- Error message -->
      <div v-if="error" class="error-message">
        <span class="material-icons">error</span>
        {{ error }}
      </div>
      
      <!-- Reports list -->
      <div v-if="!loading && !error" class="reports-list">
        <div v-if="filteredReports.length === 0" class="no-reports">
          <span class="material-icons">assignment</span>
          <p>No reports found.</p>
        </div>
        
        <div v-else class="report-cards">
          <div v-for="report in filteredReports" :key="report.id" class="report-card" :class="{ 'is-dismissed': report.dismissed }">
            <div class="report-header">
              <div class="reporter-info">
                <span class="material-icons">person</span>
                <span class="reporter">Reporter: {{ report.reporter_name }}</span>
              </div>
              <div class="date-info">
                <span class="material-icons">schedule</span>
                <span class="date">{{ formatDate(report.created_at) }}</span>
              </div>
            </div>
            
            <div class="reported-user">
              <span class="material-icons">warning</span>
              <span>Reported User: {{ report.reported_user_name }}</span>
            </div>
            
            <div class="reason">
              <div class="reason-header">
                <span class="material-icons">description</span>
                <strong>Reason:</strong>
              </div>
              <p>{{ report.reason }}</p>
            </div>

            <div class="report-status" v-if="report.dismissed">
              <span class="material-icons">check_circle</span>
              <span>Resolved</span>
            </div>
            
            <div class="report-actions">
              <button class="btn-view-profile" @click="viewProfile(report.reported_user_id)">
                <span class="material-icons">visibility</span>
                View Profile
              </button>
              <button 
                v-if="!report.dismissed"
                class="btn-dismiss" 
                @click="dismissReport(report.id)"
                :disabled="dismissingReport === report.id"
              >
                <span v-if="dismissingReport !== report.id" class="material-icons">check_circle</span>
                <span v-else class="spinner-small"></span>
                {{ dismissingReport === report.id ? 'Dismissing...' : 'Dismiss' }}
              </button>
              <button 
                v-else
                class="btn-restore" 
                @click="restoreReport(report.id)"
                :disabled="restoringReport === report.id"
              >
                <span v-if="restoringReport !== report.id" class="material-icons">restore</span>
                <span v-else class="spinner-small"></span>
                {{ restoringReport === report.id ? 'Restoring...' : 'Restore' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { fetchReports } from '@/api/reports'

const router = useRouter()
const reports = ref([])
const loading = ref(true)
const error = ref('')
const sortBy = ref('created_at')
const order = ref('desc')
const filterStatus = ref('all')
const dismissingReport = ref(null)
const restoringReport = ref(null)

const filteredReports = computed(() => {
  if (filterStatus.value === 'all') return reports.value
  if (filterStatus.value === 'active') return reports.value.filter(r => !r.dismissed)
  if (filterStatus.value === 'resolved') return reports.value.filter(r => r.dismissed)
  return reports.value
})

const fetchSortedReports = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await fetchReports({
      sort_by: sortBy.value,
      order: order.value
    })
    reports.value = response.data
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to fetch reports'
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const viewProfile = (userId) => {
  router.push(`/users/${userId}`)
}

const dismissReport = async (reportId) => {
  dismissingReport.value = reportId
  try {
    // TODO: Implement dismiss functionality
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulated API call
    const report = reports.value.find(r => r.id === reportId)
    if (report) report.dismissed = true
  } catch (err) {
    error.value = 'Failed to dismiss report'
  } finally {
    dismissingReport.value = null
  }
}

const restoreReport = async (reportId) => {
  restoringReport.value = reportId
  try {
    // TODO: Implement restore functionality
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulated API call
    const report = reports.value.find(r => r.id === reportId)
    if (report) report.dismissed = false
  } catch (err) {
    error.value = 'Failed to restore report'
  } finally {
    restoringReport.value = null
  }
}

onMounted(() => {
  fetchSortedReports()
})
</script>

<style scoped>
.reports-container {
  min-height: calc(100vh - 90px);
  background: #f8f9fa;
  padding: 2rem;
}

.welcome-banner {
  text-align: center;
  margin-bottom: 2rem;
  padding: 2rem;
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(56, 249, 215, 0.15);
  width: 90%;
  max-width: 1200px;
  margin: 0 auto 2rem;
}

.welcome-banner h1 {
  color: white;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.welcome-subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.2rem;
}

.reports-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-card .material-icons {
  font-size: 2.5rem;
  color: #43e97b;
}

.stat-info h3 {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}

.stat-info p {
  color: #2c3e50;
  font-size: 1.8rem;
  font-weight: 600;
}

.controls-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.sorting-controls {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
}

.sort-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.sort-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.sort-select {
  padding: 0.5rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #f8fafb;
  color: #2c3e50;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sort-select:hover {
  border-color: #43e97b;
}

.filter-controls {
  display: flex;
  gap: 1rem;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #f8fafb;
  color: #666;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-btn:hover {
  background: #f0f0f0;
}

.filter-btn.active {
  background: #43e97b;
  color: white;
  border-color: #43e97b;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 3rem;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #43e97b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner-small {
  width: 20px;
  height: 20px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #43e97b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: #fee2e2;
  color: #dc2626;
  border-radius: 8px;
  margin: 1rem 0;
}

.no-reports {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  color: #666;
}

.no-reports .material-icons {
  font-size: 3rem;
  color: #9ca3af;
}

.report-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.report-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  position: relative;
}

.report-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.report-card.is-dismissed {
  opacity: 0.7;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.reporter-info, .date-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.reported-user {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #fff5f5;
  border-radius: 8px;
  color: #dc2626;
}

.reason {
  margin-bottom: 1.5rem;
}

.reason-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.reason p {
  color: #4b5563;
  line-height: 1.5;
  padding: 0.75rem;
  background: #f8fafb;
  border-radius: 8px;
}

.report-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #f0fdf4;
  color: #16a34a;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.report-actions {
  display: flex;
  gap: 1rem;
}

.btn-view-profile, .btn-dismiss, .btn-restore {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-view-profile {
  background: #43e97b;
  color: white;
  flex: 1;
}

.btn-view-profile:hover {
  background: #38d16a;
}

.btn-dismiss {
  background: #f3f4f6;
  color: #4b5563;
}

.btn-dismiss:hover {
  background: #e5e7eb;
}

.btn-restore {
  background: #f0fdf4;
  color: #16a34a;
}

.btn-restore:hover {
  background: #dcfce7;
}

.btn-view-profile:disabled, .btn-dismiss:disabled, .btn-restore:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .reports-container {
    padding: 1rem;
  }
  
  .welcome-banner {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .welcome-banner h1 {
    font-size: 2rem;
  }
  
  .stats-overview {
    grid-template-columns: 1fr;
  }
  
  .sorting-controls {
    flex-direction: column;
    gap: 1rem;
  }
  
  .filter-controls {
    flex-wrap: wrap;
  }
  
  .filter-btn {
    flex: 1;
    justify-content: center;
  }
  
  .report-cards {
    grid-template-columns: 1fr;
  }
  
  .report-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .report-actions {
    flex-direction: column;
  }
  
  .btn-view-profile, .btn-dismiss, .btn-restore {
    width: 100%;
    justify-content: center;
  }
}
</style> 