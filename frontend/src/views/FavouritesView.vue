<template>
  <div class="favourites-view">
    <h1>Favourites Report</h1>
    <section class="top-favourites-section">
      <h2>Top 20 Most Favoured Users</h2>
      <div class="sort-controls">
        <label>Sort by:
          <select v-model="topSortBy" @change="fetchTopFavourites">
            <option value="name">Name</option>
            <option value="parish">Parish</option>
            <option value="birth_year">Age</option>
            <option value="favorite_count"># Favourited</option>
          </select>
        </label>
        <label>Order:
          <select v-model="topOrder" @change="fetchTopFavourites">
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
        </label>
      </div>
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
      <div class="sort-controls">
        <label>Sort by:
          <select v-model="userSortBy" @change="fetchUserFavourites">
            <option value="name">Name</option>
            <option value="parish">Parish</option>
            <option value="birth_year">Age</option>
          </select>
        </label>
        <label>Order:
          <select v-model="userOrder" @change="fetchUserFavourites">
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
        </label>
      </div>
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

const topSortBy = ref('name')
const topOrder = ref('asc')
const userSortBy = ref('name')
const userOrder = ref('asc')

const fetchTopFavourites = async () => {
  loadingTop.value = true
  try {
    const res = await getTopFavourites(20, topSortBy.value, topOrder.value)
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
      const res = await getUserFavourites(user.id, userSortBy.value, userOrder.value)
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
.sort-controls {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  margin-bottom: 1rem;
}
.sort-controls label {
  font-size: 1rem;
  color: #333;
}
.sort-controls select {
  margin-left: 0.5rem;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  border: 1px solid #d0d0d0;
}
</style> 