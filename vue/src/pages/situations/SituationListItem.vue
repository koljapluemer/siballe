<script setup lang="ts">
import type { Situation } from '@/entities/situation/situation'

defineProps<{ situation: Situation; interested: boolean }>()
const emit = defineEmits<{ change: [interested: boolean] }>()
</script>

<template>
  <label class="flex items-center gap-3 px-4 py-2">
    <input
      type="checkbox"
      class="checkbox"
      :checked="interested"
      @change="emit('change', ($event.target as HTMLInputElement).checked)"
    >
    <span>{{ situation.description }}</span>
  </label>
</template>
