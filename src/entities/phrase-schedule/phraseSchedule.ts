import { createEmptyCard, fsrs, type Card, type Grade } from 'ts-fsrs'
import { db } from '../../db/db'

const scheduler = fsrs()

// One schedule per (language, situation, communication goal) - the same
// goal key can appear in different situations/languages, so the id is
// scoped to all three.
export function goalCardId(languageCode: string, situationSlug: string, goalKey: string): string {
  return `${languageCode}:${situationSlug}:${goalKey}`
}

export async function getSchedules(): Promise<Map<string, Card>> {
  const rows = await db.schedules.toArray()
  return new Map(rows.map(({ id, ...card }) => [id, card]))
}

export async function rateGoal(id: string, existing: Card | undefined, rating: Grade): Promise<void> {
  const { card } = scheduler.next(existing ?? createEmptyCard(new Date()), new Date(), rating)
  await db.schedules.put({ ...card, id })
}
