<script setup lang="ts">
import { computed, ref } from 'vue'
import { Volume2 } from 'lucide-vue-next'

const props = defineProps<{ text: string; note?: string; audioUrl: string }>()

const revealed = ref(false)
const listened = ref(false)
const audioRef = ref<HTMLAudioElement | null>(null)

const noteSuffix = computed(() => (props.note ? ` (${props.note})` : ''))

function play(): void {
  listened.value = true
  const audio = audioRef.value
  if (!audio) return
  audio.currentTime = 0
  void audio.play()
}
</script>

<template>
  <div class="flex items-center gap-2">
    <Transition
      name="reveal"
      mode="out-in"
    >
      <button
        v-if="!revealed"
        key="button"
        type="button"
        class="btn btn-outline flex-1"
        @click="revealed = true"
      >
        Reveal Text{{ noteSuffix }}
      </button>
      <p
        v-else
        key="text"
        class="flex-1 rounded-box border border-base-300 px-4 py-3 text-center font-medium"
      >
        {{ text }}
      </p>
    </Transition>

    <button
      v-if="!listened"
      type="button"
      class="btn btn-outline flex-1"
      @click="play"
    >
      <Volume2 :size="16" />
      Listen{{ noteSuffix }}
    </button>
    <button
      v-else
      type="button"
      class="btn btn-circle btn-outline btn-sm"
      aria-label="Replay audio"
      @click="play"
    >
      <Volume2 :size="14" />
    </button>
    <audio
      ref="audioRef"
      :src="audioUrl"
      preload="none"
      class="hidden"
    />
  </div>
</template>

<style scoped>
.reveal-enter-active {
  transition: all 0.15s ease-out;
}
.reveal-enter-from {
  opacity: 0;
  transform: scale(0.96);
}
</style>
