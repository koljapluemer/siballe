// Reads the static phrase catalog from public/data/phrases/, curated by the
// phrases CMS (cms/phrases/). Per language: index.json lists situations,
// <situation-slug>.json holds that situation's communication goals and their
// target-language expressions, and audio/<slug>.mp3 holds each expression's
// clip (see dumb/slugify.ts for the filename convention).
import { slugify } from '../../dumb/slugify'

export type PhraseLanguage = { code: string; name: string }
export type PhraseSituation = { slug: string; name: string }
export type PhraseExpression = { text: string; note?: string }
export type PhraseGoal = { key: string; expressions: PhraseExpression[] }

type RawExpressionEntry = { note?: string }
type RawGoalEntry = { expressions: Record<string, RawExpressionEntry> }
type RawSituationContent = Record<string, RawGoalEntry>

async function loadJson<T>(url: string): Promise<T> {
  const response = await fetch(url)
  if (!response.ok) throw new Error(`Failed to load ${url} (${response.status})`)
  return response.json() as Promise<T>
}

let languagesPromise: Promise<PhraseLanguage[]> | null = null

export function getLanguages(): Promise<PhraseLanguage[]> {
  languagesPromise ??= loadJson<Record<string, string>>('/data/phrases/languages.json').then((record) =>
    Object.entries(record).map(([code, name]) => ({ code, name }))
  )
  return languagesPromise
}

const situationIndexCache = new Map<string, Promise<PhraseSituation[]>>()

export function getSituations(languageCode: string): Promise<PhraseSituation[]> {
  let promise = situationIndexCache.get(languageCode)
  if (!promise) {
    promise = loadJson<Record<string, string>>(`/data/phrases/${languageCode}/index.json`).then((record) =>
      Object.entries(record).map(([slug, name]) => ({ slug, name }))
    )
    situationIndexCache.set(languageCode, promise)
  }
  return promise
}

const situationGoalsCache = new Map<string, Promise<PhraseGoal[]>>()

export function getSituationGoals(languageCode: string, situationSlug: string): Promise<PhraseGoal[]> {
  const cacheKey = `${languageCode}/${situationSlug}`
  let promise = situationGoalsCache.get(cacheKey)
  if (!promise) {
    promise = loadJson<RawSituationContent>(`/data/phrases/${languageCode}/${situationSlug}.json`).then((record) =>
      Object.entries(record).map(([key, goal]) => ({
        key,
        expressions: Object.entries(goal.expressions).map(([text, entry]) => ({ text, note: entry.note }))
      }))
    )
    situationGoalsCache.set(cacheKey, promise)
  }
  return promise
}

export function getExpressionAudioUrl(languageCode: string, expressionText: string): string {
  return `/data/phrases/${languageCode}/audio/${slugify(expressionText)}.mp3`
}
