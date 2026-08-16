<script setup lang="ts">
import { useRegisterSW } from 'virtual:pwa-register/vue'
import { RefreshCw } from 'lucide-vue-next'

const { needRefresh, updateServiceWorker } = useRegisterSW()

function reload() {
  updateServiceWorker(true)
}
</script>

<template>
  <div
    v-if="needRefresh"
    class="toast toast-bottom toast-center z-50"
  >
    <div class="alert bg-base-100 border border-base-300 shadow-lg">
      <span class="text-sm">A new version is available.</span>
      <button
        type="button"
        class="btn btn-primary btn-sm gap-2"
        @click="reload"
      >
        <RefreshCw
          :size="14"
          aria-hidden="true"
        />
        Reload
      </button>
    </div>
  </div>
</template>
