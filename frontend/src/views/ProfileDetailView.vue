<template>
  <div class="profile-detail">
    <main class="main-content">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading profile...</p>
      </div>
      
      <div v-else-if="error" class="error-message">
        <span class="material-icons">error</span>
        {{ error }}
      </div>
      
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
              <span class="meta-item">
                <span class="material-icons">person</span>
                {{ profile.sex }}
              </span>
              <span class="meta-item">
                <span class="material-icons">public</span>
                {{ profile.race }}
              </span>
              <span class="meta-item">
                <span class="material-icons">calendar_today</span>
                Born {{ profile.birth_year }}
              </span>
            </div>
            <div class="profile-actions">
              <button 
                class="btn-fav" 
                @click="addToFavourites" 
                :disabled="favLoading"
                :class="{ 'is-favourited': favSuccess }"
              >
                <span class="material-icons">{{ favSuccess ? 'favorite' : 'favorite_border' }}</span>
                {{ favSuccess ? 'Favourited' : 'Favourite' }}
              </button>
              <button class="btn-email">
                <span class="material-icons">email</span>
                Email Profile
              </button>
              <router-link 
                v-if="user && user.id === profile.user_id" 
                :to="`/profiles/${profile.id}/edit`" 
                class="btn-edit"
              >
                <span class="material-icons">edit</span>
                Edit Profile
              </router-link>
            </div>
            <div v-if="favError" class="error-message">
              <span class="material-icons">error</span>
              {{ favError }}
            </div>
            <div v-if="favSuccess" class="success-message">
              <span class="material-icons">check_circle</span>
              Added to favourites!
            </div>
          </div>
        </div>
        
        <div class="profile-fields">
          <div class="field-group">
            <h3>About</h3>
            <div class="field">
              <div class="field-label">
                <span class="material-icons">description</span>
                <strong>Description</strong>
              </div>
              <p>{{ profile.description }}</p>
            </div>
            <div class="field">
              <div class="field-label">
                <span class="material-icons">book</span>
                <strong>Biography</strong>
              </div>
              <p>{{ profile.biography }}</p>
            </div>
          </div>
          
          <div class="field-group">
            <h3>Location & Physical</h3>
            <div class="field">
              <div class="field-label">
                <span class="material-icons">location_on</span>
                <strong>Parish</strong>
              </div>
              <p>{{ profile.parish }}</p>
            </div>
            <div class="field">
              <div class="field-label">
                <span class="material-icons">height</span>
                <strong>Height</strong>
              </div>
              <p>{{ profile.height }} inches</p>
            </div>
          </div>
          
          <div class="field-group">
            <h3>Preferences</h3>
            <div class="field">
              <div class="field-label">
                <span class="material-icons">restaurant</span>
                <strong>Favourite Cuisine</strong>
              </div>
              <p>{{ profile.fav_cuisine }}</p>
            </div>
            <div class="field">
              <div class="field-label">
                <span class="material-icons">palette</span>
                <strong>Favourite Colour</strong>
              </div>
              <p>{{ profile.fav_colour }}</p>
            </div>
            <div class="field">
              <div class="field-label">
                <span class="material-icons">school</span>
                <strong>Favourite School Subject</strong>
              </div>
              <p>{{ profile.fav_school_subject }}</p>
            </div>
          </div>
          
          <div class="field-group">
            <h3>Personal Traits</h3>
            <div class="traits-grid">
              <div class="trait-item" :class="{ 'is-true': profile.political }">
                <span class="material-icons">{{ profile.political ? 'check_circle' : 'cancel' }}</span>
                <span>Political</span>
              </div>
              <div class="trait-item" :class="{ 'is-true': profile.religious }">
                <span class="material-icons">{{ profile.religious ? 'check_circle' : 'cancel' }}</span>
                <span>Religious</span>
              </div>
              <div class="trait-item" :class="{ 'is-true': profile.family_oriented }">
                <span class="material-icons">{{ profile.family_oriented ? 'check_circle' : 'cancel' }}</span>
                <span>Family Oriented</span>
              </div>
            </div>
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
.profile-detail {
  min-height: calc(100vh - 90px);
  background: #f8f9fa;
  padding: 2rem;
}

.main-content {
  max-width: 1000px;
  margin: 0 auto;
  width: 100%;
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

.profile-card-detail {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-header {
  display: flex;
  gap: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #f0f0f0;
}

.profile-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: white;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(67, 233, 123, 0.2);
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

.profile-info h2 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.profile-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 1rem;
}

.meta-item .material-icons {
  color: #43e97b;
}

.profile-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-fav, .btn-email, .btn-edit {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-fav {
  background: rgba(229, 57, 53, 0.1);
  color: #e53935;
  border: none;
}

.btn-fav:hover:not(:disabled) {
  background: rgba(229, 57, 53, 0.2);
  transform: translateY(-2px);
}

.btn-fav.is-favourited {
  background: #e53935;
  color: white;
}

.btn-email {
  background: #43e97b;
  color: white;
  border: none;
}

.btn-email:hover {
  background: #38d16a;
  transform: translateY(-2px);
}

.btn-edit {
  background: #f3f4f6;
  color: #4b5563;
  border: none;
  text-decoration: none;
}

.btn-edit:hover {
  background: #e5e7eb;
  transform: translateY(-2px);
}

.success-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #43e97b;
  margin-top: 1rem;
  padding: 0.75rem;
  background: rgba(67, 233, 123, 0.1);
  border-radius: 8px;
}

.profile-fields {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.field-group {
  background: #f8fafb;
  border-radius: 12px;
  padding: 1.5rem;
}

.field-group h3 {
  color: #2c3e50;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.field {
  margin-bottom: 1.5rem;
}

.field:last-child {
  margin-bottom: 0;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.field-label .material-icons {
  color: #43e97b;
}

.field p {
  color: #4b5563;
  line-height: 1.6;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
  margin: 0;
}

.traits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.trait-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
  color: #666;
}

.trait-item.is-true {
  color: #43e97b;
}

.trait-item .material-icons {
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .profile-detail {
    padding: 1rem;
  }
  
  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 1.5rem;
  }
  
  .profile-meta {
    justify-content: center;
  }
  
  .profile-actions {
    flex-direction: column;
  }
  
  .btn-fav, .btn-email, .btn-edit {
    width: 100%;
    justify-content: center;
  }
  
  .traits-grid {
    grid-template-columns: 1fr;
  }
}
</style>
