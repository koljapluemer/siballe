<script setup lang="ts">
import MarkdownIt from 'markdown-it'
import { computed } from 'vue'

const props = defineProps<{ text: string }>()

const md = new MarkdownIt({ html: false, linkify: true })

const rendered = computed(() => md.render(props.text))
</script>

<template>
  <!-- markdown-it has html:false, so output is limited to its own generated markup, no raw HTML passthrough -->
  <!-- eslint-disable vue/no-v-html -->
  <div
    class="prose max-w-none"
    v-html="rendered"
  />
  <!-- eslint-enable vue/no-v-html -->
</template>
