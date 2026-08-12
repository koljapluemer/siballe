import { createRouter, createWebHistory } from 'vue-router'

import AddContentFormPage from '@/pages/add/AddContentFormPage.vue'
import AddPage from '@/pages/add/AddPage.vue'
import LearnPage from '@/pages/learn/LearnPage.vue'
import ProfilePage from '@/pages/profile/ProfilePage.vue'
import SituationsPage from '@/pages/situations/SituationsPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'learn', component: LearnPage },
    { path: '/add', name: 'add', component: AddPage },
    { path: '/add/:kind', name: 'add-content', component: AddContentFormPage, props: true },
    { path: '/situations', name: 'situations', component: SituationsPage },
    { path: '/profile', name: 'profile', component: ProfilePage },
  ],
})

export default router
