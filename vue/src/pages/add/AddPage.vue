<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="mx-auto flex max-w-lg flex-col gap-3 p-4">
    <h1 class="text-xl font-semibold">
      Add
    </h1>
    <RouterLink
      :to="{ name: 'add-content', params: { kind: 'sentence' } }"
      class="btn btn-primary"
    >
      Add Sentence
    </RouterLink>
    <RouterLink
      :to="{ name: 'add-content', params: { kind: 'vocab' } }"
      class="btn btn-primary"
    >
      Add Vocab
    </RouterLink>
  </div>
</template>
