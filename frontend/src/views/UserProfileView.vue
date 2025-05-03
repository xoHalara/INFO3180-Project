<template>
  <div class="user-profile">
    <main class="main-content">
      <div v-if="loading" class="loading">Loading...</div>
      <div v-else>
        <div class="profile-header">
          <div class="profile-avatar">
            <span v-if="userData.photo">
              <img :src="userData.photo" alt="Profile Photo" />
            </span>
            <span v-else>{{
              userData.name
                ? userData.name[0].toUpperCase()
                : fallbackUser?.name?.[0]?.toUpperCase() || '?'
            }}</span>
          </div>
          <div class="profile-info">
            <template v-if="!error">
              <h2>{{ userData.name }}</h2>
              <p class="username">@{{ userData.username }}</p>
              <p class="email">{{ userData.email }}</p>
              <p class="joined">Joined: {{ formatDate(userData.date_joined) }}</p>
            </template>
            <template v-else>
              <h2>{{ fallbackUser?.name || 'Unknown User' }}</h2>
              <p class="username">@{{ fallbackUser?.username || '' }}</p>
              <p class="email">{{ fallbackUser?.email || '' }}</p>
              <div class="error-message">Failed to fetch profile details. Showing local info.</div>
            </template>
            <div v-if="isOwnProfile" class="own-actions">
              <router-link to="/profiles/new" class="btn-primary">Create New Profile</router-link>
            </div>
            <div v-else class="other-actions">
              <button class="btn-fav">&#10084; Add to Favourites</button>
            </div>
          </div>
        </div>
        <div class="user-profiles-section">
          <h3>
            {{
              isOwnProfile
                ? 'Your Profiles'
                : (userData.name || fallbackUser?.name || 'User') + "'s Profiles"
            }}
          </h3>
          <div v-if="profiles.length === 0">No profiles found.</div>
          <div v-else class="profile-grid">
            <div v-for="profile in profiles" :key="profile.id" class="profile-card">
              <div class="profile-details">
                <div class="profile-meta">
                  <span>{{ profile.sex }}</span> | <span>{{ profile.race }}</span> |
                  <span>Born {{ profile.birth_year }}</span>
                </div>
                <div class="profile-name">{{ profile.name }}</div>
                <div class="profile-desc">{{ profile.description }}</div>
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
                  <button class="btn-match" @click="() => showMatches(profile.id)">Match Me</button>
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
        <div v-if="matchReportVisible" class="match-report-section">
          <h3>Match Report</h3>
          <div v-if="matchesLoading" class="loading">Loading matches...</div>
          <div v-else-if="matches.length === 0">No matches found for this profile.</div>
          <div v-else class="profile-grid">
            <div v-for="match in matches" :key="match.id" class="profile-card">
              <div class="profile-avatar">
                <span v-if="match.photo"><img :src="match.photo" alt="Profile Photo" /></span>
                <span v-else>{{ match.name ? match.name[0].toUpperCase() : '?' }}</span>
              </div>
              <div class="profile-details">
                <div class="profile-name">{{ match.name }}</div>
                <div class="profile-meta">
                  <span>{{ match.sex }}</span> | <span>{{ match.race }}</span> |
                  <span>Born {{ match.birth_year }}</span>
                </div>
                <router-link :to="`/profiles/${match.id}`" class="details-link">View Details</router-link>
              </div>
            </div>
          </div>
        </div>
        <div class="user-favourites-section" v-if="isOwnProfile">
          <h3 class="section-title"><span class="icon">&#10084;</span> Your Favourites</h3>
          <div v-if="favouritesLoading" class="loading">Loading favourites...</div>
          <div v-else-if="favourites.length === 0" class="empty-state">
            <span class="icon-empty">&#128148;</span>
            <div>You have not favourited any users yet.</div>
          </div>
          <div v-else class="favourites-grid">
            <div v-for="fav in favourites" :key="fav.id" class="favourite-card">
              <div class="fav-avatar">
                <span v-if="fav.photo"><img :src="fav.photo" alt="User Photo" /></span>
                <span v-else>{{ fav.name ? fav.name[0].toUpperCase() : '?' }}</span>
              </div>
              <div class="fav-info">
                <div class="fav-name">{{ fav.name }}</div>
                <div class="fav-username">@{{ fav.username }}</div>
                <router-link :to="`/profiles/${fav.id}`" class="details-link"
                  >View Profile</router-link
                >
              </div>
            </div>
          </div>
        </div>
        <div v-if="isOwnProfile" class="top-fav-section">
          <h3 class="section-title">
            <span class="icon">&#11088;</span> Top 20 Most Favoured Users
          </h3>
          <div class="sort-controls">
            <label for="favSortBy">Sort by:</label>
            <select id="favSortBy" v-model="favSortBy">
              <option value="name">Name</option>
              <option value="parish">Parish</option>
              <option value="age">Age</option>
            </select>
          </div>
          <div v-if="topFavLoading" class="loading">Loading top favourites...</div>
          <div v-else-if="topFavourites.length === 0" class="empty-state">
            <span class="icon-empty">&#128533;</span>
            <div>No favourites data available.</div>
          </div>
          <div v-else class="favourites-grid">
            <div v-for="user in sortedTopFavourites" :key="user.id" class="favourite-card">
              <div class="fav-avatar">
                <span v-if="user.photo"><img :src="user.photo" alt="User Photo" /></span>
                <span v-else>{{ user.name ? user.name[0].toUpperCase() : '?' }}</span>
              </div>
              <div class="fav-info">
                <div class="fav-name">{{ user.name }}</div>
                <div class="fav-username">@{{ user.username }}</div>
                <div class="fav-meta">
                  Parish: {{ user.parish || 'N/A' }} | Age:
                  {{ user.birth_year ? new Date().getFullYear() - user.birth_year : 'N/A' }}
                </div>
                <div class="fav-count">Favourited: {{ user.favorite_count }} times</div>
                <router-link :to="`/profiles/${user.id}`" class="details-link"
                  >View Profile</router-link
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
/**
 * UserProfileView - Modular user profile page for Jam-Date.
 * Shows own or other user's profile and their profiles.
 */
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/api'
import { useFavouriteStore } from '@/stores/favourite'

