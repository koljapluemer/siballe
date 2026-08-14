<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ThumbsDown, ThumbsUp } from 'lucide-vue-next'
import ExpressionButtons from '../../dumb/ExpressionButtons.vue'
import { getExpressionAudioUrl, getLanguages } from '../../entities/phrase-catalog/phraseCatalog'
import { usePracticeQueue } from './usePracticeQueue'

const props = defineProps<{ languageCode: string; situationSlug: string }>()

const languageName = ref('')
const feedback = ref<'correct' | 'wrong' | null>(null)
const queue = usePracticeQueue(props.languageCode, props.situationSlug)

onMounted(async () => {
  const languages = await getLanguages()
  languageName.value = languages.find((language) => language.code === props.languageCode)?.name ?? props.languageCode
})

async function handleRate(kind: 'correct' | 'wrong'): Promise<void> {
  if (feedback.value) return
  feedback.value = kind
  await new Promise((resolve) => setTimeout(resolve, 250))
  await queue.rate(kind === 'correct' ? queue.Rating.Good : queue.Rating.Again)
  feedback.value = null
}
</script>

<template>
  <div class="mx-auto flex w-full max-w-xl flex-col gap-4 px-4 py-8">
    <div
      v-if="queue.loading.value"
      class="flex justify-center py-8"
    >
      <span class="loading loading-spinner loading-lg" />
    </div>

    <p
      v-else-if="!queue.candidate.value"
      class="py-8 text-center opacity-70"
    >
      All caught up. Nothing due right now.
    </p>

    <Transition
      v-else
      name="phrase-swap"
      mode="out-in"
    >
      <div
        :key="queue.candidate.value.id"
        class="card w-full shadow-xl"
      >
        <div class="card-body items-center gap-4 text-center">
          <span class="badge badge-primary badge-outline">
            Try to express this in {{ languageName }}
          </span>

          <p class="text-2xl font-semibold">
            {{ queue.candidate.value.goal.key }}
          </p>

          <div class="flex w-full flex-col gap-3">
            <ExpressionButtons
              v-for="expression in queue.candidate.value.goal.expressions"
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
              @click="handleRate('wrong')"
            >
              <ThumbsDown />
            </button>
            <button
              type="button"
              class="btn btn-circle btn-lg"
              :class="feedback === 'correct' ? 'btn-success' : 'btn-outline'"
              :disabled="feedback !== null"
              aria-label="Correct"
              @click="handleRate('correct')"
            >
              <ThumbsUp />
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.phrase-swap-enter-active,
.phrase-swap-leave-active {
  transition: all 0.2s ease-out;
}
.phrase-swap-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.phrase-swap-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
