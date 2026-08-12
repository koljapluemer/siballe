import Dexie, { type EntityTable } from 'dexie'

/** Cached exercise content, keyed by the backend's stable node id. */
export interface ExerciseRow {
  id: number
  kind: string
  front: string
  back: string
  credits: string
  contentUpdatedAt: Date
}

/** Many-to-many: which situations each exercise is eligible under. */
export interface ExerciseSituationRow {
  id?: number
  exerciseId: number
  situationId: number
}

/**
 * FSRS review state for an exercise. Absence of a row for an exercise id
 * means "new/never reviewed".
 */
export interface ReviewCardRow {
  exerciseId: number
  cardJson: string
  due: Date
  updatedAt: Date
  dirty: boolean
}

const db = new Dexie('siballe') as Dexie & {
  exercises: EntityTable<ExerciseRow, 'id'>
  exerciseSituations: EntityTable<ExerciseSituationRow, 'id'>
  reviewCards: EntityTable<ReviewCardRow, 'exerciseId'>
}

db.version(1).stores({
  exercises: 'id',
  exerciseSituations: '++id, exerciseId, situationId, [exerciseId+situationId]',
  reviewCards: 'exerciseId',
})

export { db }
