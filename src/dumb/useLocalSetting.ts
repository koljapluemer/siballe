import { ref, watch, type Ref } from 'vue'

const PREFIX = 'siballe:setting:'

export function useLocalSetting<T>(key: string, defaultValue: T): Ref<T> {
  const storageKey = PREFIX + key
  const stored = window.localStorage.getItem(storageKey)

  const value = ref<T>(stored !== null ? (JSON.parse(stored) as T) : defaultValue) as Ref<T>

  watch(value, (next) => {
    window.localStorage.setItem(storageKey, JSON.stringify(next))
  }, { deep: true })

  return value
}
