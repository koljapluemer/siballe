<script setup lang="ts">
import { Compass, Play, Plus, User } from '@lucide/vue'
import { onMounted } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'

import { restoreSession } from '@/entities/auth/auth'

const route = useRoute()

onMounted(() => {
  void restoreSession()
})

const destinations = [
  { name: 'learn', label: 'Learn', icon: Play },
  { name: 'add', label: 'Add', icon: Plus },
  { name: 'situations', label: 'Situations', icon: Compass },
  { name: 'profile', label: 'Profile', icon: User },
]

function isActive(name: string): boolean {
  return route.name === name || (name === 'add' && route.name === 'add-content')
}
</script>

<template>
  <div class="pb-20">
    <RouterView />
  </div>
  <div class="dock">
    <RouterLink
      v-for="dest in destinations"
      :key="dest.name"
      :to="{ name: dest.name }"
      :class="{ 'dock-active': isActive(dest.name) }"
    >
      <component
        :is="dest.icon"
        :size="22"
      />
      <span class="dock-label">{{ dest.label }}</span>
    </RouterLink>
  </div>
</template>
