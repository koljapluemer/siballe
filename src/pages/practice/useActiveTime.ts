// "Active time" tracker for the practice page: is the user actually here,
// focused, and occasionally moving the mouse/keyboard. Reports accumulated
// ms into the app's own activity log every flush.
import { onMounted, onUnmounted } from 'vue'
import { logActiveTimeMs } from '../../entities/activity/activityLog'

const IDLE_TIMEOUT_MS = 45_000
const FLUSH_INTERVAL_MS = 15_000

// Call from the setup() of the app's "main screen" - tracking starts on
// mount and stops (with a final flush) on unmount.
export function useActiveTime(): void {
  let isVisible = document.visibilityState === 'visible'
  let isFocused = document.hasFocus()
  let lastActivityAt = Date.now()
  let lastAccumulatedAt = Date.now()
  let pendingMs = 0
  let intervalId: number | undefined

  const accumulate = (now: number) => {
    if (now <= lastAccumulatedAt) return

    if (isVisible && isFocused) {
      const activeUntil = Math.min(now, lastActivityAt + IDLE_TIMEOUT_MS)
      pendingMs += Math.max(0, activeUntil - lastAccumulatedAt)
    }

    lastAccumulatedAt = now
  }

  const flush = (now: number = Date.now()) => {
    accumulate(now)
    if (pendingMs <= 0) return

    const ms = pendingMs
    pendingMs = 0
    void logActiveTimeMs(ms)
  }

  const markActivity = () => {
    lastActivityAt = Date.now()
  }

  const handleVisibilityChange = () => {
    flush()
    isVisible = document.visibilityState === 'visible'
    if (isVisible) lastActivityAt = Date.now()
  }

  const handleBlur = () => {
    flush()
    isFocused = false
  }

  const handleFocus = () => {
    flush()
    isFocused = true
    lastActivityAt = Date.now()
  }

  const handlePageHide = () => {
    flush()
  }

  onMounted(() => {
    lastActivityAt = Date.now()
    lastAccumulatedAt = Date.now()
    intervalId = window.setInterval(() => flush(), FLUSH_INTERVAL_MS)

    document.addEventListener('visibilitychange', handleVisibilityChange)
    window.addEventListener('focus', handleFocus)
    window.addEventListener('blur', handleBlur)
    window.addEventListener('pagehide', handlePageHide)
    window.addEventListener('keydown', markActivity, { passive: true })
    window.addEventListener('pointerdown', markActivity, { passive: true })
    window.addEventListener('pointermove', markActivity, { passive: true })
  })

  onUnmounted(() => {
    flush()
    window.clearInterval(intervalId)
    document.removeEventListener('visibilitychange', handleVisibilityChange)
    window.removeEventListener('focus', handleFocus)
    window.removeEventListener('blur', handleBlur)
    window.removeEventListener('pagehide', handlePageHide)
    window.removeEventListener('keydown', markActivity)
    window.removeEventListener('pointerdown', markActivity)
    window.removeEventListener('pointermove', markActivity)
  })
}
