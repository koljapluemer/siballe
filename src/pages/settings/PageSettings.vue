<script setup lang="ts">
import ThemeToggle from '@/dumb/theme/ThemeToggle.vue'
import PageShell from '@/dumb/PageShell.vue'
</script>

<template>
  <PageShell title="Settings">
    <div class="flex items-center justify-between">
      <span class="text-sm font-medium">Theme</span>
      <ThemeToggle />
    </div>
  </PageShell>
</template>
