<script setup>
/**
 * HomeView - Jam-Date dashboard
 * Shows all profiles by default, search form, and search results (excluding current user).
 * Responsive design for mobile and desktop.
 */
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useProfileStore } from '@/stores/profile'
import { useFavouriteStore } from '@/stores/favourite'

const router = useRouter()
const authStore = useAuthStore()
const profileStore = useProfileStore()
const favouriteStore = useFavouriteStore()

const user = computed(() => authStore.getUser)

const searchParams = ref({
  name: '',
  birth_year: '',
  sex: '',
  race: '',
})

const isSearching = ref(false)

const addToFavourites = async (profile) => {
  if (!profile || !profile.user_id) return
  await favouriteStore.favouriteProfile(profile.user_id)
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const handleSearch = async () => {
  isSearching.value =
    !!searchParams.value.name ||
    !!searchParams.value.birth_year ||
    !!searchParams.value.sex ||
    !!searchParams.value.race
  if (isSearching.value) {
    // Only send non-empty params
    const params = {}
    for (const key in searchParams.value) {
      if (searchParams.value[key]) params[key] = searchParams.value[key]
    }
    await profileStore.searchProfilesAction(params)
  } else {
    profileStore.searchResults = []
  }
}

// Watch for clearing of search fields to reset search state
watch(searchParams, (val) => {
  if (!val.name && !val.birth_year && !val.sex && !val.race) {
    isSearching.value = false
    profileStore.searchResults = []
  }
})

onMounted(async () => {
  await profileStore.loadLastProfiles(4)
})

const filteredSearchResults = computed(() => {
  if (!profileStore.searchResults?.length) return []
  // Exclude current user from results
  return profileStore.searchResults.filter((profile) => profile.user_id_fk !== user.value?.id)
})

const filteredLastProfiles = computed(() => {
  if (!profileStore.lastProfiles?.length) return []
  return profileStore.lastProfiles.filter((profile) => profile.user_id_fk !== user.value?.id)
})
</script>

<template>
  <div class="home">
    <main class="main-content">
      <div class="welcome-banner">
        <h1>Welcome, {{ user?.username }}!</h1>
        <p class="welcome-subtitle">Find your perfect match in Jamaica</p>
      </div>
      
      <div class="content-section search-section">
        <h2>Search Profiles</h2>
        <form @submit.prevent="handleSearch" class="search-form">
          <div class="search-input-group">
            <div class="input-wrapper">
              <span class="material-icons">search</span>
              <input v-model="searchParams.name" placeholder="Name" />
            </div>
            <div class="input-wrapper">
              <span class="material-icons">calendar_today</span>
              <input v-model="searchParams.birth_year" placeholder="Birth Year" type="number" />
            </div>
            <div class="input-wrapper">
              <span class="material-icons">person</span>
              <input v-model="searchParams.sex" placeholder="Sex" />
            </div>
            <div class="input-wrapper">
              <span class="material-icons">public</span>
              <input v-model="searchParams.race" placeholder="Race" />
            </div>
          </div>
          <button type="submit" class="search-btn">
            <span class="material-icons">search</span>
            Search
          </button>
        </form>
        
        <div v-if="profileStore.loading && isSearching" class="loading-state">
          <div class="spinner"></div>
          <p>Searching profiles...</p>
        </div>
        
        <div v-else-if="isSearching && filteredSearchResults.length" class="profile-grid">
          <div v-for="profile in filteredSearchResults" :key="profile.id" class="profile-card">
            <div class="profile-avatar">
              <span v-if="profile.photo">
                <img :src="profile.photo" alt="Profile Photo" />
              </span>
              <span v-else>{{ profile.name ? profile.name[0].toUpperCase() : '?' }}</span>
            </div>
            <div class="profile-details">
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
              <div class="profile-actions">
                <router-link :to="`/profiles/${profile.id}`" class="details-link">
                  <span class="material-icons">visibility</span>
                  View Details
                </router-link>
                <button
                  class="btn-fav"
                  :disabled="favouriteStore.favStates[profile.user_id]?.success || favouriteStore.favStates[profile.user_id]?.loading"
                  @click="() => addToFavourites(profile)"
                  :aria-label="'Add ' + profile.name + ' to favourites'"
                >
                  <span v-if="!favouriteStore.favStates[profile.user_id]?.success" class="material-icons">favorite_border</span>
                  <span v-else class="material-icons">favorite</span>
                </button>
              </div>
              <div v-if="favouriteStore.favStates[profile.user_id]?.error" class="fav-error">
                {{ favouriteStore.favStates[profile.user_id].error }}
              </div>
              <div v-if="favouriteStore.favStates[profile.user_id]?.success" class="fav-success">
                Added to favourites!
              </div>
            </div>
          </div>
        </div>
        <div v-else-if="isSearching && filteredSearchResults.length === 0" class="no-results">
          <span class="material-icons">search_off</span>
          <p>No profiles found matching your criteria</p>
        </div>
      </div>

      <div class="content-section recent-profiles">
        <h2>Recent Profiles</h2>
        <div v-if="profileStore.loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading profiles...</p>
        </div>
        <div v-else-if="!isSearching && filteredLastProfiles.length === 0" class="no-results">
          <span class="material-icons">people</span>
          <p>No profiles available at the moment</p>
        </div>
        <div v-else-if="!isSearching" class="profile-grid">
          <div v-for="profile in filteredLastProfiles" :key="profile.id" class="profile-card">
            <div class="profile-avatar">
              <span v-if="profile.photo">
                <img :src="profile.photo" alt="Profile Photo" />
              </span>
              <span v-else>{{ profile.name ? profile.name[0].toUpperCase() : '?' }}</span>
            </div>
            <div class="profile-details">
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
              <div class="profile-actions">
                <router-link :to="`/profiles/${profile.id}`" class="details-link">
                  <span class="material-icons">visibility</span>
                  View Details
                </router-link>
                <button
                  class="btn-fav"
                  :disabled="favouriteStore.favStates[profile.user_id]?.success || favouriteStore.favStates[profile.user_id]?.loading"
                  @click="() => addToFavourites(profile)"
                  :aria-label="'Add ' + profile.name + ' to favourites'"
                >
                  <span v-if="!favouriteStore.favStates[profile.user_id]?.success" class="material-icons">favorite_border</span>
                  <span v-else class="material-icons">favorite</span>
                </button>
              </div>
              <div v-if="favouriteStore.favStates[profile.user_id]?.error" class="fav-error">
                {{ favouriteStore.favStates[profile.user_id].error }}
              </div>
              <div v-if="favouriteStore.favStates[profile.user_id]?.success" class="fav-success">
                Added to favourites!
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="profileStore.error" class="error-message">
        <span class="material-icons">error</span>
        {{ profileStore.error.message || profileStore.error }}
      </div>
    </main>
  </div>
</template>

<style scoped>
.home {
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

.content-section {
  background-color: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  margin-top: 1.5rem;
  width: 90%;
  max-width: 1000px;
  box-sizing: border-box;
}

.content-section h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  text-align: center;
}

.search-section {
  background-color: white;
  padding: 2rem;
  width: 90%;
  max-width: 1000px;
  box-sizing: border-box;
  margin-top: 0;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: #f8fafb;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  width: 100%;
}

.search-input-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper .material-icons {
  position: absolute;
  left: 12px;
  color: #666;
}

.search-form input {
  width: 100%;
  padding: 0.75rem 0.75rem 0.75rem 2.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.search-form input:focus {
  border-color: #43e97b;
  box-shadow: 0 0 0 3px rgba(67, 233, 123, 0.1);
  outline: none;
}

.search-btn {
  display: flex;
  align-items: center;
  justify-content: center;
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
  margin: 0 auto;
  min-width: 200px;
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(67, 233, 123, 0.2);
}

.search-btn .material-icons {
  font-size: 1.2rem;
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
  padding: 1rem;
  width: 100%;
}

.profile-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.3s ease;
  border: 1px solid rgba(67, 233, 123, 0.1);
}

.profile-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(67, 233, 123, 0.15);
  border-color: rgba(67, 233, 123, 0.2);
}

