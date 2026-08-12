import type { ExerciseCandidate } from './local-store'

function randomItem<T>(items: T[]): T {
  return items[Math.floor(Math.random() * items.length)]
}

/**
 * If anything is due: 5/6 of the time show a due exercise, 1/6 of the time
 * show a random new (never-reviewed) one instead. If nothing is due, prefer
 * a new exercise. If there's neither (or the pool is otherwise empty of
 * options), fall back to whatever is due least far in the future.
 */
export function pickCandidate(candidates: ExerciseCandidate[], now: Date): ExerciseCandidate | null {
  const due = candidates.filter((c) => c.card !== null && c.card.due <= now)
  const fresh = candidates.filter((c) => c.card === null)

  if (due.length > 0) {
    if (fresh.length > 0 && Math.floor(Math.random() * 6) === 0) {
      return randomItem(fresh)
    }
    return randomItem(due)
  }
  if (fresh.length > 0) {
    return randomItem(fresh)
  }
  if (candidates.length === 0) return null
  return candidates.reduce((a, b) => (a.card!.due < b.card!.due ? a : b))
}
