<script setup lang="ts">
import { ref } from 'vue'
import { Languages, MessageCircle } from 'lucide-vue-next'
import { useLocalSetting } from '@/dumb/useLocalSetting'
import BottomDock, { type DockItem } from './BottomDock.vue'
import PracticeQueueView from './PracticeQueueView.vue'
import SelectView from './SelectView.vue'
import { useActiveTime } from './useActiveTime'
import { defaultPhraseSelection, type PhraseSelection } from './phraseSelection'

useActiveTime()

type View = 'practice' | 'select'

const selection = useLocalSetting<PhraseSelection>('phrases.selection', defaultPhraseSelection)
const view = ref<View>(selection.value.situationSlug ? 'practice' : 'select')

const items: DockItem[] = [
  { key: 'practice', icon: MessageCircle, label: 'Practice' },
  { key: 'select', icon: Languages, label: 'Situation' }
]
</script>

<template>
  <div class="pb-24">
    <PracticeQueueView
      v-if="view === 'practice' && selection.situationSlug"
      :key="`${selection.languageCode}:${selection.situationSlug}`"
      :language-code="selection.languageCode"
      :situation-slug="selection.situationSlug"
    />
    <div
      v-else-if="view === 'practice'"
      class="flex flex-col items-center gap-4 px-4 py-16 text-center"
    >
      <p class="opacity-70">
        Pick a language and situation to start.
      </p>
    </div>
    <SelectView
      v-if="view === 'select'"
      :selection="selection"
      @update:selection="(next) => (selection = next)"
      @selected="view = 'practice'"
    />
    <BottomDock
      :model-value="view"
      :items="items"
      @update:model-value="(next) => (view = next as View)"
    />
  </div>
</template>
