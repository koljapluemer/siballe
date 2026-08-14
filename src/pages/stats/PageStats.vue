<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getActivityStats } from '@/entities/activity/activityLog'
import PageShell from '@/dumb/PageShell.vue'
import { formatDuration } from './formatDuration'

const stats = ref<{ label: string; value: string | number }[]>([])

onMounted(async () => {
  const { trials, activeMs } = await getActivityStats()
  stats.value = [
    { label: 'Time spent', value: formatDuration(activeMs) },
    { label: 'Phrases practiced', value: trials }
  ]
})
</script>

<template>
  <PageShell title="Stats">
    <div class="stats stats-vertical sm:stats-horizontal shadow">
      <div
        v-for="stat in stats"
        :key="stat.label"
        class="stat"
      >
        <div class="stat-title">
          {{ stat.label }}
        </div>
        <div class="stat-value text-2xl">
          {{ stat.value }}
        </div>
      </div>
    </div>
  </PageShell>
</template>
