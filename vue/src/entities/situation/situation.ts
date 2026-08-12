import { apiGet } from '@/db/api-client'

export interface Situation {
  id: number
  description: string
  language: string
}

export interface LanguageGroup {
  language: string
  situations: Situation[]
}

interface RawLanguageGroup {
  language: string
  situations: { id: number; description: string }[]
}

function toLanguageGroup(raw: RawLanguageGroup): LanguageGroup {
  return {
    language: raw.language,
    situations: raw.situations.map((s) => ({ ...s, language: raw.language })),
  }
}

export async function fetchGroupedSituations(): Promise<LanguageGroup[]> {
  const data = (await apiGet('/situations/')) as RawLanguageGroup[]
  return data.map(toLanguageGroup)
}

export async function listSituationsForLanguage(languageCode: string): Promise<Situation[]> {
  const data = (await apiGet('/situations/', { language: languageCode })) as RawLanguageGroup[]
  if (data.length === 0) return []
  return toLanguageGroup(data[0]).situations
}
