<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, PartyPopper, ThumbsDown, ThumbsUp } from 'lucide-vue-next'
import ExpressionButtons from '../../dumb/ExpressionButtons.vue'
import { getExpressionAudioUrl, getLanguages, getSituations } from '../../entities/phrase-catalog/phraseCatalog'
import { useActiveTime } from './useActiveTime'
import { useLesson } from './useLesson'

const props = defineProps<{ languageCode: string; situationSlug: string }>()

const router = useRouter()
useActiveTime()

const languageName = ref('')
const situationName = ref('')
const feedback = ref<'correct' | 'wrong' | null>(null)
const lesson = useLesson(props.languageCode, props.situationSlug)

onMounted(async () => {
  const [languages, situations] = await Promise.all([getLanguages(), getSituations(props.languageCode)])
  languageName.value = languages.find((language) => language.code === props.languageCode)?.name ?? props.languageCode
  situationName.value =
    situations.find((situation) => situation.slug === props.situationSlug)?.name ?? props.situationSlug
})

async function handleRate(kind: 'correct' | 'wrong'): Promise<void> {
  if (feedback.value) return
  feedback.value = kind
  await new Promise((resolve) => setTimeout(resolve, 250))
  await lesson.rate(kind)
  feedback.value = null
}

function goHome(): void {
  router.push({ name: 'home' })
}
</script>

<template>
  <div class="mx-auto flex w-full max-w-xl flex-col gap-4 px-4 py-8">
    <div class="flex items-center gap-3">
      <button
        type="button"
        class="btn btn-circle btn-ghost btn-sm"
        aria-label="Back to home"
        @click="goHome"
      >
        <ArrowLeft :size="18" />
      </button>
      <div class="flex-1">
        <p class="text-xs font-semibold tracking-wide uppercase opacity-60">
          {{ languageName }}
        </p>
        <p class="font-semibold">
          {{ situationName }}
        </p>
      </div>
      <div
        v-if="!lesson.loading.value && lesson.total.value > 0"
        class="text-sm font-medium tabular-nums opacity-70"
      >
        {{ Math.min(lesson.index.value + 1, lesson.total.value) }} / {{ lesson.total.value }}
      </div>
    </div>

    <progress
      v-if="!lesson.loading.value && lesson.total.value > 0"
      class="progress progress-primary w-full"
      :value="lesson.finished.value ? lesson.total.value : lesson.index.value"
      :max="lesson.total.value"
    />

    <div
      v-if="lesson.loading.value"
      class="flex justify-center py-8"
    >
      <span class="loading loading-spinner loading-lg" />
    </div>

    <div
      v-else-if="lesson.finished.value"
      class="card w-full shadow-xl"
    >
      <div class="card-body items-center gap-4 text-center">
        <PartyPopper
          :size="40"
          class="text-primary"
        />
        <p class="text-xl font-semibold">
          Lesson complete
        </p>
        <p class="opacity-70">
          {{ lesson.correctCount.value }} / {{ lesson.total.value }} correct
        </p>
        <div class="flex w-full flex-col gap-2 pt-2">
          <button
            type="button"
            class="btn btn-primary"
            @click="lesson.restart()"
          >
            Practice again
          </button>
          <button
            type="button"
            class="btn btn-outline"
            @click="goHome"
          >
            Back to home
          </button>
        </div>
      </div>
    </div>

    <p
      v-else-if="!lesson.current.value"
      class="py-8 text-center opacity-70"
    >
      No phrases to practice for this situation yet.
    </p>

    <Transition
      v-else
      name="phrase-swap"
      mode="out-in"
    >
      <div
        :key="lesson.current.value.id"
        class="card w-full shadow-xl"
      >
        <div class="card-body items-center gap-4 text-center">
          <span class="badge badge-primary badge-outline">
            Try to express this in {{ languageName }}
          </span>

          <p class="text-2xl font-semibold">
            {{ lesson.current.value.goal.key }}
          </p>

          <div class="flex w-full flex-col gap-3">
            <ExpressionButtons
              v-for="expression in lesson.current.value.goal.expressions"
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
