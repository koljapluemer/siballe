<script setup lang="ts">
import { computed } from 'vue'
import { Moon, Sun } from 'lucide-vue-next'
import { theme, toggleTheme } from './theme'

const isDark = computed(() => theme.value === 'dark')
</script>

<template>
  <button
    type="button"
    class="btn btn-ghost btn-circle btn-sm"
    :aria-label="isDark ? 'Switch to light theme' : 'Switch to dark theme'"
    @click="toggleTheme"
  >
    <Moon
      v-if="isDark"
      :size="18"
      aria-hidden="true"
    />
    <Sun
      v-else
      :size="18"
      aria-hidden="true"
    />
  </button>
</template>
