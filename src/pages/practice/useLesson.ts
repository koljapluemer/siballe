// A lesson run: up to LESSON_SIZE exercises for one (language, situation)
// pair, drawn once up front and then stepped through in order - unlike the
// old infinite queue, the set doesn't change while the run is in progress.
import { computed, onMounted, ref } from 'vue'
import { Rating, type Card } from 'ts-fsrs'
import { logTrial } from '../../entities/activity/activityLog'
import { getSituationGoals, type PhraseGoal } from '../../entities/phrase-catalog/phraseCatalog'
import { getSchedules, goalCardId, initGoal, rateGoal } from '../../entities/phrase-schedule/phraseSchedule'

export type LessonExercise = { goal: PhraseGoal; id: string; schedule: Card | undefined }

const LESSON_SIZE = 10

function shuffle<T>(items: T[]): T[] {
  const result = [...items]
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[result[i], result[j]] = [result[j], result[i]]
  }
  return result
}

export function useLesson(languageCode: string, situationSlug: string) {
  const loading = ref(true)
  const exercises = ref<LessonExercise[]>([])
  const index = ref(0)
  const correctCount = ref(0)
  const finished = ref(false)

  const current = computed(() => (finished.value ? null : (exercises.value[index.value] ?? null)))
  const total = computed(() => exercises.value.length)

  async function build(): Promise<void> {
    loading.value = true
    finished.value = false
    index.value = 0
    correctCount.value = 0

    const [goals, schedules] = await Promise.all([
      getSituationGoals(languageCode, situationSlug),
      getSchedules()
    ])
    const now = new Date()
    const candidates = goals.map((goal) => {
      const id = goalCardId(languageCode, situationSlug, goal.key)
      return { goal, id, schedule: schedules.get(id) }
    })

    // Prioritize what's due, then what's never been seen, then whatever's
    // soonest to come due - so a lesson always favors the phrases that most
    // need review.
    const due = candidates
      .filter((c) => c.schedule && c.schedule.due <= now)
      .sort((a, b) => a.schedule!.due.getTime() - b.schedule!.due.getTime())
    const unseen = shuffle(candidates.filter((c) => !c.schedule))
    const upcoming = candidates
      .filter((c) => c.schedule && c.schedule.due > now)
      .sort((a, b) => a.schedule!.due.getTime() - b.schedule!.due.getTime())

    exercises.value = [...due, ...unseen, ...upcoming].slice(0, LESSON_SIZE)
    loading.value = false
  }

  function advance(): void {
    if (index.value + 1 < exercises.value.length) {
      index.value += 1
    } else {
      finished.value = true
    }
  }

  async function rate(kind: 'correct' | 'wrong'): Promise<void> {
    const exercise = current.value
    if (!exercise) return
    if (kind === 'correct') correctCount.value += 1
    await rateGoal(exercise.id, exercise.schedule, kind === 'correct' ? Rating.Good : Rating.Again)
    await logTrial()
    advance()
  }

  // For an exercise on content never seen before: acknowledges it was shown
  // without grading recall, since there's nothing to score yet.
  async function acknowledge(): Promise<void> {
    const exercise = current.value
    if (!exercise) return
    await initGoal(exercise.id)
    await logTrial()
    advance()
  }

  onMounted(build)

  return { loading, current, index, total, correctCount, finished, rate, acknowledge, restart: build }
}
