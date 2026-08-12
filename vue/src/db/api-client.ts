import { setLoggedOut } from './auth-state'
import { clearTokens, getAccessToken, getRefreshToken, saveAccessToken } from './token-store'

export const apiBaseUrl: string =
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api'

export class ApiException extends Error {
  statusCode?: number

  constructor(message: string, statusCode?: number) {
    super(message)
    this.statusCode = statusCode
  }
}

function buildUrl(path: string, query?: Record<string, string>): string {
  const url = new URL(`${apiBaseUrl}${path}`)
  if (query) {
    for (const [key, value] of Object.entries(query)) {
      url.searchParams.set(key, value)
    }
  }
  return url.toString()
}

async function authHeaders(): Promise<Record<string, string>> {
  const access = getAccessToken()
  return access ? { Authorization: `Bearer ${access}` } : {}
}

async function refreshAccessToken(): Promise<boolean> {
  const refresh = getRefreshToken()
  if (!refresh) return false
  try {
    const response = await fetch(`${apiBaseUrl}/auth/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh }),
    })
    if (!response.ok) return false
    const data = (await response.json()) as { access: string }
    saveAccessToken(data.access)
    return true
  } catch {
    return false
  }
}

/**
 * Sends a request with the current access token attached (if any). On a 401,
 * attempts one silent token refresh and retries once; if the refresh also
 * fails, the stored tokens are cleared and auth state moves to loggedOut.
 */
async function sendWithRetry(
  send: (headers: Record<string, string>) => Promise<Response>,
): Promise<Response> {
  let response: Response
  try {
    response = await send(await authHeaders())
  } catch (e) {
    throw new ApiException(`Could not reach the server: ${String(e)}`)
  }

  if (response.status === 401) {
    if (await refreshAccessToken()) {
      try {
        response = await send(await authHeaders())
      } catch (e) {
        throw new ApiException(`Could not reach the server: ${String(e)}`)
      }
    } else {
      clearTokens()
      setLoggedOut()
    }
  }
  return response
}

async function decode(response: Response): Promise<unknown> {
  if (response.ok) {
    if (response.status === 204) return null
    return response.json()
  }

  const text = await response.text()
  let detail = text
  try {
    const decoded = JSON.parse(text)
    if (decoded && typeof decoded === 'object' && 'detail' in decoded) {
      detail = String((decoded as { detail: unknown }).detail)
    }
  } catch {
    // body wasn't JSON, keep raw text
  }
  throw new ApiException(detail, response.status)
}

export async function apiGet(path: string, query?: Record<string, string>): Promise<unknown> {
  const url = buildUrl(path, query)
  const response = await sendWithRetry((headers) => fetch(url, { headers }))
  return decode(response)
}

export async function apiPost(path: string, body: unknown): Promise<unknown> {
  const url = buildUrl(path)
  const response = await sendWithRetry((headers) =>
    fetch(url, {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }),
  )
  return decode(response)
}
