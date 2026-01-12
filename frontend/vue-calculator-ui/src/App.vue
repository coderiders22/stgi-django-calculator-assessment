import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Navbar from '@/components/Navbar.vue'
import { initCSRF } from '@/services/api'
import { auth } from '@/stores/auth'

async function bootstrap() {
  await initCSRF()
  await auth.init()  

  const app = createApp(App)
  app.use(router)
  app.component('Navbar', Navbar)
  app.mount('#app')
}

bootstrap()
