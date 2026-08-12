<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { ApiException } from '@/db/api-client'
import { fetchGroupedSituations, type LanguageGroup } from '@/entities/situation/situation'
import { getInterestedIds, setInterested } from '@/entities/situation/interest'

import SituationListItem from './SituationListItem.vue'

const loading = ref(true)
const error = ref<string | null>(null)
const groups = ref<LanguageGroup[]>([])
const interestedIds = ref<Set<number>>(new Set())

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  interestedIds.value = getInterestedIds()
  try {
    groups.value = await fetchGroupedSituations()
  } catch (e) {
    error.value = e instanceof ApiException ? e.message : 'Something went wrong.'
  } finally {
    loading.value = false
  }
}

function toggle(situationId: number, interested: boolean): void {
  setInterested(situationId, interested)
  interestedIds.value = new Set(interestedIds.value)
  if (interested) {
    interestedIds.value.add(situationId)
  } else {
    interestedIds.value.delete(situationId)
  }
}

onMounted(load)
</script>

<template>
  <div class="mx-auto max-w-lg">
    <h1 class="p-4 text-xl font-semibold">
      Situations
    </h1>

    <div
      v-if="loading"
      class="flex justify-center py-12"
    >
      <span class="loading loading-spinner" />
    </div>
    <p
      v-else-if="error"
      class="px-4 text-error"
    >
      Failed to load situations: {{ error }}
    </p>
    <p
      v-else-if="groups.length === 0"
      class="px-4"
    >
      No situations available yet.
    </p>
    <div v-else>
      <div
        v-for="group in groups"
        :key="group.language"
      >
        <h2 class="px-4 pt-4 pb-1 font-medium">
          {{ group.language }}
        </h2>
        <SituationListItem
          v-for="situation in group.situations"
          :key="situation.id"
          :situation="situation"
          :interested="interestedIds.has(situation.id)"
          @change="(interested) => toggle(situation.id, interested)"
        />
      </div>
    </div>
  </div>
</template>
