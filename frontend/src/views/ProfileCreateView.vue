<template>
  <div class="profile-create-container">
    <h2>Create New Profile</h2>
    <form @submit.prevent="handleSubmit" class="profile-form" enctype="multipart/form-data">
      <div v-for="field in fields" :key="field.key" class="form-group">
        <label :for="field.key">{{ field.label }}:</label>
        <input
          v-if="field.type !== 'textarea' && field.type !== 'select'"
          :type="field.type"
          :id="field.key"
          v-model="form[field.key]"
          :required="field.required"
          class="form-control"
        />
        <textarea
          v-else-if="field.type === 'textarea'"
          :id="field.key"
          v-model="form[field.key]"
          :required="field.required"
          class="form-control"
        ></textarea>
        <select
          v-else-if="field.type === 'select'"
          :id="field.key"
          v-model="form[field.key]"
          :required="field.required"
          class="form-control"
        >
          <option v-for="option in field.options" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>
      <!-- Photo upload -->
      <div class="form-group">
        <label for="photo">Profile Photo:</label>
        <input type="file" id="photo" @change="handlePhotoChange" accept="image/*" class="form-control" />
      </div>
      <!-- Height in cm -->
      <div class="form-group">
        <label for="height">Height (cm):</label>
        <select v-model="form.height" id="height" class="form-control" required>
          <option value="" disabled selected>Select height</option>
          <option v-for="cm in heightOptions" :key="cm" :value="cm">{{ cm }} cm</option>
        </select>
      </div>
      <!-- Birthdate calendar -->
      <div class="form-group">
        <label for="birthdate">Birthdate:</label>
        <input type="date" v-model="form.birthdate" id="birthdate" class="form-control" />
      </div>
      <!-- Political -->
      <div class="form-group">
        <label for="political">Political:</label>
        <select v-model="form.political" id="political" class="form-control" required>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
          <option value="Somewhat">Somewhat</option>
        </select>
      </div>
      <!-- Religious -->
      <div class="form-group">
        <label for="religious">Religious:</label>
        <select v-model="form.religious" id="religious" class="form-control" required>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
          <option value="Somewhat">Somewhat</option>
        </select>
      </div>
      <!-- Family Oriented -->
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

const fields = [
  { key: 'description', label: 'Description', type: 'textarea', required: true },
  { key: 'parish', label: 'Parish', type: 'text', required: true },
  { key: 'biography', label: 'Biography', type: 'textarea', required: true },
  {
    key: 'sex',
    label: 'Sex',
    type: 'select',
    options: ['Male', 'Female', 'Other'],
    required: true,
  },
  { key: 'race', label: 'Race', type: 'text', required: true },
  { key: 'fav_cuisine', label: 'Favourite Cuisine', type: 'text', required: true },
  { key: 'fav_colour', label: 'Favourite Colour', type: 'text', required: true },
  { key: 'fav_school_subject', label: 'Favourite School Subject', type: 'text', required: true },
]

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
    // Convert boolean fields
    const payload = new FormData()
    for (const key in form.value) {
      if (form.value[key] !== null && form.value[key] !== '') {
        payload.append(key, form.value[key])
      }
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
