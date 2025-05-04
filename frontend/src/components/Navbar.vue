<template>
  <nav class="navbar">
    <div class="nav-brand">Jam-Date</div>
    <div class="nav-links">
      <template v-if="$route.path === '/login'">
        <router-link to="/login" class="nav-link" active-class="active" exact-active-class="active">
          <span class="material-icons">login</span>
          <span>Login</span>
        </router-link>
        <router-link to="/register" class="nav-link" active-class="active" exact-active-class="active">
          <span class="material-icons">person_add</span>
          <span>Register</span>
        </router-link>
      </template>
      <template v-else>
        <router-link to="/home" class="nav-link" active-class="active" exact-active-class="active">
          <span class="material-icons">home</span>
          <span>Home</span>
        </router-link>
        <router-link
          v-if="authStore.getUser && authStore.getUser.id"
          :to="`/users/${authStore.getUser.id}`"
          class="nav-link"
          active-class="active"
          exact-active-class="active"
        >
          <span class="material-icons">person</span>
          <span>Profile</span>
        </router-link>
        <router-link to="/reports" class="nav-link" active-class="active" exact-active-class="active">
          <span class="material-icons">assessment</span>
          <span>Reports</span>
        </router-link>
        <button @click="$emit('logout')" class="nav-link logout-btn">
          <span class="material-icons">logout</span>
          <span>Logout</span>
        </button>
      </template>
    </div>
  </nav>
</template>

<script setup>
/**
 * Navbar - Centralized navigation bar for Jam-Date.
 * Emits 'logout' event when logout is clicked.
 */
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
</script>

<style scoped>
.navbar {
  width: 100vw;
  left: 0;
  top: 0;
  position: fixed;
  z-index: 100;
  background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
  padding: 1.2rem 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  border-radius: 0;
  margin-bottom: 0;
  box-shadow: 0 4px 24px rgba(56, 249, 215, 0.08);
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
  gap: 2rem;
  align-items: center;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 500;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.nav-link .material-icons {
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.nav-link:hover .material-icons {
  transform: scale(1.1);
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
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  margin-left: 1rem;
  box-shadow: 0 2px 8px rgba(229, 57, 53, 0.08);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logout-btn:hover {
  background: #fff;
  color: #e53935;
  transform: translateY(-2px);
}

.logout-btn .material-icons {
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.logout-btn:hover .material-icons {
  transform: scale(1.1);
}

@media (max-width: 700px) {
  .navbar {
    flex-direction: column;
    align-items: flex-start;
    padding: 1rem 1.5rem;
  }
  
  .nav-brand {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  
  .nav-links {
    flex-direction: column;
    gap: 1rem;
    width: 100%;
  }
  
  .nav-link, .logout-btn {
    font-size: 1rem;
    padding: 0.75rem 1rem;
    width: 100%;
    text-align: left;
    justify-content: flex-start;
  }
}
</style>
