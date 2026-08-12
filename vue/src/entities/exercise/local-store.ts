import type { Card } from 'ts-fsrs'

import { db } from '@/db/dexie'

import type { Exercise, ExercisePoolEntry } from './exercise'

/** An exercise paired with its local FSRS review state, if any. A missing
 * card means the exercise has never been reviewed on this device ("new"). */
export interface ExerciseCandidate {
  exercise: Exercise
  card: Card | null
}

/** A locally-graded review not yet confirmed by the server. */
export interface DirtyReview {
  exerciseId: number
  cardData: Record<string, unknown>
  updatedAt: Date
}

/** One row of the server's authoritative progress state, as returned by
 * POST /sync/exercise-progress/. */
export interface ServerProgressEntry {
  nodeId: number
  cardData: Record<string, unknown>
  updatedAt: Date
}

function reviveCard(cardJson: string): Card {
  const raw = JSON.parse(cardJson) as Record<string, unknown>
  return {
    ...raw,
    due: new Date(raw.due as string),
    last_review: raw.last_review ? new Date(raw.last_review as string) : undefined,
  } as Card
}

/** Refreshes cached exercise content from the pool endpoint. Never touches
 * review cards — content refresh must not reset review progress. */
export async function upsertPool(entries: ExercisePoolEntry[]): Promise<void> {
  const now = new Date()
  await db.transaction('rw', db.exercises, db.exerciseSituations, async () => {
    for (const entry of entries) {
      await db.exercises.put({
        id: entry.exercise.id,
        kind: entry.exercise.kind,
        front: entry.exercise.front,
        back: entry.exercise.back,
        credits: entry.exercise.credits,
        contentUpdatedAt: now,
      })
      for (const situationId of entry.situationIds) {
        const existing = await db.exerciseSituations
          .where('[exerciseId+situationId]')
          .equals([entry.exercise.id, situationId])
          .first()
        if (!existing) {
          await db.exerciseSituations.add({ exerciseId: entry.exercise.id, situationId })
        }
      }
    }
  })
}

/** Exercises eligible under any of the given situations, each paired with
 * its local review state (if any) — the candidate pool the picking strategy
 * chooses from, entirely local, no network involved. */
export async function candidatesForSituations(situationIds: Set<number>): Promise<ExerciseCandidate[]> {
  if (situationIds.size === 0) return []

  const links = await db.exerciseSituations.where('situationId').anyOf([...situationIds]).toArray()
  const exerciseIds = [...new Set(links.map((l) => l.exerciseId))]
  if (exerciseIds.length === 0) return []

  const [exercises, cards] = await Promise.all([
    db.exercises.bulkGet(exerciseIds),
    db.reviewCards.bulkGet(exerciseIds),
  ])

  const candidates: ExerciseCandidate[] = []
  exerciseIds.forEach((_id, i) => {
    const exercise = exercises[i]
    if (!exercise) return
    const cardRow = cards[i]
    candidates.push({
      exercise,
      card: cardRow ? reviveCard(cardRow.cardJson) : null,
    })
  })
  return candidates
}

/** Records a graded review locally and marks it dirty for the next sync. */
export async function saveReview(exerciseId: number, card: Card): Promise<void> {
  await db.reviewCards.put({
    exerciseId,
    cardJson: JSON.stringify(card),
    due: card.due,
    updatedAt: new Date(),
    dirty: true,
  })
}

export async function dirtyCards(): Promise<DirtyReview[]> {
  const rows = (await db.reviewCards.toArray()).filter((row) => row.dirty)
  return rows.map((row) => ({
    exerciseId: row.exerciseId,
    cardData: JSON.parse(row.cardJson) as Record<string, unknown>,
    updatedAt: row.updatedAt,
  }))
}

/** Merges the server's authoritative progress set back in. The server has
 * already resolved last-write-wins, so an entry only gets dropped locally if
 * it's somehow older than what's already here. */
export async function applyServerState(entries: ServerProgressEntry[]): Promise<void> {
  await db.transaction('rw', db.reviewCards, async () => {
    for (const entry of entries) {
      const existing = await db.reviewCards.get(entry.nodeId)
      if (existing && existing.updatedAt > entry.updatedAt) continue
      await db.reviewCards.put({
        exerciseId: entry.nodeId,
        cardJson: JSON.stringify(entry.cardData),
        due: new Date(entry.cardData.due as string),
        updatedAt: entry.updatedAt,
        dirty: false,
      })
    }
  })
}
