import { reactive } from 'vue'

export type AuthStatus = 'unknown' | 'loggedOut' | 'loggedIn'

/**
 * Current login status, shared by the api client (to know whether/when to
 * clear tokens on a failed refresh) and the Profile page (to render login
 * state).
 */
export const authState = reactive<{ status: AuthStatus; username: string | null }>({
  status: 'unknown',
  username: null,
})

export function setLoggedIn(username: string): void {
  authState.username = username
  authState.status = 'loggedIn'
}

export function setLoggedOut(): void {
  if (authState.status === 'loggedOut') return
  authState.username = null
  authState.status = 'loggedOut'
}
