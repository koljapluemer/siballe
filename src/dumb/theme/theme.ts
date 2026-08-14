import { ref, readonly } from 'vue'

export type Theme = 'light' | 'dark'

const STORAGE_KEY = 'siballe:theme'

const themeState = ref<Theme>('light')

function applyTheme(next: Theme) {
  document.documentElement.setAttribute('data-theme', next)
}

export function initTheme() {
  const stored = window.localStorage.getItem(STORAGE_KEY)
  const initial: Theme = stored === 'light' || stored === 'dark'
    ? stored
    : (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')

  themeState.value = initial
  applyTheme(initial)
}

export function setTheme(next: Theme) {
  themeState.value = next
  window.localStorage.setItem(STORAGE_KEY, next)
  applyTheme(next)
}

export function toggleTheme() {
  setTheme(themeState.value === 'light' ? 'dark' : 'light')
}

export const theme = readonly(themeState)
