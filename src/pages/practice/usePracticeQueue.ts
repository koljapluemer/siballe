import { onMounted, ref } from 'vue'
import { Rating, type Card, type Grade } from 'ts-fsrs'
import { logTrial } from '../../entities/activity/activityLog'
import { getSituationGoals, type PhraseGoal } from '../../entities/phrase-catalog/phraseCatalog'
import { getSchedules, goalCardId, rateGoal } from '../../entities/phrase-schedule/phraseSchedule'

export type PracticeCandidate = { goal: PhraseGoal; id: string; schedule: Card | undefined }

let lastGoalKey: string | null = null

export function usePracticeQueue(languageCode: string, situationSlug: string) {
  const loading = ref(true)
  const candidate = ref<PracticeCandidate | null>(null)

  async function loadNext(): Promise<void> {
    loading.value = true
    const [goals, schedules] = await Promise.all([
      getSituationGoals(languageCode, situationSlug),
      getSchedules()
    ])
    const now = new Date()
    const eligible = goals
      .map((goal) => {
        const id = goalCardId(languageCode, situationSlug, goal.key)
        return { goal, id, schedule: schedules.get(id) }
      })
      .filter(({ schedule }) => !schedule || schedule.due <= now)

    const due = eligible.filter(({ schedule }) => schedule)
    const unseen = eligible.filter(({ schedule }) => !schedule)
    const preferred = due.length > 0 ? due : unseen
    const withoutPrevious = preferred.filter(({ goal }) => goal.key !== lastGoalKey)
    const pool = withoutPrevious.length > 0 ? withoutPrevious : preferred

    const next = pool.length > 0 ? (pool[Math.floor(Math.random() * pool.length)] ?? null) : null
    lastGoalKey = next?.goal.key ?? null
    candidate.value = next
    loading.value = false
  }

  async function rate(rating: Grade): Promise<void> {
    if (!candidate.value) return
    await rateGoal(candidate.value.id, candidate.value.schedule, rating)
    await logTrial()
    await loadNext()
  }

  onMounted(loadNext)

  return { loading, candidate, rate, Rating }
}
