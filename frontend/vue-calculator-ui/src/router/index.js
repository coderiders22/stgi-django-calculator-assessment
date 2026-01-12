import { createRouter, createWebHistory } from 'vue-router'
import api from '@/services/api'


import Welcome from '../views/Welcome.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import NotFound from '../views/NotFound.vue'

const routes = [
  { path: '/', name: 'Welcome', component: Welcome },
  { path: '/login', name: 'Login', component: Login, meta: { guestOnly: true } },
  { path: '/register', name: 'Register', component: Register, meta: { guestOnly: true } },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
const isGuest = localStorage.getItem('is_guest') === 'true'

  
  if (to.meta.requiresAuth && isGuest) {
    return next()
  }


  if (to.meta.requiresAuth) {
    try {
      const res = await api.get('/auth/me/', { withCredentials: true })
      
    

   
      if (res.data.is_authenticated === true) {
        return next()
      }

 
      return next({ name: 'Login', query: { redirect: to.fullPath } })
    } catch (error) {
     
      return next({ name: 'Login', query: { redirect: to.fullPath } })
    }
  }

  // 🔥 Guest-only routes (login/register)
  if (to.meta.guestOnly) {
    try {
      const res = await api.get('/auth/me/', { withCredentials: true })
      
 

      // If authenticated, redirect to dashboard
      if (res.data.is_authenticated === true) {
        const redirect = to.query.redirect || '/dashboard'
        return next(redirect)
      }

      // If guest mode is active
      if (isGuest) {
        return next('/dashboard')
      }
    } catch (error) {

    }
  }

 
  next()
})

export default router