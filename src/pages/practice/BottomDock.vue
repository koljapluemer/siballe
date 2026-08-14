<script setup lang="ts">
import type { Component } from 'vue'

export type DockItem = { key: string; icon: Component; label: string }

defineProps<{ modelValue: string; items: DockItem[] }>()
const emit = defineEmits<{ 'update:modelValue': [key: string] }>()
</script>

<template>
  <div class="fixed inset-x-0 bottom-0 z-40 flex justify-center gap-2 p-4 sm:gap-4">
    <button
      v-for="item in items"
      :key="item.key"
      type="button"
      class="btn btn-circle shadow-lg sm:btn-lg"
      :class="modelValue === item.key ? 'btn-primary' : 'btn-outline bg-base-100'"
      :aria-label="item.label"
      :aria-pressed="modelValue === item.key"
      @click="emit('update:modelValue', item.key)"
    >
      <component :is="item.icon" />
    </button>
  </div>
</template>
