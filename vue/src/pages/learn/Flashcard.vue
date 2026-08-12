<script setup lang="ts">
import MarkdownView from '@/dumb/MarkdownView.vue'

defineProps<{ front: string; back?: string; credits?: string }>()
</script>

<template>
  <div class="card bg-base-100 shadow m-4">
    <div class="card-body">
      <MarkdownView :text="front" />
      <template v-if="back">
        <div class="divider" />
        <MarkdownView :text="back" />
      </template>
      <div
        v-if="back && credits"
        class="bg-base-200 mt-2 rounded p-2 text-xs"
      >
        {{ credits }}
      </div>
    </div>
  </div>
</template>
