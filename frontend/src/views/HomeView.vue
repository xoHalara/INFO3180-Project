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
      <h1>Welcome, {{ user?.username }}!</h1>
      <div class="content-section search-section">
        <h2>Search Profiles</h2>
        <form @submit.prevent="handleSearch" class="search-form">
          <input v-model="searchParams.name" placeholder="Name" />
          <input v-model="searchParams.birth_year" placeholder="Birth Year" type="number" />
          <input v-model="searchParams.sex" placeholder="Sex" />
          <input v-model="searchParams.race" placeholder="Race" />
          <button type="submit">Search</button>
        </form>
        <div v-if="profileStore.loading && isSearching">Searching...</div>
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
                <span>{{ profile.sex }}</span> | <span>{{ profile.race }}</span> |
                <span>Born {{ profile.birth_year }}</span>
              </div>
              <router-link :to="`/profiles/${profile.id}`" class="details-link"
                >View more details</router-link
              >
            </div>
          </div>
        </div>
        <div v-else-if="isSearching && filteredSearchResults.length === 0">No results found.</div>
      </div>
      <div class="page-content-horizontal">
        <div class="content-section">
          <h2>Profiles</h2>
          <div v-if="profileStore.loading">Loading...</div>
          <div v-else-if="!isSearching && filteredLastProfiles.length === 0">No profiles found.</div>
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
                  <span>{{ profile.sex }}</span> | <span>{{ profile.race }}</span> |
                  <span>Born {{ profile.birth_year }}</span>
                </div>
                <div class="profile-actions">
                  <router-link :to="`/profiles/${profile.id}`" class="details-link"
                    >View Details</router-link
                  >
                  <button
                    class="btn-fav"
                    :disabled="
                      favouriteStore.favStates[profile.user_id]?.success ||
                      favouriteStore.favStates[profile.user_id]?.loading
                    "
                    @click="() => addToFavourites(profile)"
                    :aria-label="'Add ' + profile.name + ' to favourites'"
                  >
                    <span v-if="!favouriteStore.favStates[profile.user_id]?.success">&#10084;</span>
                    <span v-else>✔️</span>
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
      </div>
      <div v-if="profileStore.error" class="error-message">
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

.main-content h1 {
  margin-bottom: 2rem;
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

.search-section {
  background-color: white;
  padding: 2rem;
  width: 90%;
  max-width: 1000px;
  box-sizing: border-box;
  margin-top: 0;
  border-radius: 0;
  box-shadow: none;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: #f8fafb;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  width: 100%;
  justify-content: center;
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
  padding: 1rem;
  width: 90%;
  max-width: 1200px;
}

.profile-card {
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

.profile-card:hover {
  box-shadow: 0 8px 32px rgba(56, 249, 215, 0.15);
  transform: translateY(-4px);
  border-color: rgba(76, 175, 80, 0.2);
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

.profile-details {
  text-align: center;
  width: 100%;
}

.profile-name {
  font-size: 1.35rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 0.5rem;
}

.profile-meta {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.profile-actions {
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

.btn-fav {
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

.btn-fav:hover {
  color: #b71c1c;
  transform: scale(1.15);
  background: rgba(229, 57, 53, 0.2);
}

.search-form input {
  flex: 1 1 200px;
  min-width: 0;
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-form input:focus {
  border-color: #4caf50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
  outline: none;
}

.search-form button {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  border: none;
  background: #4caf50;
  color: white;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.2s, transform 0.2s;
}

.search-form button:hover {
  background: #388e3c;
  transform: translateY(-1px);
}

.error-message {
  color: #d32f2f;
  margin-top: 1rem;
  text-align: center;
}

.fav-error {
  color: #e53935;
  font-size: 0.98rem;
  margin-top: 0.3rem;
}

.fav-success {
  color: #43e97b;
  font-size: 0.98rem;
  margin-top: 0.3rem;
}

@media (max-width: 900px) {
  .main-content {
    padding: 1rem;
  }
  
  .content-section,
  .search-section {
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
  
  .search-form {
    padding: 1rem;
  }
  
  .profile-grid {
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
  
  .search-section {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .search-form {
    gap: 0.75rem;
  }
  
  .search-form input {
    flex: 1 1 100%;
  }
  
  .profile-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    width: 100%;
    padding: 0 1rem;
  }
  
  .profile-card {
    padding: 1.5rem 1rem;
    width: 100%;
  }
}
</style>
