<template>
  <div class="user-profile-view">
    <div class="profile-header-bg">
      <div class="profile-header">
        <div class="avatar-lg">
          {{ userData.name ? userData.name[0].toUpperCase() : '?' }}
        </div>
        <div class="user-main-info">
          <h2>{{ userData.name || userData.username }}</h2>
          <p v-if="userData.username" class="username">@{{ userData.username }}</p>
          <p v-if="userData.email" class="email">{{ userData.email }}</p>
        </div>
        <div class="profile-actions">
          <router-link
            v-if="authStore.getUser && String(authStore.getUser.id) === String(userId)"
            to="/profiles/new"
            class="btn-fab"
            title="Add Profile"
          >
            <span class="material-icons">add</span>
          </router-link>
          <div v-if="authStore.getUser && String(authStore.getUser.id) === String(userId)" class="more-options">
            <button class="btn-more" @click="toggleDropdown" ref="moreButton">
              <span class="material-icons">more_vert</span>
            </button>
            <div v-if="showDropdown" class="dropdown-menu">
              <button class="dropdown-item" @click="editAccount">
                <span class="material-icons">edit</span>
                Edit Account
              </button>
              <button class="dropdown-item delete" @click="confirmDelete">
                <span class="material-icons">delete</span>
                Delete Account
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-title">
        <span class="material-icons section-icon">badge</span>
        User's Profiles
      </div>
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading profiles...</p>
      </div>
      <div v-else-if="error" class="error-message">
        <span class="material-icons">error</span>
        {{ error }}
      </div>
      <div v-else-if="profiles.length === 0" class="empty-state">
        <img src="https://cdn.jsdelivr.net/gh/edent/SuperTinyIcons/images/svg/user.svg" alt="No profiles" class="empty-illustration" />
        <div>No profiles found for this user.</div>
        <router-link
          v-if="authStore.getUser && String(authStore.getUser.id) === String(userId)"
          to="/profiles/new"
          class="btn-primary"
        >
          <span class="material-icons">add_circle</span>
          Create a profile
        </router-link>
      </div>
      <div v-else class="profile-cards">
        <div v-for="profile in profiles" :key="profile.id" class="profile-card">
          <div class="profile-card-header">
            <div class="avatar">{{ profile.name ? profile.name[0].toUpperCase() : '?' }}</div>
            <div class="profile-card-info">
              <div class="profile-name">{{ profile.name }}</div>
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
            </div>
          </div>
          <div class="profile-card-actions">
            <router-link :to="`/profiles/${profile.id}`" class="btn-view">
              <span class="material-icons">visibility</span>
              View Details
            </router-link>
            <button 
              v-if="authStore.getUser && String(authStore.getUser.id) === String(userId)"
              class="btn-edit"
              @click="editProfile(profile.id)"
            >
              <span class="material-icons">edit</span>
              Edit
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-title">
        <span class="material-icons section-icon">favorite</span>
        Users Favourited by This User
      </div>
      <div v-if="loadingFavourites" class="loading-state">
        <div class="spinner"></div>
        <p>Loading favourites...</p>
      </div>
      <div v-else-if="userFavourites.length === 0" class="empty-state">
        <img src="https://cdn.jsdelivr.net/gh/edent/SuperTinyIcons/images/svg/heart.svg" alt="No favourites" class="empty-illustration" />
        <div>This user has not favourited any users yet.</div>
      </div>
      <div v-else class="fav-cards">
        <div v-for="fav in userFavourites" :key="fav.id" class="fav-card">
          <router-link :to="`/users/${fav.id}`" class="fav-link">
            <div class="avatar-sm">{{ fav.name ? fav.name[0].toUpperCase() : '?' }}</div>
            <div class="fav-details">
              <div class="fav-name">{{ fav.name || fav.username }}</div>
              <div class="fav-meta">
                <span v-if="fav.username">@{{ fav.username }}</span>
                <span v-if="fav.email">&nbsp;·&nbsp;{{ fav.email }}</span>
              </div>
            </div>
            <span class="material-icons">chevron_right</span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/api'
import { fetchAllProfiles, getUserFavourites } from '@/api/profile'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const userId = route.params.userId

const userData = ref({})
const profiles = ref([])
const userFavourites = ref([])
const loading = ref(true)
const loadingFavourites = ref(true)
const error = ref('')
const showDropdown = ref(false)
const moreButton = ref(null)

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const handleClickOutside = (event) => {
  if (moreButton.value && !moreButton.value.contains(event.target)) {
    showDropdown.value = false
  }
}

const editAccount = () => {
  router.push(`/users/${userId}/edit`)
}

const confirmDelete = () => {
  if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
    deleteAccount()
  }
}

const deleteAccount = async () => {
  try {
    await api.delete(`/users/${userId}`)
    authStore.logout()
    router.push('/login')
  } catch (err) {
    error.value = 'Failed to delete account. Please try again.'
  }
}

const fetchUserData = async () => {
  try {
    const res = await api.get(`/users/${userId}`)
    userData.value = res.data
  } catch (err) {
    error.value = 'Failed to fetch user info.'
  }
}

