<script setup lang="ts">
import { useRoute } from 'vue-router'
import { BarChart3, MessageCircle, Settings } from 'lucide-vue-next'

const route = useRoute()

const tabs = [
  { routeName: 'practice', label: 'Practice', icon: MessageCircle },
  { routeName: 'stats', label: 'Stats', icon: BarChart3 },
  { routeName: 'settings', label: 'Settings', icon: Settings }
]
</script>

<template>
  <div class="min-h-screen w-full text-base-content">
    <div class="pointer-events-none fixed inset-x-0 top-0 z-50 flex items-start justify-between gap-2 p-3">
      <router-link
        :to="{ name: 'info' }"
        class="pointer-events-auto flex items-center gap-2 rounded-box border border-base-300 bg-base-100/90 px-3 py-2 font-semibold shadow-sm backdrop-blur"
      >
        siballe
      </router-link>

      <nav
        class="pointer-events-auto flex flex-wrap items-center justify-end gap-1 rounded-box border border-base-300 bg-base-100/90 p-1 shadow-sm backdrop-blur"
      >
        <router-link
          v-for="tab in tabs"
          :key="tab.routeName"
          :to="{ name: tab.routeName }"
          class="btn btn-sm gap-2"
          :class="{ 'btn-active': route.name === tab.routeName }"
        >
          <component
            :is="tab.icon"
            :size="18"
            aria-hidden="true"
          />
          <span class="hidden sm:inline">{{ tab.label }}</span>
        </router-link>
      </nav>
    </div>

    <main class="flex w-full min-h-screen justify-center bg-base-200/40 px-4 pb-8 pt-20">
      <RouterView />
    </main>
  </div>
</template>
