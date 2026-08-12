/**
 * Frontend-only persistence of which situations the user wants to learn.
 * Never synced to the backend — there's no field for it there.
 */
const KEY = 'interested_situation_ids'

export function getInterestedIds(): Set<number> {
  const stored = JSON.parse(localStorage.getItem(KEY) ?? '[]') as number[]
  return new Set(stored)
}

export function setInterested(situationId: number, interested: boolean): void {
  const ids = getInterestedIds()
  if (interested) {
    ids.add(situationId)
  } else {
    ids.delete(situationId)
  }
  localStorage.setItem(KEY, JSON.stringify([...ids]))
}
