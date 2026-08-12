import { apiGet } from '@/db/api-client'

export interface Exercise {
  id: number
  kind: string
  front: string
  back: string
  credits: string
}

/** One entry from GET /exercises/pool/ — an exercise plus the situations it's
 * eligible under, used to populate the local cache. */
export interface ExercisePoolEntry {
  exercise: Exercise
  situationIds: number[]
}

interface RawPoolEntry extends Exercise {
  situation_ids: number[]
}

export async function generateExercise(situationId: number): Promise<Exercise> {
  return (await apiGet('/exercises/generate/', {
    situation_id: String(situationId),
  })) as Exercise
}

export async function fetchExercisePool(situationIds: Set<number>): Promise<ExercisePoolEntry[]> {
  const data = (await apiGet('/exercises/pool/', {
    situation_ids: [...situationIds].join(','),
  })) as { results: RawPoolEntry[] }

  return data.results.map((row) => ({
    exercise: { id: row.id, kind: row.kind, front: row.front, back: row.back, credits: row.credits },
    situationIds: row.situation_ids,
  }))
}
