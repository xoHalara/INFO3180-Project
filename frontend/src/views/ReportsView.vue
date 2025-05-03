<template>
  <div class="reports-container">
    <h2>User Reports</h2>
    
    <!-- Sorting controls -->
    <div class="sorting-controls">
      <label for="sort-by">Sort by:</label>
      <select v-model="sortBy" id="sort-by" @change="fetchSortedReports">
        <option value="created_at">Date Created</option>
        <option value="reporter_name">Reporter Name</option>
        <option value="reported_user_name">Reported User Name</option>
        <option value="reason">Reason</option>
      </select>
      
      <label for="order">Order:</label>
      <select v-model="order" id="order" @change="fetchSortedReports">
        <option value="desc">Descending</option>
        <option value="asc">Ascending</option>
      </select>
    </div>
    
    <!-- Loading state -->
    <div v-if="loading" class="loading">
      Loading reports...
    </div>
    
    <!-- Error message -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <!-- Reports list -->
    <div v-if="!loading && !error" class="reports-list">
      <div v-if="reports.length === 0" class="no-reports">
        No reports found.
      </div>
      
      <div v-else class="report-cards">
        <div v-for="report in reports" :key="report.id" class="report-card">
          <div class="report-header">
            <span class="reporter">Reporter: {{ report.reporter_name }}</span>
            <span class="date">{{ new Date(report.created_at).toLocaleDateString() }}</span>
          </div>
          <div class="reported-user">
            Reported User: {{ report.reported_user_name }}
          </div>
          <div class="reason">
            <strong>Reason:</strong>
            <p>{{ report.reason }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchReports } from '@/api/reports'

const reports = ref([])
const loading = ref(true)
const error = ref('')
const sortBy = ref('created_at')
const order = ref('desc')

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

onMounted(() => {
  fetchSortedReports()
})
</script>

<style scoped>
.reports-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.sorting-controls {
  margin-bottom: 20px;
  display: flex;
  gap: 20px;
  align-items: center;
}

.sorting-controls select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.report-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.report-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.report-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-size: 0.9em;
  color: #666;
}

.reported-user {
  font-weight: bold;
  margin-bottom: 12px;
}

.reason {
  font-size: 0.95em;
  line-height: 1.4;
}

.reason p {
  margin-top: 4px;
}

.loading, .error-message, .no-reports {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error-message {
  color: #dc3545;
}
</style> 