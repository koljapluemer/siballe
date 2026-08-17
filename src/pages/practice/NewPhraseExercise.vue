<script setup lang="ts">
import { Check } from 'lucide-vue-next'
import ExpressionPlayback from '../../dumb/ExpressionPlayback.vue'
import { getExpressionAudioUrl, type PhraseGoal } from '../../entities/phrase-catalog/phraseCatalog'

defineProps<{
  languageCode: string
  goal: PhraseGoal
  acknowledged: boolean
}>()
const emit = defineEmits<{ acknowledge: [] }>()
</script>

<template>
  <div class="card w-full shadow-xl">
    <div class="card-body items-center gap-4 text-center">
      <span class="badge badge-primary badge-outline">
        Listen and Repeat
      </span>

      <p class="text-2xl font-semibold">
        {{ goal.key }}
      </p>

      <div class="flex w-full flex-col gap-3">
        <ExpressionPlayback
          v-for="expression in goal.expressions"
          :key="expression.text"
          :text="expression.text"
          :note="expression.note"
          :audio-url="getExpressionAudioUrl(languageCode, expression.text)"
        />
      </div>

      <div class="flex justify-center pt-2">
        <button
          type="button"
          class="btn btn-circle btn-lg"
          :class="acknowledged ? 'btn-success' : 'btn-outline'"
          :disabled="acknowledged"
          aria-label="Got it"
          @click="emit('acknowledge')"
        >
          <Check />
        </button>
      </div>
    </div>
  </div>
</template>
