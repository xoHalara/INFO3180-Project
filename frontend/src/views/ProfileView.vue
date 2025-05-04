<template>
  <div class="profile">
    <UserProfileView :user-id="userId" :is-own-profile="true" v-if="hasProfile" />
    <div v-else>
      <main class="main-content">
        <h1>Welcome, {{ user?.name || user?.username }}</h1>
        <div class="profile-section">
          <div class="profile-info">
            <h2>Your Account</h2>
            <div class="info-group">
              <label>Username:</label>
              <p>{{ user?.username }}</p>
            </div>
            <div class="info-group">
              <label>Name:</label>
              <p>{{ user?.name }}</p>
            </div>
            <button class="btn-primary" @click="goToCreateProfile">Create New Profile</button>
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

.content-section {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-top: 1rem;
  width: 90%;
  max-width: 1000px;
  box-sizing: border-box;
}

.page-content-horizontal {
  display: flex;
  flex-direction: row;
  gap: 2rem;
  width: 90%;
  max-width: 1200px;
  margin-top: 2rem;
  justify-content: center;
}

.page-content-horizontal .content-section {
  margin-top: 0;
  flex: 1 1 0;
  max-width: 1000px;
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
}

.profile-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #388e3c;
  margin-bottom: 1.5rem;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.profile-name {
  font-size: 2rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 0.5rem;
}

.profile-meta {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.profile-bio {
  font-size: 1.1rem;
  color: #444;
  line-height: 1.6;
  text-align: center;
  max-width: 600px;
  margin: 0 auto 2rem;
}

.profile-actions {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 1rem;
}

.edit-link {
  color: #43e97b;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.2s ease;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  background: rgba(67, 233, 123, 0.1);
}

.edit-link:hover {
  color: #388e3c;
  background: rgba(67, 233, 123, 0.2);
  text-decoration: none;
}

.fav-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
  padding: 1rem;
  width: 90%;
  max-width: 1200px;
}

.fav-card {
  background: linear-gradient(90deg, #f8fffc 0%, #e0f7fa 100%);
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(56, 249, 215, 0.07);
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 220px;
  transition: all 0.3s ease;
  border: 1px solid rgba(76, 175, 80, 0.1);
}

.fav-card:hover {
  box-shadow: 0 8px 32px rgba(56, 249, 215, 0.15);
  transform: translateY(-4px);
  border-color: rgba(76, 175, 80, 0.2);
}

.fav-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: #388e3c;
  margin-bottom: 1.5rem;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.fav-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.fav-details {
  text-align: center;
  width: 100%;
}

.fav-name {
  font-size: 1.35rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 0.5rem;
}

.fav-meta {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.fav-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin-top: 1rem;
}

.details-link {
  color: #43e97b;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.2s ease;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  background: rgba(67, 233, 123, 0.1);
}

.details-link:hover {
  color: #388e3c;
  background: rgba(67, 233, 123, 0.2);
  text-decoration: none;
}

.btn-remove {
  background: none;
  border: none;
  color: #e53935;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0.5rem;
  border-radius: 50%;
  outline: none;
  background: rgba(229, 57, 53, 0.1);
}

.btn-remove:hover {
  color: #b71c1c;
  transform: scale(1.15);
  background: rgba(229, 57, 53, 0.2);
}

.error-message {
  color: #d32f2f;
  margin-top: 1rem;
  text-align: center;
}

@media (max-width: 900px) {
  .main-content {
    padding: 1rem;
  }
  
  .content-section {
    width: 95%;
  }
  
  .page-content-horizontal {
    flex-direction: column;
    gap: 1rem;
    align-items: center;
    width: 95%;
  }
  
  .page-content-horizontal .content-section {
    width: 100%;
  }
  
  .fav-list {
    width: 95%;
  }
}

@media (max-width: 600px) {
  .main-content {
    padding: 0.5rem;
  }
  
  .content-section {
    padding: 1rem;
    width: 100%;
  }
  
  .page-content-horizontal {
    gap: 0.5rem;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .fav-list {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    width: 100%;
    padding: 0 1rem;
  }
  
  .fav-card {
    padding: 1.5rem 1rem;
    width: 100%;
  }
}
</style>
