<script setup>
import { RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Navbar from './components/Navbar.vue'

const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div id="app">
    <Navbar @logout="handleLogout" />
    <div class="app-content">
      <router-view />
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

html, body {
  height: auto;
  min-height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  min-height: 100%;
  width: 100vw;
  background: #f8f9fa;
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  display: flex;
  flex-direction: column;
}

.app-content {
  padding-top: 90px;
  max-height: none;
  overflow: visible;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: none;
}

.navbar {
  width: 100vw;
  left: 0;
  top: 0;
  position: fixed;
  z-index: 50;
  background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
  padding: 1rem 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  border-radius: 0;
  margin-bottom: 0;
  box-shadow: 0 4px 24px rgba(56, 249, 215, 0.08);
}
</style>
