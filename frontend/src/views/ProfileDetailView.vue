<template>
  <div class="profile-detail">
    <main class="main-content">
      <div v-if="loading" class="loading">Loading...</div>
      <div v-else-if="error" class="error-message">{{ error }}</div>
      <div v-else class="profile-card-detail">
        <div class="profile-header">
          <div class="profile-avatar">
            <span v-if="profile.photo">
              <img :src="profile.photo" alt="Profile Photo" />
            </span>
            <span v-else>{{ profile.name ? profile.name[0].toUpperCase() : '?' }}</span>
          </div>
          <div class="profile-info">
            <h2>{{ profile.name }}</h2>
            <div class="profile-meta">
              <span>{{ profile.sex }}</span> | <span>{{ profile.race }}</span> |
              <span>Born {{ profile.birth_year }}</span>
            </div>
            <div class="profile-actions">
              <button class="btn-fav" @click="addToFavourites" :disabled="favLoading">
                <span v-if="!favSuccess">&#10084;</span>
                <span v-else>✔️</span>
                Favourite
              </button>
              <button class="btn-email">Email Profile</button>
              <router-link v-if="user && user.id === profile.user_id" :to="`/profiles/${profile.id}/edit`" class="btn-edit">Edit Profile</router-link>
            </div>
            <div v-if="favError" class="error-message">{{ favError }}</div>
            <div v-if="favSuccess" class="success-message">Added to favourites!</div>
          </div>
        </div>
        <div class="profile-fields">
          <div class="field"><strong>Description:</strong> {{ profile.description }}</div>
          <div class="field"><strong>Parish:</strong> {{ profile.parish }}</div>
          <div class="field"><strong>Biography:</strong> {{ profile.biography }}</div>
          <div class="field"><strong>Height:</strong> {{ profile.height }} inches</div>
          <div class="field"><strong>Favourite Cuisine:</strong> {{ profile.fav_cuisine }}</div>
          <div class="field"><strong>Favourite Colour:</strong> {{ profile.fav_colour }}</div>
          <div class="field">
            <strong>Favourite School Subject:</strong> {{ profile.fav_school_subject }}
          </div>
          <div class="field">
            <strong>Political:</strong> {{ profile.political ? 'Yes' : 'No' }}
          </div>
          <div class="field">
            <strong>Religious:</strong> {{ profile.religious ? 'Yes' : 'No' }}
          </div>
          <div class="field">
            <strong>Family Oriented:</strong> {{ profile.family_oriented ? 'Yes' : 'No' }}
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const profileId = route.params.profileId
const profile = ref({})
const loading = ref(true)
const error = ref('')
const favLoading = ref(false)
const favSuccess = ref(false)
const favError = ref('')
const user = authStore.getUser

const fetchProfile = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await api.get(`/profiles/${profileId}`)
    profile.value = res.data
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load profile.'
  } finally {
    loading.value = false
  }
}

const addToFavourites = async () => {
  favLoading.value = true
  favError.value = ''
  favSuccess.value = false
  try {
    const userId = authStore.getUser?.id
    await api.post(`/profiles/${profile.value.user_id}/favourite`, {})
    favSuccess.value = true
  } catch (err) {
    favError.value = err.response?.data?.message || 'Failed to add to favourites.'
  } finally {
    favLoading.value = false
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 700px;
  margin: 0 auto;
  width: 100%;
}
.profile-card-detail {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.07);
  padding: 2rem 2rem 1.5rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}
.profile-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
}
.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: #388e3c;
  overflow: hidden;
}
.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
.profile-info {
  flex: 1;
}
.profile-meta {
  color: #666;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}
.profile-actions {
  margin-top: 1rem;
  display: flex;
  gap: 1rem;
}
.btn-fav {
  background: #fff;
  color: #e53935;
  border: 1px solid #e53935;
  border-radius: 4px;
  padding: 0.5rem 1.2rem;
  cursor: pointer;
  font-size: 1rem;
  transition:
    background 0.2s,
    color 0.2s;
}
.btn-fav:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.btn-fav:hover:not(:disabled) {
  background: #e53935;
  color: #fff;
}
.btn-email {
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1.2rem;
  cursor: pointer;
  font-size: 1rem;
}
.btn-email:hover {
  background: #388e3c;
}
.btn-edit {
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1.2rem;
  cursor: pointer;
  font-size: 1rem;
}
.btn-edit:hover {
  background: #388e3c;
}
.profile-fields {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.field {
  font-size: 1.05rem;
  color: #222;
}
.error-message {
  color: #d32f2f;
  margin-top: 0.5rem;
  text-align: center;
}
.success-message {
  color: #388e3c;
  margin-top: 0.5rem;
  text-align: center;
}
.loading {
  text-align: center;
  color: #888;
  font-size: 1.2rem;
  margin-top: 2rem;
}
</style>
