import { createEmptyCard, fsrs, type Card, type Grade } from 'ts-fsrs'
import { db } from '../../db/db'

const scheduler = fsrs()

// One schedule per (language, situation, communication goal) - the same
// goal key can appear in different situations/languages, so the id is
// scoped to all three.
export function goalCardId(languageCode: string, situationSlug: string, goalKey: string): string {
  return `${languageCode}:${situationSlug}:${goalKey}`
}

export function parseGoalCardId(id: string): { languageCode: string; situationSlug: string; goalKey: string } {
  const [languageCode = '', situationSlug = '', ...rest] = id.split(':')
  return { languageCode, situationSlug, goalKey: rest.join(':') }
}

export async function getSchedules(): Promise<Map<string, Card>> {
  const rows = await db.schedules.toArray()
  return new Map(rows.map(({ id, ...card }) => [id, card]))
}

export async function rateGoal(id: string, existing: Card | undefined, rating: Grade): Promise<void> {
  const { card } = scheduler.next(existing ?? createEmptyCard(new Date()), new Date(), rating)
  await db.schedules.put({ ...card, id })
}

// Distinct (language, situation) pairs the user has already practiced at
// least once, each with when it was last reviewed - feeds the home
// screen's "jump back in" cards.
export type PracticedSituation = { languageCode: string; situationSlug: string; lastPracticedAt: Date }

export async function getPracticedSituations(): Promise<PracticedSituation[]> {
  const rows = await db.schedules.toArray()
  const bySituation = new Map<string, PracticedSituation>()

  for (const row of rows) {
    const { languageCode, situationSlug } = parseGoalCardId(row.id)
    if (!languageCode || !situationSlug) continue
    const key = `${languageCode}:${situationSlug}`
    const practicedAt = row.last_review ?? row.due
    const existing = bySituation.get(key)
    if (!existing || practicedAt > existing.lastPracticedAt) {
      bySituation.set(key, { languageCode, situationSlug, lastPracticedAt: practicedAt })
    }
  }

  return [...bySituation.values()]
}
