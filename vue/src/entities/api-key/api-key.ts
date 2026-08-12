/**
 * On-device-only storage for the user's OpenAI API key. Never sent to or
 * stored by our backend — only included, per-request, when the user submits
 * the Add-content form.
 */
const KEY = 'openai_api_key'

export function readApiKey(): string | null {
  return localStorage.getItem(KEY)
}

export function writeApiKey(apiKey: string): void {
  localStorage.setItem(KEY, apiKey)
}

export function deleteApiKey(): void {
  localStorage.removeItem(KEY)
}
