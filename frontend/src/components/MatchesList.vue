<template>
  <div class="matches-list">
    <div class="matches-header">
      <h3>Matches</h3>
      <button class="btn-close" @click="$emit('close')">&times;</button>
    </div>
    <div v-if="loading" class="loading">Loading matches...</div>
    <div v-else-if="matches.length === 0">No matches found.</div>
    <div v-else class="profile-grid">
      <div v-for="match in matches" :key="match.id" class="profile-card">
        <div class="profile-details">
          <div class="profile-meta">
            <span>{{ match.sex }}</span> | <span>{{ match.race }}</span> |
            <span>Born {{ match.birth_year }}</span>
          </div>
          <div class="profile-desc">{{ match.description }}</div>
          <router-link :to="`/profiles/${match.id}`" class="details-link">View Details</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  matches: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})
</script>

<style scoped>
.matches-list {
  margin-top: 2rem;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.07);
  padding: 1.5rem;
}
.matches-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}
.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #888;
  cursor: pointer;
  padding: 0 0.5rem;
}
.btn-close:hover {
  color: #e53935;
}
.loading {
  text-align: center;
  color: #888;
  font-size: 1.1rem;
  margin-top: 1rem;
}
</style>
