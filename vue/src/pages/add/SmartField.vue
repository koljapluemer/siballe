<script setup lang="ts" generic="T">
import { ref } from 'vue'

const props = defineProps<{
  modelValue: string
  label: string
  hint?: string
  rows?: number
  suggestionsBuilder: (query: string) => Promise<T[]>
  displayFn: (option: T) => string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  select: [option: T]
}>()

let debounceHandle: ReturnType<typeof setTimeout> | undefined
let requestId = 0
const suggestions = ref<T[]>([])

function onInput(value: string): void {
  emit('update:modelValue', value)
  clearTimeout(debounceHandle)
  debounceHandle = setTimeout(() => void fetchSuggestions(value), 250)
}

async function fetchSuggestions(query: string): Promise<void> {
  const id = ++requestId
  const results = await props.suggestionsBuilder(query)
  if (id !== requestId) return
  suggestions.value = results
}

function select(option: T): void {
  emit('update:modelValue', props.displayFn(option))
  emit('select', option)
  suggestions.value = []
}

function dismiss(): void {
  suggestions.value = []
}
</script>

<template>
  <div class="relative">
    <label class="fieldset">
      <span class="label">{{ label }}</span>
      <textarea
        v-if="rows"
        :rows="rows"
        class="textarea w-full"
        :placeholder="hint"
        :value="modelValue"
        @input="onInput(($event.target as HTMLTextAreaElement).value)"
        @blur="dismiss"
      />
      <input
        v-else
        type="text"
        class="input w-full"
        :placeholder="hint"
        :value="modelValue"
        @input="onInput(($event.target as HTMLInputElement).value)"
        @blur="dismiss"
      >
    </label>
    <ul
      v-if="suggestions.length > 0"
      class="menu bg-base-100 rounded-box absolute z-10 mt-1 w-full shadow"
      @mousedown.prevent
    >
      <li
        v-for="(option, i) in (suggestions as T[])"
        :key="i"
      >
        <a @click="select(option)">{{ displayFn(option) }}</a>
      </li>
    </ul>
  </div>
</template>
