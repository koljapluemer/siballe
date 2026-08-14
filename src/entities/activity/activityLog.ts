import { db } from '../../db/db'

// Aggregate usage totals (trial count, active-time ms) for the app's own
// Stats page. A single accumulated row is enough here - unlike sam-learns'
// cross-app activity log, there's no per-app/per-day breakdown to feed a
// shared chart, since this app doesn't need one of its own.
const TOTALS_ID = 'totals'

async function getTotals(): Promise<{ id: string; trials: number; activeMs: number }> {
  return (await db.activityTotals.get(TOTALS_ID)) ?? { id: TOTALS_ID, trials: 0, activeMs: 0 }
}

export async function logTrial(): Promise<void> {
  const totals = await getTotals()
  await db.activityTotals.put({ ...totals, trials: totals.trials + 1 })
}

export async function logActiveTimeMs(ms: number): Promise<void> {
  if (!Number.isFinite(ms) || ms <= 0) return
  const totals = await getTotals()
  await db.activityTotals.put({ ...totals, activeMs: totals.activeMs + ms })
}

export async function getActivityStats(): Promise<{ trials: number; activeMs: number }> {
  const { trials, activeMs } = await getTotals()
  return { trials, activeMs }
}