// Accept userId as a prop for modular use
const props = defineProps({
  userId: {
    type: [String, Number],
    default: null,
  },
  isOwnProfile: {
    type: Boolean,
    default: false,
  },
})

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const favouriteStore = useFavouriteStore()

// Use prop if provided, else fallback to route param
const effectiveUserId = computed(() => props.userId ?? route.params.userId)
const currentUser = computed(() => authStore.getUser)
const isOwnProfile = computed(
  () =>
    props.isOwnProfile ||
    (currentUser.value && String(currentUser.value.id) === String(effectiveUserId.value)),
)

const userData = ref({})
const profiles = ref([])
const loading = ref(true)
const error = ref('')
const favourites = ref([])
const favouritesLoading = ref(false)
const matches = ref([])
const topFavourites = ref([])
const topFavLoading = ref(false)
const favSortBy = ref('name')
const matchesLoading = ref(false)
const matchReportVisible = ref(false)

const fallbackUser = computed(() => {
  // Use currentUser as fallback if available
  return currentUser.value || null
})

const fetchUserProfile = async () => {
  loading.value = true
  error.value = ''
  try {
    const userRes = await api.get(`/users/${effectiveUserId.value}`)
    userData.value = userRes.data
    const profilesRes = await api.get(`/profiles/?user_id=${effectiveUserId.value}`)
    profiles.value = profilesRes.data
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load user profile.'
    userData.value = {} // Clear userData so fallback is used
  } finally {
    loading.value = false
  }
}

const fetchFavourites = async () => {
  // Only fetch if this is the logged-in user's profile
  if (!isOwnProfile.value || !currentUser.value) return
  if (String(currentUser.value.id) !== String(effectiveUserId.value)) return
  favouritesLoading.value = true
  try {
    const res = await api.get(`/users/${currentUser.value.id}/favourites`)
    favourites.value = res.data
  } catch {
    favourites.value = []
  } finally {
    favouritesLoading.value = false
  }
}

const showMatches = async (profileId) => {
  matchesLoading.value = true
  matchReportVisible.value = true
  matches.value = []
  try {
    const res = await api.get(`/profiles/matches/${profileId}`)
    matches.value = res.data
  } catch {
    matches.value = []
  } finally {
    matchesLoading.value = false
  }
}

const fetchTopFavourites = async () => {
  if (!isOwnProfile.value) return
  topFavLoading.value = true
  try {
    const res = await api.get(`/users/favourites/${effectiveUserId.value}`)
    topFavourites.value = res.data
  } catch {
    topFavourites.value = []
  } finally {
    topFavLoading.value = false
  }
}

