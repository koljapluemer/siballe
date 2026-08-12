<script setup lang="ts">
import { onMounted } from 'vue'

import Flashcard from './Flashcard.vue'
import FsrsButtonRow from './FsrsButtonRow.vue'
import { useLearnFlow } from './use-learn-flow'

const { stage, exercise, loadThenSync, startRound, reveal, rate } = useLearnFlow()

onMounted(() => void loadThenSync())
</script>

<template>
  <div class="mx-auto max-w-lg">
    <h1 class="p-4 text-xl font-semibold">
      Learn
    </h1>

    <div
      v-if="stage === 'loading'"
      class="flex justify-center py-12"
    >
      <span class="loading loading-spinner" />
    </div>

    <div
      v-else-if="stage === 'empty'"
      class="flex flex-col items-center gap-4 p-6 text-center"
    >
      <p>You haven't marked any situations to learn yet.</p>
      <button
        class="btn btn-primary"
        @click="startRound"
      >
        Retry
      </button>
    </div>

    <div
      v-else-if="stage === 'noCandidates'"
      class="flex flex-col items-center gap-4 p-6 text-center"
    >
      <p>No exercises are available for your situations yet.</p>
      <button
        class="btn btn-primary"
        @click="loadThenSync"
      >
        Retry
      </button>
    </div>

    <div v-else-if="exercise">
      <Flashcard
        :front="exercise.front"
        :back="stage === 'revealed' ? exercise.back : undefined"
        :credits="stage === 'revealed' ? exercise.credits : undefined"
      />
      <div
        v-if="stage === 'front'"
        class="px-4"
      >
        <button
          class="btn btn-primary w-full"
          @click="reveal"
        >
          Reveal
        </button>
      </div>
      <FsrsButtonRow
        v-else
        @rate="rate"
      />
    </div>
  </div>
</template>
