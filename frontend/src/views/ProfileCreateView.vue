<template>
  <div class="profile-create-container">
    <h2>Create New Profile</h2>
    <form @submit.prevent="handleSubmit" class="profile-form" enctype="multipart/form-data">
      <!-- 1. Profile Photo -->
      <div class="form-group">
        <label for="photo">Profile Photo:</label>
        <input type="file" id="photo" @change="handlePhotoChange" accept="image/*" class="form-control" />
      </div>
      <!-- 2. Biography -->
      <div class="form-group">
        <label for="biography">Biography:</label>
        <textarea id="biography" v-model="form.biography" required class="form-control"></textarea>
      </div>
      <!-- 3. Interests (was Description) -->
      <div class="form-group">
        <label for="description">Interests:</label>
        <textarea id="description" v-model="form.description" required class="form-control"></textarea>
      </div>
      <!-- 4. Birthdate -->
      <div class="form-group">
        <label for="birthdate">Birthdate:</label>
        <input type="date" v-model="form.birthdate" id="birthdate" class="form-control" required />
      </div>
      <!-- 5. Sex -->
      <div class="form-group">
        <label for="sex">Sex:</label>
        <select v-model="form.sex" id="sex" class="form-control" required>
          <option value="" disabled>Select sex</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
      </div>
      <!-- 6. Height -->
      <div class="form-group">
        <label for="height">Height (cm):</label>
        <select v-model="form.height" id="height" class="form-control" required>
          <option value="" disabled>Select height</option>
          <option v-for="cm in heightOptions" :key="cm" :value="cm">{{ cm }} cm</option>
        </select>
      </div>
      <!-- 7. Race -->
      <div class="form-group">
        <label for="race">Race:</label>
        <input type="text" id="race" v-model="form.race" required class="form-control" />
      </div>
      <!-- 8. Parish (dropdown) -->
      <div class="form-group">
        <label for="parish">Parish:</label>
        <select v-model="form.parish" id="parish" class="form-control" required>
          <option value="" disabled>Select parish</option>
          <option v-for="parish in parishOptions" :key="parish" :value="parish">{{ parish }}</option>
        </select>
      </div>
      <!-- 9. Remaining fields -->
      <div class="form-group">
        <label for="fav_cuisine">Favourite Cuisine:</label>
        <input type="text" id="fav_cuisine" v-model="form.fav_cuisine" required class="form-control" />
      </div>
      <div class="form-group">
        <label for="fav_colour">Favourite Colour:</label>
        <input type="text" id="fav_colour" v-model="form.fav_colour" required class="form-control" />
      </div>
      <div class="form-group">
        <label for="fav_school_subject">Favourite School Subject:</label>
        <input type="text" id="fav_school_subject" v-model="form.fav_school_subject" required class="form-control" />
      </div>
      <div class="form-group">
        <label for="political">Political:</label>
        <select v-model="form.political" id="political" class="form-control" required>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
          <option value="Somewhat">Somewhat</option>
        </select>
      </div>
      <div class="form-group">
        <label for="religious">Religious:</label>
        <select v-model="form.religious" id="religious" class="form-control" required>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
          <option value="Somewhat">Somewhat</option>
        </select>
      </div>
      <div class="form-group">
        <label for="family_oriented">Family Oriented:</label>
        <select v-model="form.family_oriented" id="family_oriented" class="form-control" required>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
          <option value="Somewhat">Somewhat</option>
        </select>
      </div>
      <button type="submit" class="btn-primary">Create Profile</button>
    </form>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
  </div>
</template>

<script setup>
/**
 * ProfileCreateView - Form for creating a new profile in Jam-Date.
 */
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useProfileStore } from '@/stores/profile'

const router = useRouter()
const profileStore = useProfileStore()

const parishOptions = [
  'Kingston', 'St. Andrew', 'St. Thomas', 'Portland', 'St. Mary', 'St. Ann',
  'Trelawny', 'St. James', 'Hanover', 'Westmoreland', 'St. Elizabeth',
  'Manchester', 'Clarendon', 'St. Catherine'
]

const form = ref({
  description: '',
  parish: '',
  biography: '',
  sex: '',
  race: '',
  height: '',
  fav_cuisine: '',
  fav_colour: '',
  fav_school_subject: '',
  political: '',
  religious: '',
  family_oriented: '',
  birthdate: '',
  photo: null,
})

const heightOptions = Array.from({ length: 251 }, (_, i) => 50 + i) // 50 to 300 cm

const errorMessage = ref('')
const successMessage = ref('')

const handlePhotoChange = (event) => {
  const file = event.target.files[0]
  form.value.photo = file
}

const handleSubmit = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  try {
    const payload = new FormData()
    for (const key in form.value) {
      if (form.value[key] !== null && form.value[key] !== '') {
        if (key !== 'birthdate') {
          payload.append(key, form.value[key])
        }
      }
    }
    if (form.value.birthdate) {
      const year = new Date(form.value.birthdate).getFullYear()
      payload.append('birth_year', year)
    }
    payload.set('political', form.value.political === 'Yes')
    payload.set('religious', form.value.religious === 'Yes')
    payload.set('family_oriented', form.value.family_oriented === 'Yes')
    await profileStore.createProfile(payload, true)
    successMessage.value = 'Profile created successfully!'
    setTimeout(() => router.push('/profile'), 1000)
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to create profile.'
  }
}

const goToProfile = () => {
  router.push('/profile')
}
</script>

<style scoped>
.profile-create-container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background: #fff;
}
.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.form-control {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}
.btn-primary {
  background-color: #4caf50;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}
.btn-primary:hover {
  background-color: #388e3c;
}
.btn-secondary {
  background-color: #eee;
  color: #333;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  margin-bottom: 1rem;
}
.btn-secondary:hover {
  background-color: #ccc;
}
.error-message {
  color: #d32f2f;
  margin-top: 0.5rem;
  text-align: center;
}
.success-message {
  color: #388e3c;
  margin-top: 0.5rem;
  text-align: center;
}
</style>
