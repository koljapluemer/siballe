import Dexie, { type EntityTable } from 'dexie'
import type { Card } from 'ts-fsrs'

// The single physical Dexie database for the app. Primary keys are
// app-generated strings (crypto.randomUUID()) and table names are plain -
// both deliberately Dexie Cloud compatible, so cloud sync can be added
// later (dexie-cloud-addon + db.cloud.configure()) without a schema change.
export type ScheduleRow = Card & { id: string }
export type ActivityTotalsRow = { id: string; trials: number; activeMs: number }

export const db = new Dexie('siballeDb') as Dexie & {
  schedules: EntityTable<ScheduleRow, 'id'>
  activityTotals: EntityTable<ActivityTotalsRow, 'id'>
}

db.version(1).stores({
  schedules: 'id',
  activityTotals: 'id'
})
