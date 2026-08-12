<script setup lang="ts">
import { X } from '@lucide/vue'
import { reactive } from 'vue'

import { searchNodes } from '@/entities/node/node'

import SmartField from './SmartField.vue'

const props = defineProps<{ kind: string }>()

interface Row {
  content: string
  note: string
}

const rows = reactive<Row[]>([{ content: '', note: '' }])

defineExpose({
  nonEmptyTranslations(): { content: string; note: string }[] {
    return rows
      .filter((row) => row.content.trim() !== '')
      .map((row) => ({ content: row.content.trim(), note: row.note.trim() }))
  },
})

function ensureTrailingEmptyRow(): void {
  const last = rows[rows.length - 1]
  if (last.content.trim() !== '') {
    rows.push({ content: '', note: '' })
  }
}

function removeAt(index: number): void {
  if (rows.length <= 1) return
  rows.splice(index, 1)
}

function searchEnglish(query: string): Promise<string[]> {
  return searchNodes(props.kind, 'eng', query)
}
</script>

<template>
  <div class="flex flex-col gap-2">
    <span class="label">Translations</span>
    <div
      v-for="(row, i) in rows"
      :key="i"
      class="flex items-start gap-2"
    >
      <div class="flex flex-1 flex-col gap-1">
        <SmartField
          v-model="row.content"
          label="English"
          :suggestions-builder="searchEnglish"
          :display-fn="(o: string) => o"
          @update:model-value="ensureTrailingEmptyRow"
        />
        <label class="fieldset">
          <span class="label">Note (optional)</span>
          <input
            v-model="row.note"
            type="text"
            class="input input-sm w-full"
          >
        </label>
      </div>
      <button
        v-if="rows.length > 1"
        type="button"
        class="btn btn-ghost btn-sm btn-square mt-6"
        @click="removeAt(i)"
      >
        <X :size="16" />
      </button>
    </div>
  </div>
</template>