const fetchUserProfiles = async () => {
  try {
    const res = await fetchAllProfiles()
    profiles.value = res.data.filter(p => String(p.user_id_fk ?? p.user_id) === String(userId))
  } catch (err) {
    error.value = 'Failed to fetch user profiles.'
  }
}

const fetchUserFavourites = async () => {
  loadingFavourites.value = true
  try {
    const res = await getUserFavourites(userId)
    userFavourites.value = res.data
  } catch {
    userFavourites.value = []
  } finally {
    loadingFavourites.value = false
  }
}

const editProfile = (profileId) => {
  router.push(`/profiles/${profileId}/edit`)
}

onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  loading.value = true
  error.value = ''
  await Promise.all([
    fetchUserData(),
    fetchUserProfiles(),
    fetchUserFavourites()
  ])
  loading.value = false
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.user-profile-view {
  padding: 0 0 3rem 0;
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.profile-header-bg {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  border-radius: 0 0 24px 24px;
  padding: 2.5rem 1rem 2rem 1rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 24px rgba(56, 249, 215, 0.15);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  max-width: 900px;
  margin: 0 auto;
  position: relative;
}

.avatar-lg {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #43e97b;
  font-weight: bold;
  box-shadow: 0 4px 16px rgba(67, 233, 123, 0.2);
}

.user-main-info {
  flex: 1;
}

.user-main-info h2 {
  margin-bottom: 0.5rem;
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.username {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.2rem;
  margin-bottom: 0.3rem;
}

.email {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
}

.btn-fab {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  background: white;
  color: #43e97b;
  border: none;
  border-radius: 50%;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  box-shadow: 0 4px 16px rgba(67, 233, 123, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 2;
}

.btn-fab:hover {
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 6px 20px rgba(67, 233, 123, 0.3);
}

.section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  font-size: 1.4rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.section-icon {
  font-size: 1.6rem;
  color: #43e97b;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(67, 233, 123, 0.1);
  border-left-color: #43e97b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 3rem 2rem;
  color: #666;
  text-align: center;
}

.empty-illustration {
  width: 64px;
  height: 64px;
  opacity: 0.7;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #43e97b;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-primary:hover {
  background: #38d16a;
  transform: translateY(-2px);
}

.profile-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.profile-card {
  background: #f8fafb;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  transition: all 0.3s ease;
}

.profile-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(67, 233, 123, 0.1);
}

.profile-card-header {
  display: flex;
  gap: 1.2rem;
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  color: white;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(67, 233, 123, 0.2);
}

.profile-card-info {
  flex: 1;
}

.profile-name {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.profile-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.95rem;
}

.meta-item .material-icons {
  font-size: 1.1rem;
  color: #43e97b;
}

.profile-card-actions {
  display: flex;
  gap: 1rem;
}

.btn-view, .btn-edit {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-view {
  background: #43e97b;
  color: white;
  border: none;
  flex: 1;
  justify-content: center;
}

.btn-view:hover {
  background: #38d16a;
  transform: translateY(-2px);
}

.btn-edit {
  background: #f3f4f6;
  color: #4b5563;
  border: none;
}

.btn-edit:hover {
  background: #e5e7eb;
  transform: translateY(-2px);
}

.fav-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.fav-card {
  background: #f8fafb;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.fav-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(67, 233, 123, 0.1);
}

.fav-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.2rem;
  text-decoration: none;
  color: inherit;
}

.avatar-sm {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: white;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(67, 233, 123, 0.2);
}

.fav-details {
  flex: 1;
}

.fav-name {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.1rem;
  margin-bottom: 0.2rem;
}

.fav-meta {
  color: #666;
  font-size: 0.9rem;
}

.fav-link .material-icons {
  color: #43e97b;
  font-size: 1.4rem;
}

.profile-actions {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  gap: 1rem;
  z-index: 2;
}

.more-options {
  position: relative;
}

.btn-more {
  background: white;
  color: #43e97b;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  box-shadow: 0 4px 16px rgba(67, 233, 123, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-more:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(67, 233, 123, 0.3);
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: 100%;
  margin-top: 0.5rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  min-width: 180px;
  z-index: 10;
  overflow: hidden;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  width: 100%;
  border: none;
  background: none;
  color: #2c3e50;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background: #f8fafb;
}

.dropdown-item.delete {
  color: #dc2626;
}

.dropdown-item.delete:hover {
  background: #fee2e2;
}

.dropdown-item .material-icons {
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .user-profile-view {
    padding: 0 0 2rem 0;
    gap: 1.5rem;
  }
  
  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 1.5rem;
  }
  
  .profile-header-bg {
    padding: 2rem 1rem 1.5rem 1rem;
  }
  
  .user-main-info h2 {
    font-size: 2rem;
  }
  
  .profile-actions {
    position: static;
    transform: none;
    margin-top: 1rem;
    justify-content: center;
  }
  
  .dropdown-menu {
    right: 50%;
    transform: translateX(50%);
  }
  
  .section {
    padding: 1.5rem;
  }
  
  .profile-cards, .fav-cards {
    grid-template-columns: 1fr;
  }
  
  .profile-card-actions {
    flex-direction: column;
  }
  
  .btn-view, .btn-edit {
    width: 100%;
    justify-content: center;
  }
}
</style>
