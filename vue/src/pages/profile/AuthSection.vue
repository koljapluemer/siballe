<script setup lang="ts">
import { ref } from 'vue'

import { ApiException } from '@/db/api-client'
import { authState, login, logout, register } from '@/entities/auth/auth'

const showSignup = ref(false)
const submitting = ref(false)
const error = ref<string | null>(null)

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

async function submit(): Promise<void> {
  if (showSignup.value && password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }

  submitting.value = true
  error.value = null
  try {
    if (showSignup.value) {
      await register(username.value.trim(), email.value.trim(), password.value)
    } else {
      await login(username.value.trim(), password.value)
    }
    password.value = ''
    confirmPassword.value = ''
  } catch (e) {
    error.value = e instanceof ApiException ? e.message : 'Something went wrong.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div
    v-if="authState.status === 'unknown'"
    class="flex justify-center"
  >
    <span class="loading loading-spinner" />
  </div>

  <div
    v-else-if="authState.status === 'loggedIn'"
    class="flex items-center gap-2"
  >
    <span class="flex-1">Logged in as {{ authState.username }}</span>
    <button
      class="btn btn-ghost btn-sm"
      @click="logout"
    >
      Log out
    </button>
  </div>

  <form
    v-else
    class="flex flex-col gap-3"
    @submit.prevent="submit"
  >
    <label class="fieldset">
      <span class="label">Username</span>
      <input
        v-model="username"
        type="text"
        class="input w-full"
      >
    </label>

    <label
      v-if="showSignup"
      class="fieldset"
    >
      <span class="label">Email</span>
      <input
        v-model="email"
        type="email"
        class="input w-full"
      >
    </label>

    <label class="fieldset">
      <span class="label">Password</span>
      <input
        v-model="password"
        type="password"
        class="input w-full"
      >
    </label>

    <label
      v-if="showSignup"
      class="fieldset"
    >
      <span class="label">Confirm password</span>
      <input
        v-model="confirmPassword"
        type="password"
        class="input w-full"
      >
    </label>

    <p
      v-if="error"
      class="text-sm text-error"
    >
      {{ error }}
    </p>

    <button
      type="submit"
      class="btn btn-primary"
      :disabled="submitting"
    >
      <span
        v-if="submitting"
        class="loading loading-spinner loading-sm"
      />
      <span v-else>{{ showSignup ? 'Create account' : 'Log in' }}</span>
    </button>
    <button
      type="button"
      class="btn btn-ghost btn-sm"
      :disabled="submitting"
      @click="showSignup = !showSignup"
    >
      {{ showSignup ? 'Log in instead' : 'Create account instead' }}
    </button>
  </form>
</template>
