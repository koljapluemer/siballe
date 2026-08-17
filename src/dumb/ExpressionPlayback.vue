<script setup lang="ts">
import { ref } from 'vue'
import { Volume2 } from 'lucide-vue-next'

defineProps<{ text: string; note?: string; audioUrl: string }>()

const audioRef = ref<HTMLAudioElement | null>(null)

function play(): void {
  const audio = audioRef.value
  if (!audio) return
  audio.currentTime = 0
  void audio.play()
}
</script>

<template>
  <div class="flex items-center gap-2">
    <p class="flex-1 rounded-box border border-base-300 px-4 py-3 text-center font-medium">
      {{ text }}<span
        v-if="note"
        class="opacity-60"
      > ({{ note }})</span>
    </p>
    <button
      type="button"
      class="btn btn-circle btn-outline"
      aria-label="Play audio"
      @click="play"
    >
      <Volume2 :size="16" />
    </button>
    <audio
      ref="audioRef"
      :src="audioUrl"
      preload="none"
      class="hidden"
    />
  </div>
</template>
