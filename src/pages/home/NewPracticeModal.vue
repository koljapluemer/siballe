<script setup lang="ts">
// Lang-select-into-situation-select flow, shown as a modal from the home
// screen. Picking a situation emits `start` and closes itself; the caller
// decides what to do with the pick (navigate into a fresh lesson run).
import { ref, watch } from 'vue'
import { X } from 'lucide-vue-next'
import { getLanguages, getSituations, type PhraseLanguage, type PhraseSituation } from '../../entities/phrase-catalog/phraseCatalog'

const emit = defineEmits<{ start: [{ languageCode: string; situationSlug: string }] }>()

const dialogRef = ref<HTMLDialogElement | null>(null)
const languages = ref<PhraseLanguage[]>([])
const situations = ref<PhraseSituation[]>([])
const languageCode = ref('')
const loadingLanguages = ref(false)
const loadingSituations = ref(false)

async function open(): Promise<void> {
  languageCode.value = ''
  situations.value = []
  dialogRef.value?.showModal()
  if (languages.value.length === 0) {
    loadingLanguages.value = true
    languages.value = await getLanguages()
    loadingLanguages.value = false
  }
}

function close(): void {
  dialogRef.value?.close()
}

function selectLanguage(code: string): void {
  languageCode.value = code
}

watch(languageCode, async (code) => {
  situations.value = []
  if (!code) return
  loadingSituations.value = true
  situations.value = await getSituations(code)
  loadingSituations.value = false
})

function selectSituation(situationSlug: string): void {
  emit('start', { languageCode: languageCode.value, situationSlug })
  close()
}

defineExpose({ open })
</script>

<template>
  <dialog
    ref="dialogRef"
    class="modal"
  >
    <div class="modal-box relative flex flex-col gap-6">
      <form method="dialog">
        <button
          type="submit"
          class="btn btn-circle btn-ghost btn-sm absolute top-2 right-2"
          aria-label="Close"
        >
          <X :size="16" />
        </button>
      </form>

      <h3 class="text-lg font-semibold">
        Practice a new situation
      </h3>

      <div class="flex flex-col gap-2">
        <h4 class="text-sm font-semibold tracking-wide uppercase opacity-60">
          Language
        </h4>
        <div
          v-if="loadingLanguages"
          class="flex justify-center py-4"
        >
          <span class="loading loading-spinner" />
        </div>
        <div
          v-else
          class="flex flex-wrap gap-2"
        >
          <button
            v-for="language in languages"
            :key="language.code"
            type="button"
            class="btn btn-sm"
            :class="languageCode === language.code ? 'btn-primary' : 'btn-outline'"
            @click="selectLanguage(language.code)"
          >
            {{ language.name }}
          </button>
        </div>
      </div>

      <div
        v-if="languageCode"
        class="flex flex-col gap-2"
      >
        <h4 class="text-sm font-semibold tracking-wide uppercase opacity-60">
          Situation
        </h4>
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
            class="btn btn-block justify-start btn-outline"
            @click="selectSituation(situation.slug)"
          >
            {{ situation.name }}
          </button>
        </div>
      </div>
    </div>
    <form
      method="dialog"
      class="modal-backdrop"
    >
      <button>close</button>
    </form>
  </dialog>
</template>
