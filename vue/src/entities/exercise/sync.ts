import { apiPost, ApiException } from '@/db/api-client'

import { fetchExercisePool } from './exercise'
import { applyServerState, dirtyCards, upsertPool, type ServerProgressEntry } from './local-store'

/**
 * Best-effort background sync: refreshes the local exercise pool for the
 * given situations, and — if logged in — pushes locally graded reviews and
 * merges the server's authoritative progress back in. Failures (offline,
 * server error, not logged in) are swallowed; the UI already has everything
 * it needs from local storage regardless of sync outcome.
 */
export async function syncAll(interestedSituationIds: Set<number>, loggedIn: boolean): Promise<void> {
  await refreshPool(interestedSituationIds)
  if (loggedIn) await syncProgress()
}

async function refreshPool(situationIds: Set<number>): Promise<void> {
  if (situationIds.size === 0) return
  try {
    const entries = await fetchExercisePool(situationIds)
    await upsertPool(entries)
  } catch (e) {
    if (!(e instanceof ApiException)) throw e
  }
}

async function syncProgress(): Promise<void> {
  try {
    const dirty = await dirtyCards()
    const response = (await apiPost('/sync/exercise-progress/', {
      progress: dirty.map((d) => ({
        node_id: d.exerciseId,
        card_data: d.cardData,
        updated_at: d.updatedAt.toISOString(),
      })),
    })) as { progress: { node_id: number; card_data: Record<string, unknown>; updated_at: string }[] }

    const entries: ServerProgressEntry[] = response.progress.map((e) => ({
      nodeId: e.node_id,
      cardData: e.card_data,
      updatedAt: new Date(e.updated_at),
    }))
    await applyServerState(entries)
  } catch (e) {
    if (!(e instanceof ApiException)) throw e
  }
}
