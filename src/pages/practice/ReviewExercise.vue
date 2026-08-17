<script setup lang="ts">
import { ThumbsDown, ThumbsUp } from 'lucide-vue-next'
import ExpressionButtons from '../../dumb/ExpressionButtons.vue'
import { getExpressionAudioUrl, type PhraseGoal } from '../../entities/phrase-catalog/phraseCatalog'

defineProps<{
  languageCode: string
  languageName: string
  goal: PhraseGoal
  feedback: 'correct' | 'wrong' | null
}>()
const emit = defineEmits<{ rate: [kind: 'correct' | 'wrong'] }>()
</script>

<template>
  <div class="card w-full shadow-xl">
    <div class="card-body items-center gap-4 text-center">
      <span class="badge badge-primary badge-outline">
        Try to express this in {{ languageName }}
      </span>

      <p class="text-2xl font-semibold">
        {{ goal.key }}
      </p>

      <div class="flex w-full flex-col gap-3">
        <ExpressionButtons
          v-for="expression in goal.expressions"
          :key="expression.text"
          :text="expression.text"
          :note="expression.note"
          :audio-url="getExpressionAudioUrl(languageCode, expression.text)"
        />
      </div>

      <div class="flex justify-center gap-6 pt-2">
        <button
          type="button"
          class="btn btn-circle btn-lg"
          :class="feedback === 'wrong' ? 'btn-error' : 'btn-outline'"
          :disabled="feedback !== null"
          aria-label="Wrong"
          @click="emit('rate', 'wrong')"
        >
          <ThumbsDown />
        </button>
        <button
          type="button"
          class="btn btn-circle btn-lg"
          :class="feedback === 'correct' ? 'btn-success' : 'btn-outline'"
          :disabled="feedback !== null"
          aria-label="Correct"
          @click="emit('rate', 'correct')"
        >
          <ThumbsUp />
        </button>
      </div>
    </div>
  </div>
</template>
