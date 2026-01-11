// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/gradient.css'
import Navbar from '@/components/Navbar.vue'
import { initCSRF } from '@/services/api'

// 🔥 Initialize CSRF cookie BEFORE mounting app
initCSRF().then(() => {
  const app = createApp(App)
  
  app.use(router)
  app.component('Navbar', Navbar)
  app.mount('#app')

}).catch(error => {

  // Mount app anyway to show error
  const app = createApp(App)
  app.use(router)
  app.component('Navbar', Navbar)
  app.mount('#app')
})