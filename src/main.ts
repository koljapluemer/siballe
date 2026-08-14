import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { initTheme } from './dumb/theme/theme'

initTheme()

const app = createApp(App)
app.use(router)
app.mount('#app')
