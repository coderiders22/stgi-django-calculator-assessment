import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/gradient.css'

import Navbar from '@/components/Navbar.vue'
import { initCSRF } from '@/services/api'


async function bootstrap() {
  try {
    await initCSRF()
  } catch (e) {
    console.warn('CSRF init error:', e)
  }

  const app = createApp(App)
  app.use(router)
  app.component('Navbar', Navbar)
  app.mount('#app')
}

bootstrap()
