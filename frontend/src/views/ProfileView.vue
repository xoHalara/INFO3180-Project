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
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.profile-section {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
}

.profile-info {
  max-width: 600px;
}

.info-group {
  margin: 1rem 0;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.info-group label {
  font-weight: bold;
  color: #666;
  display: block;
  margin-bottom: 0.5rem;
}

.info-group p {
  margin: 0;
  color: #333;
}

.btn-primary {
  background-color: #4caf50;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 1rem;
}

.btn-primary:hover {
  background-color: #388e3c;
}
</style>
