import { apiGet, apiPost } from '@/db/api-client'

export interface TranslationInput {
  content: string
  note: string
}

export interface AddContentResult {
  nodeId: number | null
  situationId: number
  generationError: string | null
}

export async function searchNodes(kind: string, language: string, query: string): Promise<string[]> {
  if (!query.trim()) return []
  const data = (await apiGet('/nodes/search/', { kind, language, q: query })) as {
    content: string
  }[]
  return data.map((row) => row.content)
}

export async function addContent(params: {
  kind: string
  language: string
  situationDescription: string
  content: string
  translations: TranslationInput[]
  apiKey: string | null
}): Promise<AddContentResult> {
  const data = (await apiPost('/nodes/add-content/', {
    kind: params.kind,
    language: params.language,
    situation_description: params.situationDescription,
    content: params.content,
    translations: params.translations,
    ...(params.apiKey ? { openai_api_key: params.apiKey } : {}),
  })) as { node_id: number | null; situation_id: number; generation_error: string | null }

  return {
    nodeId: data.node_id,
    situationId: data.situation_id,
    generationError: data.generation_error,
  }
}
