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
        <router-link
          v-if="authStore.getUser && String(authStore.getUser.id) === String(userId)"
          to="/profiles/new"
          class="btn-fab"
          title="Add Profile"
        >
          <span class="material-icons">add</span>
        </router-link>
      </div>
    </div>

    <div class="section">
      <div class="section-title">
        <span class="material-icons section-icon">badge</span>
        User's Profiles
      </div>
      <div v-if="profiles.length === 0" class="empty-state">
        <img src="https://cdn.jsdelivr.net/gh/edent/SuperTinyIcons/images/svg/user.svg" alt="No profiles" class="empty-illustration" />
        <div>No profiles found for this user.</div>
        <router-link
          v-if="authStore.getUser && String(authStore.getUser.id) === String(userId)"
          to="/profiles/new"
          class="btn-primary"
        >
          Create a profile
        </router-link>
      </div>
      <div v-else class="profile-cards">
        <div v-for="profile in profiles" :key="profile.id" class="profile-card">
          <div class="avatar">{{ profile.name ? profile.name[0].toUpperCase() : '?' }}</div>
          <div class="profile-card-info">
            <div class="profile-name">{{ profile.name }}</div>
            <div class="profile-meta">{{ profile.sex }}, {{ profile.race }}, Born {{ profile.birth_year }}</div>
            <router-link :to="`/profiles/${profile.id}`" class="btn-view">View</router-link>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-title">
        <span class="material-icons section-icon">favorite</span>
        Users Favourited by This User
      </div>
      <div v-if="loadingFavourites" class="loading">Loading favourites...</div>
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
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/api'
import { fetchAllProfiles, getUserFavourites } from '@/api/profile'

const route = useRoute()
const authStore = useAuthStore()
const userId = route.params.userId

const userData = ref({})
const profiles = ref([])
const userFavourites = ref([])
const loading = ref(true)
const loadingFavourites = ref(true)
const error = ref('')

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
    profiles.value = res.data.filter(p => String(p.user_id_fk) === String(userId))
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

onMounted(async () => {
  loading.value = true
  error.value = ''
  await fetchUserData()
  await fetchUserProfiles()
  await fetchUserFavourites()
  loading.value = false
})
</script>

<style scoped>
.user-profile-view {
  padding: 0 0 3rem 0;
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}
.profile-header-bg {
  background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
  border-radius: 0 0 24px 24px;
  padding: 2.5rem 1rem 2rem 1rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 24px rgba(56, 249, 215, 0.08);
}
.profile-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  max-width: 700px;
  margin: 0 auto;
  position: relative;
}
.avatar-lg {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: #43e97b;
  font-weight: bold;
  box-shadow: 0 2px 12px rgba(67, 233, 123, 0.13);
}
.user-main-info {
  flex: 1;
}
.user-main-info h2 {
  margin-bottom: 0.2rem;
  font-size: 2rem;
  font-weight: 700;
  color: #222;
}
.username {
  color: #43e97b;
  font-size: 1.1rem;
  margin-bottom: 0.1rem;
}
.email {
  color: #666;
  font-size: 1rem;
}
.btn-fab {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  box-shadow: 0 2px 8px rgba(67, 233, 123, 0.13);
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  z-index: 2;
}
.btn-fab:hover {
  background: #43e97b;
  color: #fff;
}
.section {
  margin-bottom: 2.5rem;
}
.section-title {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: #388e3c;
  margin-bottom: 1.2rem;
}
.section-icon {
  font-size: 1.5rem;
}
.profile-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}
.profile-card {
  background: #f8fffc;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(67, 233, 123, 0.07);
  padding: 1.2rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.2rem;
  min-width: 220px;
  flex: 1 1 220px;
}
.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  color: #388e3c;
  font-weight: bold;
}
.profile-card-info {
  flex: 1;
}
.profile-name {
  font-weight: 600;
  color: #222;
  font-size: 1.1rem;
}
.profile-meta {
  color: #666;
  font-size: 0.98rem;
  margin-bottom: 0.3rem;
}
.btn-view {
  background: #43e97b;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.3rem 1rem;
  font-size: 0.98rem;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
}
.btn-view:hover {
  background: #388e3c;
  color: #fff;
}
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  color: #888;
  text-align: center;
}
.empty-illustration {
  width: 48px;
  height: 48px;
  opacity: 0.7;
}
.fav-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 1.2rem;
}
.fav-card {
  background: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(67, 233, 123, 0.05);
  padding: 0.8rem 1.2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: 180px;
  flex: 1 1 180px;
  transition: box-shadow 0.2s;
}
.fav-card:hover {
  box-shadow: 0 4px 16px rgba(67, 233, 123, 0.13);
}
.avatar-sm {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  color: #388e3c;
  font-weight: bold;
}
.fav-details {
  display: flex;
  flex-direction: column;
  font-size: 1rem;
  color: #222;
}
.fav-name {
  font-weight: 600;
  color: #222;
}
.fav-meta {
  color: #666;
  font-size: 0.97rem;
}
.loading {
  color: #888;
  margin: 1rem 0;
}
.error-message {
  color: #d32f2f;
  margin: 1rem 0;
}
@media (max-width: 700px) {
  .user-profile-view {
    padding: 0 0 2rem 0;
    gap: 1.5rem;
  }
  .profile-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  .profile-header-bg {
    padding: 1.5rem 0.5rem 1.2rem 0.5rem;
  }
  .profile-cards, .fav-cards {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
