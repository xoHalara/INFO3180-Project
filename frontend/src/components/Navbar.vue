<template>
  <nav class="navbar">
    <div class="nav-brand">Jam-Date</div>
    <div class="nav-links">
      <router-link to="/home" class="nav-link" active-class="active" exact-active-class="active"
        >Home</router-link
      >
      <router-link to="/profile" class="nav-link" active-class="active" exact-active-class="active"
        >Profile</router-link
      >
      <button @click="$emit('logout')" class="nav-link logout-btn">Logout</button>
    </div>
  </nav>
</template>

<script setup>
/**
 * Navbar - Centralized navigation bar for Jam-Date.
 * Emits 'logout' event when logout is clicked.
 */
</script>

<style scoped>
.navbar {
  background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
  padding: 1rem 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  border-radius: 12px 12px 0 0;
  margin-bottom: 2rem;
  box-shadow: 0 4px 24px rgba(56, 249, 215, 0.08);
  position: sticky;
  top: 0;
  z-index: 10;
}
.nav-brand {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: 1px;
  color: #fff;
  text-shadow: 0 2px 8px rgba(67, 233, 123, 0.15);
}
.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}
.nav-link {
  color: #fff;
  text-decoration: none;
  padding: 0.5rem 1.2rem;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 500;
  background: none;
  border: none;
  cursor: pointer;
  transition:
    background 0.2s,
    color 0.2s,
    box-shadow 0.2s;
  position: relative;
}
.nav-link.active,
.nav-link.router-link-exact-active {
  background: rgba(255, 255, 255, 0.18);
  color: #222;
  box-shadow: 0 2px 8px rgba(67, 233, 123, 0.08);
}
.nav-link:not(.active):hover {
  background: rgba(255, 255, 255, 0.09);
  color: #222;
}
.logout-btn {
  color: #fff;
  background: linear-gradient(90deg, #e53935 0%, #e35d5b 100%);
  font-weight: 600;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1.2rem;
  margin-left: 1rem;
  box-shadow: 0 2px 8px rgba(229, 57, 53, 0.08);
  transition:
    background 0.2s,
    color 0.2s;
}
.logout-btn:hover {
  background: #fff;
  color: #e53935;
}
</style>
