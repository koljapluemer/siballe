import { apiGet } from '@/db/api-client'

export interface Language {
  code: string
  name: string
}

let cache: Language[] | null = null

export async function listLanguages(): Promise<Language[]> {
  if (cache) return cache
  const data = (await apiGet('/languages/')) as Language[]
  cache = data
  return data
}
