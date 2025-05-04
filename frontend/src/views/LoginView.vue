<template>
  <div class="login">
    <div class="main-content">
      <div class="content-section">
        <h2>Login</h2>
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="username" required class="form-control" />
          </div>
          <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required class="form-control" />
          </div>
          <button type="submit" class="btn-login">Login</button>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          <p class="register-link">
            Don't have an account? <router-link to="/register">Register here</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * LoginView - Handles user login for Jam-Date frontend.
 * Uses Pinia auth store and Vue Router for navigation.
 */
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const errorMessage = ref('')

const handleLogin = async () => {
  errorMessage.value = ''
  try {
    await authStore.login(username.value, password.value)
    router.push('/home')
  } catch (error) {
    errorMessage.value = 'Login failed: Invalid username or password.'
    console.error('Login failed:', error)
  }
}
</script>

<style scoped>
.login {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding-top: 90px;
  width: 100vw;
  overflow-x: hidden;
}

.main-content {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  box-sizing: border-box;
}

.content-section {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-top: 1rem;
  width: 90%;
  max-width: 500px;
  box-sizing: border-box;
}

.content-section h2 {
  margin-bottom: 1.5rem;
  text-align: center;
  color: #222;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  width: 100%;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #444;
  font-size: 1.1rem;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus {
  border-color: #4caf50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
  outline: none;
}

.btn-login {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  border: none;
  background: #4caf50;
  color: white;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.2s, transform 0.2s;
  margin-top: 1rem;
}

.btn-login:hover {
  background: #388e3c;
  transform: translateY(-1px);
}

.error-message {
  color: #d32f2f;
  margin-top: 1rem;
  text-align: center;
}

.register-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.register-link a {
  color: #43e97b;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.register-link a:hover {
  color: #388e3c;
}

@media (max-width: 900px) {
  .main-content {
    padding: 0.75rem;
  }
  
  .content-section {
    width: 95%;
    padding: 1.5rem;
    margin-top: 0.5rem;
  }
}

@media (max-width: 600px) {
  .main-content {
    padding: 0.5rem;
  }
  
  .content-section {
    padding: 1.25rem;
    width: 100%;
    margin-top: 0;
  }
  
  .content-section h2 {
    margin-bottom: 1.25rem;
  }
  
  .form-group input {
    padding: 0.5rem;
  }
  
  .btn-login {
    padding: 0.5rem 1rem;
  }
}
</style>
