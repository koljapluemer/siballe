import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('./pages/home/PageHome.vue'),
      meta: {
        title: 'siballe',
        description: 'Memorize core phrases for everyday situations, by target language.'
      }
    },
    {
      path: '/practice/:languageCode/:situationSlug',
      name: 'practice',
      component: () => import('./pages/practice/PagePractice.vue'),
      props: true,
      meta: {
        title: 'Practice | siballe',
        description: 'Practice target-language phrases by situation with FSRS spaced repetition.'
      }
    },
    {
      path: '/stats',
      name: 'stats',
      component: () => import('./pages/stats/PageStats.vue'),
      meta: {
        title: 'Stats | siballe',
        description: 'Time spent and phrases practiced.'
      }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('./pages/settings/PageSettings.vue'),
      meta: {
        title: 'Settings | siballe',
        description: 'App settings.'
      }
    }
  ] satisfies RouteRecordRaw[]
})

router.afterEach((to) => {
  const baseTitle = 'siballe'
  const routeTitle = typeof to.meta.title === 'string' ? to.meta.title : ''
  document.title = routeTitle || baseTitle

  const description =
    typeof to.meta.description === 'string'
      ? to.meta.description
      : 'Memorize core phrases for everyday situations, by target language.'
  let descriptionTag = document.querySelector('meta[name="description"]')

  if (!descriptionTag) {
    descriptionTag = document.createElement('meta')
    descriptionTag.setAttribute('name', 'description')
    document.head.appendChild(descriptionTag)
  }

  descriptionTag.setAttribute('content', description)
})

export default router
