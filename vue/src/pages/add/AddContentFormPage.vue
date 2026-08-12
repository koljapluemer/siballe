<script setup lang="ts">
import { computed, onMounted, ref, useTemplateRef } from 'vue'
import { useRouter } from 'vue-router'

import { ApiException } from '@/db/api-client'
import { readApiKey } from '@/entities/api-key/api-key'
import { listLanguages, type Language } from '@/entities/language/language'
import { addContent, searchNodes } from '@/entities/node/node'
import { listSituationsForLanguage } from '@/entities/situation/situation'

import SmartField from './SmartField.vue'
import TranslationRowsField from './TranslationRowsField.vue'

const props = defineProps<{ kind: string }>()
const router = useRouter()

const nodeKind = computed(() => (props.kind === 'sentence' ? 'SENTENCE' : 'VOCAB'))
const isSentence = computed(() => nodeKind.value === 'SENTENCE')

const languages = ref<Language[]>([])
const languageText = ref('')
const selectedLanguage = ref<Language | null>(null)
const situationText = ref('')
const contentText = ref('')

const situationsCache = new Map<string, string[]>()
const translationsRef = useTemplateRef<InstanceType<typeof TranslationRowsField>>('translations')

const submitting = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  languages.value = await listLanguages()
})

async function languageSuggestions(query: string): Promise<Language[]> {
  const trimmed = query.trim().toLowerCase()
  if (!trimmed) return []
  return languages.value.filter((l) => l.name.toLowerCase().includes(trimmed)).slice(0, 8)
}

async function situationSuggestions(query: string): Promise<string[]> {
  const language = selectedLanguage.value
  if (!language) return []
  let options = situationsCache.get(language.code)
  if (!options) {
    const situations = await listSituationsForLanguage(language.code)
    options = situations.map((s) => s.description)
    situationsCache.set(language.code, options)
  }
  const lower = query.trim().toLowerCase()
  const matches = lower ? options.filter((s) => s.toLowerCase().includes(lower)) : options
  return matches.slice(0, 8)
}

function contentSuggestions(query: string): Promise<string[]> {
  const language = selectedLanguage.value
  if (!language) return Promise.resolve([])
  return searchNodes(nodeKind.value, language.code, query)
}

function resolveLanguage(): Language | null {
  const typed = languageText.value.trim().toLowerCase()
  return languages.value.find((l) => l.name.toLowerCase() === typed) ?? null
}

const situationHint = computed(() =>
  selectedLanguage.value ? `General ${selectedLanguage.value.name}` : undefined,
)

async function submit(): Promise<void> {
  const language = resolveLanguage()
  if (!language) {
    error.value = 'Select a language from the list.'
    return
  }
  const content = contentText.value.trim()
  const translations = translationsRef.value?.nonEmptyTranslations() ?? []
  if (content === '' && translations.length === 0) {
    error.value = 'Add the word/sentence or at least one translation.'
    return
  }

  submitting.value = true
  error.value = null
  try {
    await addContent({
      kind: nodeKind.value,
      language: language.code,
      situationDescription: situationText.value.trim(),
      content,
      translations,
      apiKey: readApiKey(),
    })
    await router.push({ name: 'add' })
  } catch (e) {
    error.value = e instanceof ApiException ? e.message : 'Something went wrong.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="mx-auto flex max-w-lg flex-col gap-4 p-4">
    <h1 class="text-xl font-semibold">
      {{ isSentence ? 'Add Sentence' : 'Add Vocab' }}
    </h1>

    <SmartField
      v-model="languageText"
      label="Language"
      :suggestions-builder="languageSuggestions"
      :display-fn="(o: Language) => o.name"
      @select="(o) => (selectedLanguage = o)"
    />

    <SmartField
      v-model="situationText"
      label="Situation"
      :hint="situationHint"
      :suggestions-builder="situationSuggestions"
      :display-fn="(o: string) => o"
    />

    <SmartField
      v-model="contentText"
      :label="isSentence ? 'Sentence' : 'Word'"
      :rows="isSentence ? 3 : undefined"
      :suggestions-builder="contentSuggestions"
      :display-fn="(o: string) => o"
    />

    <TranslationRowsField
      ref="translations"
      :kind="nodeKind"
    />

    <p
      v-if="error"
      class="text-sm text-error"
    >
      {{ error }}
    </p>

    <button
      class="btn btn-primary"
      :disabled="submitting"
      @click="submit"
    >
      <span
        v-if="submitting"
        class="loading loading-spinner loading-sm"
      />
      <span v-else>Save</span>
    </button>
  </div>
</template>
