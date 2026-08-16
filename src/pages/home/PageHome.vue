<script setup lang="ts">
// Duolingo-style level screen: up to 5 "jump back in" cards for situations
// already practiced (longest-not-practiced first), plus a way to start a
// brand new one.
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { MessageCircle, Plus } from 'lucide-vue-next'
import { getLanguages, getSituations } from '../../entities/phrase-catalog/phraseCatalog'
import { getPracticedSituations } from '../../entities/phrase-schedule/phraseSchedule'
import NewPracticeModal from './NewPracticeModal.vue'
import { timeAgo } from './timeAgo'

type SituationCard = {
  languageCode: string
  situationSlug: string
  languageName: string
  situationName: string
  lastPracticedAt: Date
}

const CARD_LIMIT = 5

const router = useRouter()
const modalRef = ref<InstanceType<typeof NewPracticeModal> | null>(null)
const cards = ref<SituationCard[]>([])
const loading = ref(true)

onMounted(async () => {
  const practiced = await getPracticedSituations()
  practiced.sort((a, b) => a.lastPracticedAt.getTime() - b.lastPracticedAt.getTime())
  const recent = practiced.slice(0, CARD_LIMIT)

  const languages = await getLanguages()
  const languageNameByCode = new Map(languages.map((language) => [language.code, language.name]))

  const languageCodes = [...new Set(recent.map((item) => item.languageCode))]
  const situationsByLanguage = new Map(
    await Promise.all(languageCodes.map(async (code) => [code, await getSituations(code)] as const))
  )

  cards.value = recent.map((item) => ({
    ...item,
    languageName: languageNameByCode.get(item.languageCode) ?? item.languageCode,
    situationName:
      situationsByLanguage.get(item.languageCode)?.find((s) => s.slug === item.situationSlug)?.name ??
      item.situationSlug
  }))
  loading.value = false
})

function startLesson(languageCode: string, situationSlug: string): void {
  router.push({ name: 'practice', params: { languageCode, situationSlug } })
}
</script>

<template>
  <div class="mx-auto flex w-full max-w-xl flex-col gap-8 p-4">
    <div class="flex flex-col gap-1">
      <h1 class="text-2xl font-semibold">
        siballe
      </h1>
      <p class="opacity-70">
        Memorize core phrases for everyday situations, by target language.
      </p>
    </div>

    <div
      v-if="loading"
      class="flex justify-center py-8"
    >
      <span class="loading loading-spinner loading-lg" />
    </div>

    <div
      v-else
      class="flex flex-col gap-6"
    >
      <div
        v-if="cards.length > 0"
        class="flex flex-col gap-3"
      >
        <h2 class="text-sm font-semibold tracking-wide uppercase opacity-60">
          Jump back in
        </h2>
        <button
          v-for="card in cards"
          :key="`${card.languageCode}:${card.situationSlug}`"
          type="button"
          class="card card-side bg-base-100 shadow-sm transition hover:shadow-md"
          @click="startLesson(card.languageCode, card.situationSlug)"
        >
          <div class="card-body flex-row items-center gap-4 py-4">
            <div class="rounded-full bg-primary/10 p-3 text-primary">
              <MessageCircle :size="24" />
            </div>
            <div class="flex flex-1 flex-col items-start text-left">
              <p class="font-semibold">
                {{ card.situationName }}
              </p>
              <p class="text-sm opacity-60">
                {{ card.languageName }}
              </p>
            </div>
            <p class="text-xs whitespace-nowrap opacity-50">
              {{ timeAgo(card.lastPracticedAt) }}
            </p>
          </div>
        </button>
      </div>

      <button
        type="button"
        class="btn btn-outline h-auto gap-2 border-dashed py-4"
        @click="modalRef?.open()"
      >
        <Plus :size="18" />
        Practice a new situation
      </button>
    </div>

    <NewPracticeModal
      ref="modalRef"
      @start="({ languageCode, situationSlug }) => startLesson(languageCode, situationSlug)"
    />
  </div>
</template>
