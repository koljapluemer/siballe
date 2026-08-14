<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { Check } from 'lucide-vue-next'
import { getLanguages, getSituations, type PhraseLanguage, type PhraseSituation } from '../../entities/phrase-catalog/phraseCatalog'
import type { PhraseSelection } from './phraseSelection'

const props = defineProps<{ selection: PhraseSelection }>()
const emit = defineEmits<{ 'update:selection': [PhraseSelection]; selected: [] }>()

const languages = ref<PhraseLanguage[]>([])
const situations = ref<PhraseSituation[]>([])
const loadingSituations = ref(false)

onMounted(async () => {
  languages.value = await getLanguages()
})

watch(
  () => props.selection.languageCode,
  async (languageCode) => {
    situations.value = []
    if (!languageCode) return
    loadingSituations.value = true
    situations.value = await getSituations(languageCode)
    loadingSituations.value = false
  },
  { immediate: true }
)

function selectLanguage(languageCode: string): void {
  if (languageCode === props.selection.languageCode) return
  emit('update:selection', { languageCode, situationSlug: '' })
}

function selectSituation(situationSlug: string): void {
  emit('update:selection', { ...props.selection, situationSlug })
  emit('selected')
}
</script>

<template>
  <div class="mx-auto flex w-full max-w-xl flex-col gap-6 px-4 py-8">
    <div class="flex flex-col gap-2">
      <h2 class="text-sm font-semibold tracking-wide uppercase opacity-60">
        Language
      </h2>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="language in languages"
          :key="language.code"
          type="button"
          class="btn btn-sm"
          :class="selection.languageCode === language.code ? 'btn-primary' : 'btn-outline'"
          @click="selectLanguage(language.code)"
        >
          {{ language.name }}
        </button>
      </div>
    </div>

    <div
      v-if="selection.languageCode"
      class="flex flex-col gap-2"
    >
      <h2 class="text-sm font-semibold tracking-wide uppercase opacity-60">
        Situation
      </h2>
      <div
        v-if="loadingSituations"
        class="flex justify-center py-4"
      >
        <span class="loading loading-spinner" />
      </div>
      <div
        v-else
        class="flex flex-col gap-2"
      >
        <button
          v-for="situation in situations"
          :key="situation.slug"
          type="button"
          class="btn btn-block justify-start gap-2"
          :class="selection.situationSlug === situation.slug ? 'btn-primary' : 'btn-outline'"
          @click="selectSituation(situation.slug)"
        >
          <Check
            v-if="selection.situationSlug === situation.slug"
            :size="16"
          />
          {{ situation.name }}
        </button>
      </div>
    </div>
  </div>
</template>
