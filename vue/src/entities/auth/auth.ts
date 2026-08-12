import { apiGet, apiPost, ApiException } from '@/db/api-client'
import { authState, setLoggedIn, setLoggedOut } from '@/db/auth-state'
import { clearTokens, getAccessToken, saveTokens } from '@/db/token-store'

export { authState }

interface TokenPair {
  access: string
  refresh: string
}

async function loadMe(): Promise<void> {
  const data = (await apiGet('/auth/me/')) as { username: string }
  setLoggedIn(data.username)
}

export async function register(username: string, email: string, password: string): Promise<void> {
  const data = (await apiPost('/auth/register/', {
    username,
    email,
    password,
    password_confirm: password,
  })) as TokenPair
  saveTokens(data.access, data.refresh)
  await loadMe()
}

export async function login(username: string, password: string): Promise<void> {
  const data = (await apiPost('/auth/token/', { username, password })) as TokenPair
  saveTokens(data.access, data.refresh)
  await loadMe()
}

export function logout(): void {
  clearTokens()
  setLoggedOut()
}

/** Restores login state from stored tokens at app start. */
export async function restoreSession(): Promise<void> {
  if (!getAccessToken()) {
    setLoggedOut()
    return
  }
  try {
    await loadMe()
  } catch (e) {
    // The api client already attempts one silent refresh internally, so a
    // failure here means the session is genuinely dead.
    if (e instanceof ApiException) {
      clearTokens()
      setLoggedOut()
    }
  }
}
