/*
  auth.js - Pinia store for authentication and user state management in Jam-Date frontend
  Handles login, registration, logout, and persistent user state using the API service.
*/

import { defineStore } from 'pinia'
import api from '../api/api'

/**
 * Authentication store for managing user login, registration, and JWT token.
 */
export const useAuthStore = defineStore('auth', {
  state: () => ({
    access_token: localStorage.getItem('access_token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),

  getters: {
    /**
     * Returns true if the user is authenticated (has a valid token).
     */
    isAuthenticated: (state) => !!state.access_token,
    /**
     * Returns the current user object.
     */
    getUser: (state) => state.user,
  },

  actions: {
    /**
     * Logs in a user with username and password.
     * @param {string} username
     * @param {string} password
     * @returns {Promise<object>} User data and access token
     */
    async login(username, password) {
      try {
        const response = await api.post('/auth/login', {
          username,
          password,
        })

        const { access_token, user_id, username: uname, name } = response.data
        this.access_token = access_token
        this.user = { id: user_id, username: uname, name }

        localStorage.setItem('access_token', access_token)
        localStorage.setItem('user', JSON.stringify(this.user))

        return response.data
      } catch (error) {
        console.error('Login failed:', error)
        throw error
      }
    },

    /**
     * Registers a new user.
     * @param {string} username
     * @param {string} password
     * @param {string} name
     * @param {string} email
     * @returns {Promise<object>} Registration response
     */
    async register(username, password, name, email) {
      try {
        const response = await api.post('/auth/register', {
          username,
          password,
          name,
          email,
        })
        return response.data
      } catch (error) {
        console.error('Registration failed:', error)
        throw error
      }
    },

    /**
     * Logs out the current user and clears state.
     */
    logout() {
      this.access_token = null
      this.user = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
    },

    /**
     * Initializes authentication state from localStorage.
     */
    initializeAuth() {
      const access_token = localStorage.getItem('access_token')
      const user = JSON.parse(localStorage.getItem('user'))

      if (access_token && user) {
        this.access_token = access_token
        this.user = user
      }
    },
  },
})
