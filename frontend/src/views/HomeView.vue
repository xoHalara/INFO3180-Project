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

      <div class="content-section">
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
      <div v-if="profileStore.error" class="error-message">
        {{ profileStore.error.message || profileStore.error }}
      </div>
    </main>
  </div>
</template>

<style scoped>
.home {
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

.content-section {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 2rem;
  margin-top: 1.5rem;
}
.profile-card {
  background: linear-gradient(90deg, #f8fffc 0%, #e0f7fa 100%);
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(56, 249, 215, 0.07);
  padding: 1.5rem 1.2rem 1.2rem 1.2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 200px;
  transition:
    box-shadow 0.2s,
    transform 0.2s;
}
.profile-card:hover {
  box-shadow: 0 6px 24px rgba(56, 249, 215, 0.13);
  transform: translateY(-2px) scale(1.02);
}
.profile-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #388e3c;
  margin-bottom: 1rem;
  overflow: hidden;
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
  font-size: 1.25rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 0.25rem;
}
.profile-meta {
  font-size: 1.05rem;
  color: #666;
  margin-bottom: 0.5rem;
}
.profile-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
}
.details-link {
  color: #43e97b;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.08rem;
  transition: color 0.2s;
}
.details-link:hover {
  color: #388e3c;
  text-decoration: underline;
}
.btn-fav {
  background: none;
  border: none;
  color: #e53935;
  font-size: 1.5rem;
  cursor: pointer;
  transition:
    color 0.2s,
    transform 0.2s;
  padding: 0.2rem 0.5rem;
  border-radius: 50%;
  outline: none;
}
.btn-fav:hover {
  color: #b71c1c;
  transform: scale(1.15);
}
.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.search-form input {
  flex: 1 1 120px;
  min-width: 0;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.search-form button {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  border: none;
  background: #4caf50;
  color: white;
  cursor: pointer;
  font-size: 1rem;
}
.search-form button:hover {
  background: #388e3c;
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
  .profile-grid {
    gap: 1rem;
  }
  .profile-card {
    min-width: 160px;
    padding: 1rem 0.5rem;
  }
}
@media (max-width: 600px) {
  .main-content {
    padding: 0.5rem;
  }
  .content-section {
    padding: 1rem;
  }
  .profile-grid {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  .profile-card {
    min-width: 0;
    width: 100%;
    padding: 0.5rem;
  }
  .search-form {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
