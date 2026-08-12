<script setup lang="ts">
import { Rating, type Grade } from 'ts-fsrs'

const emit = defineEmits<{ rate: [rating: Grade] }>()

const buttons: { label: string; rating: Grade }[] = [
  { label: 'Wrong', rating: Rating.Again },
  { label: 'Hard', rating: Rating.Hard },
  { label: 'Correct', rating: Rating.Good },
  { label: 'Easy', rating: Rating.Easy },
]
</script>

<template>
  <div class="flex justify-evenly gap-2 px-4">
    <button
      v-for="button in buttons"
      :key="button.label"
      class="btn btn-primary flex-1"
      @click="emit('rate', button.rating)"
    >
      {{ button.label }}
    </button>
  </div>
</template>