const sortedTopFavourites = computed(() => {
  if (!Array.isArray(topFavourites.value)) return []
  const arr = [...topFavourites.value]
  if (favSortBy.value === 'name') {
    arr.sort((a, b) => a.name.localeCompare(b.name))
  } else if (favSortBy.value === 'parish') {
    arr.sort((a, b) => (a.parish || '').localeCompare(b.parish || ''))
  } else if (favSortBy.value === 'age') {
    arr.sort((a, b) => {
      const ageA = a.birth_year ? new Date().getFullYear() - a.birth_year : 0
      const ageB = b.birth_year ? new Date().getFullYear() - b.birth_year : 0
      return ageA - ageB
    })
  }
  return arr
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString()
}

const addToFavourites = async (profile) => {
  if (!profile || !profile.user_id) return
  await favouriteStore.favouriteProfile(profile.user_id)
}

onMounted(() => {
  fetchUserProfile()
  fetchFavourites()
  fetchTopFavourites()
})
</script>

<style scoped>
.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
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
.username {
  color: #666;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}
.email {
  color: #888;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}
.joined {
  color: #aaa;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}
.own-actions,
.other-actions {
  margin-top: 1rem;
}
.btn-primary {
  background-color: #4caf50;
  color: white;
  padding: 0.5rem 1.2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}
.btn-primary:hover {
  background-color: #388e3c;
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
.btn-fav:hover {
  background: #e53935;
  color: #fff;
}
.user-profiles-section {
  margin-top: 2rem;
}
.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
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
.profile-details {
  text-align: center;
  width: 100%;
}
.profile-meta {
  font-size: 1.05rem;
  color: #666;
  margin-bottom: 0.5rem;
}
.profile-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 0.25rem;
}
.profile-desc {
  font-size: 1.05rem;
  color: #333;
  margin-bottom: 0.7rem;
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
.loading {
  text-align: center;
  color: #888;
  font-size: 1.2rem;
  margin-top: 2rem;
}
.error-message {
  color: #d32f2f;
  margin-top: 2rem;
  text-align: center;
}
.user-favourites-section {
  margin-top: 2.5rem;
}
.section-title {
  font-size: 1.35rem;
  font-weight: 700;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #388e3c;
  letter-spacing: 0.5px;
}
.icon {
  font-size: 1.3em;
  color: #e53935;
  vertical-align: middle;
}
.icon-empty {
  font-size: 2.2em;
  color: #bdbdbd;
  display: block;
  margin-bottom: 0.5rem;
}
.empty-state {
  background: #f8fafb;
  border: 1.5px dashed #bdbdbd;
  border-radius: 10px;
  padding: 2.5rem 1rem;
  text-align: center;
  color: #888;
  font-size: 1.1rem;
  margin: 1.5rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.favourites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.2rem;
  margin-top: 1rem;
}
.favourite-card {
  background: linear-gradient(90deg, #e0eafc 0%, #cfdef3 100%);
  border-radius: 10px;
  padding: 1.2rem 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(67, 233, 123, 0.07);
  transition:
    box-shadow 0.2s,
    transform 0.2s;
}
.favourite-card:hover {
  box-shadow: 0 4px 16px rgba(56, 249, 215, 0.13);
  transform: translateY(-2px) scale(1.02);
}
.fav-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  color: #388e3c;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(56, 249, 215, 0.08);
}
.fav-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
.fav-info {
  flex: 1;
}
.fav-name {
  font-weight: 600;
  color: #222;
  font-size: 1.08rem;
}
.fav-username {
  color: #666;
  font-size: 0.97rem;
  margin-bottom: 0.18rem;
}
.fav-meta {
  color: #388e3c;
  font-size: 0.95rem;
  margin-bottom: 0.18rem;
}
.fav-count {
  color: #888;
  font-size: 0.95rem;
  margin-top: 0.18rem;
}
.sort-controls {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.05rem;
  color: #388e3c;
}
.sort-controls select {
  padding: 0.3rem 0.7rem;
  border-radius: 6px;
  border: 1px solid #bdbdbd;
  font-size: 1rem;
  background: #f8fafb;
  color: #222;
  margin-left: 0.5rem;
}
.matches-section {
  margin-top: 2.5rem;
}
.top-fav-section {
  margin-top: 2.5rem;
}
.btn-match {
  background: #ff9800;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1.2rem;
  cursor: pointer;
  font-size: 1rem;
  margin-left: 0.5rem;
}
.btn-match:hover {
  background: #f57c00;
}
.match-report-section {
  margin-top: 2.5rem;
  background: #f8f0ff;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 16px rgba(56, 249, 215, 0.07);
}
</style>
