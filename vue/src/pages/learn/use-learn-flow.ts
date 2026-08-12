import { createEmptyCard, fsrs, type Card, type Grade } from 'ts-fsrs'
import { ref } from 'vue'

import { authState } from '@/entities/auth/auth'
import type { Exercise } from '@/entities/exercise/exercise'
import { candidatesForSituations, saveReview, type ExerciseCandidate } from '@/entities/exercise/local-store'
import { pickCandidate } from '@/entities/exercise/pick-candidate'
import { syncAll } from '@/entities/exercise/sync'
import { getInterestedIds } from '@/entities/situation/interest'

export type Stage = 'loading' | 'empty' | 'noCandidates' | 'front' | 'revealed'

const scheduler = fsrs()

export function useLearnFlow() {
  const stage = ref<Stage>('loading')
  const exercise = ref<Exercise | null>(null)
  let candidate: ExerciseCandidate | null = null

  async function startRound(): Promise<void> {
    const ids = getInterestedIds()
    if (ids.size === 0) {
      stage.value = 'empty'
      return
    }

    const candidates = await candidatesForSituations(ids)
    const picked = pickCandidate(candidates, new Date())
    candidate = picked
    exercise.value = picked?.exercise ?? null
    stage.value = picked ? 'front' : 'noCandidates'
  }

  /** Renders instantly from whatever is already cached locally, then
   * refreshes in the background — the first render never waits on the
   * network. */
  async function loadThenSync(): Promise<void> {
    await startRound()
    await syncAll(getInterestedIds(), authState.status === 'loggedIn')
    await startRound()
  }

  function reveal(): void {
    stage.value = 'revealed'
  }

  async function rate(rating: Grade): Promise<void> {
    const current = candidate
    if (!current) return
    const card: Card = current.card ?? createEmptyCard(new Date())
    const result = scheduler.next(card, new Date(), rating)
    await saveReview(current.exercise.id, result.card)

    void syncAll(getInterestedIds(), authState.status === 'loggedIn')

    await startRound()
  }

  return { stage, exercise, startRound, loadThenSync, reveal, rate }
}
