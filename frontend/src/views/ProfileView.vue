<template>
  <div class="profile">
    <UserProfileView :user-id="userId" :is-own-profile="true" v-if="hasProfile" />
    <div v-else>
      <main class="main-content">
        <div class="welcome-banner">
          <h1>Welcome, {{ user?.name || user?.username }}!</h1>
          <p class="welcome-subtitle">Create your profile to start matching</p>
        </div>
        
        <div class="profile-section">
          <div class="profile-info">
            <h2>Your Account</h2>
            <div class="info-card">
              <div class="info-group">
                <span class="material-icons">person</span>
                <div class="info-content">
                  <label>Username</label>
                  <p>{{ user?.username }}</p>
                </div>
              </div>
              <div class="info-group">
                <span class="material-icons">badge</span>
                <div class="info-content">
                  <label>Name</label>
                  <p>{{ user?.name || 'Not set' }}</p>
                </div>
              </div>
            </div>
            
            <div class="create-profile-section">
              <h3>Ready to find your match?</h3>
              <p>Create your profile to start connecting with others</p>
              <button class="btn-primary" @click="goToCreateProfile">
                <span class="material-icons">add_circle</span>
                Create New Profile
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/api'
import UserProfileView from './UserProfileView.vue'

const router = useRouter()
const authStore = useAuthStore()
const user = computed(() => authStore.getUser)
const userId = computed(() => user.value?.id)
const hasProfile = ref(false)

const checkHasProfile = async () => {
  if (!userId.value) {
    hasProfile.value = false
    return
  }
  try {
    const res = await api.get(`/profiles/?user_id=${userId.value}`)
    hasProfile.value = Array.isArray(res.data) && res.data.length > 0
  } catch {
    hasProfile.value = false
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const goToCreateProfile = () => {
  router.push('/profiles/new')
}

onMounted(() => {
  checkHasProfile()
})
</script>

<style scoped>
.profile {
  min-height: calc(100vh - 90px);
  display: flex;
  flex-direction: column;
  width: 100vw;
  background: #f8f9fa;
}

.main-content {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 2rem;
  box-sizing: border-box;
}

.welcome-banner {
  text-align: center;
  margin-bottom: 2rem;
  padding: 2rem;
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(56, 249, 215, 0.15);
  width: 90%;
  max-width: 1000px;
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

.profile-section {
  background-color: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  margin-top: 1.5rem;
  width: 90%;
  max-width: 1000px;
  box-sizing: border-box;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-info h2 {
  color: #2c3e50;
  font-size: 1.8rem;
  text-align: center;
  margin-bottom: 1rem;
}

.info-card {
  background: #f8fafb;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.info-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.info-group:last-child {
  border-bottom: none;
}

.info-group .material-icons {
  font-size: 1.5rem;
  color: #43e97b;
}

.info-content {
  flex: 1;
}

.info-content label {
  display: block;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.info-content p {
  font-size: 1.1rem;
  color: #2c3e50;
  font-weight: 500;
}

.create-profile-section {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(67, 233, 123, 0.1) 0%, rgba(56, 249, 215, 0.1) 100%);
  border-radius: 12px;
  border: 1px solid rgba(67, 233, 123, 0.2);
}

.create-profile-section h3 {
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.create-profile-section p {
  color: #666;
  margin-bottom: 1.5rem;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: none;
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(67, 233, 123, 0.2);
}

.btn-primary .material-icons {
  font-size: 1.2rem;
}

@media (max-width: 900px) {
  .main-content {
    padding: 1rem;
  }
  
  .welcome-banner {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .welcome-banner h1 {
    font-size: 2rem;
  }
  
  .profile-section {
    width: 95%;
    padding: 1.5rem;
  }
}

@media (max-width: 600px) {
  .main-content {
    padding: 0.5rem;
  }
  
  .welcome-banner {
    padding: 1rem;
    margin-bottom: 1rem;
  }
  
  .welcome-banner h1 {
    font-size: 1.8rem;
  }
  
  .profile-section {
    padding: 1rem;
    width: 100%;
  }
  
  .info-group {
    padding: 0.75rem;
  }
  
  .create-profile-section {
    padding: 1.5rem;
  }
}
</style>
