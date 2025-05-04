<template>
  <div class="favourites-view">
    <h1>Favourites Report</h1>
    <section class="top-favourites-section">
      <h2>Top 20 Most Favoured Users</h2>
      <div v-if="loadingTop" class="loading">Loading top favourites...</div>
      <div v-else-if="topFavourites.length === 0" class="empty">No favourites data available.</div>
      <ul v-else class="fav-list">
        <li v-for="user in topFavourites" :key="user.id" class="fav-user">
          <span class="fav-name">{{ user.name || user.username }}</span>
          <span class="fav-count">({{ user.favorite_count || 0 }} favourites)</span>
        </li>
      </ul>
    </section>
    <section class="user-favourites-section">
      <h2>Users You Have Favoured</h2>
      <div v-if="loadingUserFavs" class="loading">Loading your favourites...</div>
      <div v-else-if="userFavourites.length === 0" class="empty">You have not favourited any users yet.</div>
      <ul v-else class="fav-list">
        <li v-for="user in userFavourites" :key="user.id" class="fav-user">
          <span class="fav-name">{{ user.name || user.username }}</span>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getTopFavourites, getUserFavourites } from '@/api/profile'

const authStore = useAuthStore()
const user = authStore.getUser

const topFavourites = ref([])
const userFavourites = ref([])
const loadingTop = ref(true)
const loadingUserFavs = ref(true)

const fetchTopFavourites = async () => {
  loadingTop.value = true
  try {
    const res = await getTopFavourites(20)
    topFavourites.value = res.data
  } catch {
    topFavourites.value = []
  } finally {
    loadingTop.value = false
  }
}

const fetchUserFavourites = async () => {
  loadingUserFavs.value = true
  try {
    if (user?.id) {
      const res = await getUserFavourites(user.id)
      userFavourites.value = res.data
    } else {
      userFavourites.value = []
    }
  } catch {
    userFavourites.value = []
  } finally {
    loadingUserFavs.value = false
  }
}

onMounted(() => {
  fetchTopFavourites()
  fetchUserFavourites()
})
</script>

<style scoped>
.favourites-view {
  padding: 2rem;
}
.top-favourites-section, .user-favourites-section {
  margin-bottom: 2.5rem;
}
.fav-list {
  list-style: none;
  padding: 0;
}
.fav-user {
  padding: 0.5rem 0;
  font-size: 1.1rem;
  display: flex;
  gap: 1.5rem;
  align-items: center;
}
.fav-name {
  font-weight: 600;
}
.fav-count {
  color: #388e3c;
  font-size: 0.98rem;
}
.loading {
  color: #888;
  margin: 1rem 0;
}
.empty {
  color: #bdbdbd;
  margin: 1rem 0;
}
</style> 