.profile-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: white;
  margin-bottom: 1.5rem;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(67, 233, 123, 0.2);
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.profile-details {
  text-align: center;
  width: 100%;
}

.profile-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.profile-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
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
  font-size: 1.2rem;
  color: #43e97b;
}

.profile-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

.details-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #43e97b;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  background: rgba(67, 233, 123, 0.1);
}

.details-link:hover {
  background: rgba(67, 233, 123, 0.2);
  transform: translateY(-2px);
}

.details-link .material-icons {
  font-size: 1.2rem;
}

.btn-fav {
  background: none;
  border: none;
  color: #e53935;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(229, 57, 53, 0.1);
}

.btn-fav:hover {
  transform: scale(1.1);
  background: rgba(229, 57, 53, 0.2);
}

.btn-fav .material-icons {
  font-size: 1.5rem;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
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

.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  color: #666;
}

.no-results .material-icons {
  font-size: 3rem;
  color: #43e97b;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #e53935;
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(229, 57, 53, 0.1);
  border-radius: 8px;
}

.error-message .material-icons {
  font-size: 1.5rem;
}

.fav-error {
  color: #e53935;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: rgba(229, 57, 53, 0.1);
  border-radius: 4px;
}

.fav-success {
  color: #43e97b;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: rgba(67, 233, 123, 0.1);
  border-radius: 4px;
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
  
  .content-section,
  .search-section {
    width: 95%;
    padding: 1.5rem;
  }
  
  .search-input-group {
    grid-template-columns: 1fr;
  }
  
  .profile-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
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
  
  .content-section {
    padding: 1rem;
    width: 100%;
  }
  
  .search-section {
    width: 100%;
  }
  
  .profile-card {
    padding: 1.5rem;
  }
  
  .profile-avatar {
    width: 80px;
    height: 80px;
  }
}
</style>
