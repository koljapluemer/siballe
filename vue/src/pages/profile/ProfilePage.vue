<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { deleteApiKey, readApiKey, writeApiKey } from '@/entities/api-key/api-key'

import AuthSection from './AuthSection.vue'

const apiKey = ref('')
const loaded = ref(false)
const saved = ref(false)

onMounted(() => {
  apiKey.value = readApiKey() ?? ''
  loaded.value = true
})

function saveApiKey(): void {
  const value = apiKey.value.trim()
  if (value === '') {
    deleteApiKey()
  } else {
    writeApiKey(value)
  }
  saved.value = true
  setTimeout(() => (saved.value = false), 2000)
}
</script>

<template>
  <div class="mx-auto flex max-w-lg flex-col gap-6 p-4">
    <h1 class="text-xl font-semibold">
      Profile
    </h1>

    <div
      v-if="!loaded"
      class="flex justify-center py-12"
    >
      <span class="loading loading-spinner" />
    </div>
    <template v-else>
      <AuthSection />

      <div class="divider" />

      <div class="flex flex-col gap-3">
        <label class="fieldset">
          <span class="label">OpenAI API Key</span>
          <input
            v-model="apiKey"
            type="password"
            class="input w-full"
          >
        </label>
        <button
          class="btn btn-primary"
          @click="saveApiKey"
        >
          {{ saved ? 'Saved.' : 'Save' }}
        </button>
      </div>
    </template>
  </div>
</template>
