
<template>
  <nav class="navbar" :class="{ scrolled: isScrolled, transparent: isTransparent }">
    <div class="nav-container">
      <!-- Logo -->
      <router-link to="/" class="logo-wrapper">
        <div class="logo-icon">
          <Calculator :size="24" />
        </div>
        <span class="logo-text">CalculatorPro</span>
      </router-link>

      <!-- Desktop Navigation -->
      <div class="nav-links">
        <router-link
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          class="nav-link"
          :class="{ active: isActive(link.path) }"
        >
          <component :is="link.icon" :size="18" />
          <span>{{ link.label }}</span>
        </router-link>
      </div>

      <!-- Actions -->
      <div class="nav-actions">
        <!-- ===== GUEST MODE (DESKTOP) ===== -->
        <div v-if="isGuest && !username" class="user-menu">
          <button class="user-button guest" @click="userMenuOpen = !userMenuOpen">
            <div class="user-avatar">
              <Shield :size="18" />
            </div>
            <span class="user-name">Guest Mode</span>
            <ChevronDown :size="16" :class="{ rotated: userMenuOpen }" />
          </button>

          <transition name="dropdown">
            <div v-if="userMenuOpen" class="user-dropdown">
              <div class="dropdown-header">
                <div class="dropdown-avatar">
                  <Shield :size="20" />
                </div>
                <div class="dropdown-info">
                  <div class="dropdown-name">Guest Session</div>
                  <div class="dropdown-email">Limited access</div>
                </div>
              </div>

              <div class="dropdown-divider"></div>

              <button class="dropdown-item logout" @click="exitGuest">
                <LogOut :size="16" />
                Exit Guest Mode
              </button>
            </div>
          </transition>
        </div>

        <!-- ===== NOT LOGGED IN (DESKTOP) ===== -->
        <div v-else-if="!username" class="auth-buttons">
          <router-link to="/login" class="btn btn-ghost">
            <LogIn :size="16" /> Sign in
          </router-link>
          <router-link to="/register" class="btn btn-primary">
            <Rocket :size="16" /> Get Started
          </router-link>
        </div>

        <!-- ===== LOGGED IN USER ===== -->
        <div v-else class="user-menu">
          <button class="user-button" @click="userMenuOpen = !userMenuOpen">
            <div class="user-avatar">
              <User :size="18" />
            </div>
            <span class="user-name">{{ username }}</span>
            <ChevronDown :size="16" :class="{ rotated: userMenuOpen }" />
          </button>

          <transition name="dropdown">
            <div v-if="userMenuOpen" class="user-dropdown">
              <div class="dropdown-header">
                <div class="dropdown-avatar">
                  <User :size="20" />
                </div>
                <div class="dropdown-info">
                  <div class="dropdown-name">{{ username }}</div>
                  <div class="dropdown-email">Authenticated</div>
                </div>
              </div>

              <div class="dropdown-divider"></div>

              <router-link to="/dashboard" class="dropdown-item" @click="closeMenus">
                <LayoutDashboard :size="16" /> Dashboard
              </router-link>

              <div class="dropdown-divider"></div>

              <button class="dropdown-item logout" @click="logout">
                <LogOut :size="16" /> Sign out
              </button>
            </div>
          </transition>
        </div>

        <!-- Mobile Menu -->
        <button class="mobile-menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">
          <Menu v-if="!mobileMenuOpen" />
          <X v-else />
        </button>
      </div>
    </div>

    <!-- ===== MOBILE SIDEBAR ===== -->
    <teleport to="body">
      <transition name="sidebar">
        <div v-if="mobileMenuOpen" class="mobile-sidebar">
          <div class="sidebar-header">
            <span class="logo-text">CalculatorPro</span>
            <button class="sidebar-close-btn" @click="mobileMenuOpen = false">
              <X />
            </button>
          </div>

          <!-- Guest / User Card -->
          <div
            v-if="username || isGuest"
            class="sidebar-user-info"
            :class="{ guest: isGuest }"
          >
            <div class="user-avatar-large">
              <Shield v-if="isGuest" :size="24" />
              <User v-else :size="24" />
            </div>
            <div class="user-details">
              <div class="user-name">{{ username || 'Guest Mode' }}</div>
              <div class="user-email">{{ isGuest ? 'Limited access' : 'Authenticated' }}</div>
            </div>
          </div>

          <!-- Links -->
          <div class="sidebar-links">
            <router-link
              v-for="link in navLinks"
              :key="link.path"
              :to="link.path"
              class="sidebar-link"
              :class="{ active: isActive(link.path) }"
              @click="mobileMenuOpen = false"
            >
              <component :is="link.icon" :size="18" />
              {{ link.label }}
            </router-link>
          </div>

          <!-- Actions -->
          <div class="sidebar-actions">
            <button v-if="username" class="sidebar-logout" @click="logout">
              <LogOut :size="18" />
              Sign Out
            </button>

            <button
              v-else-if="isGuest"
              class="sidebar-logout"
              @click="exitGuest"
            >
              <LogOut :size="18" />
              Exit Guest Mode
            </button>

            <div v-else class="sidebar-auth-buttons">
              <router-link to="/login" class="sidebar-btn ghost" @click="mobileMenuOpen = false">
                <LogIn :size="18" />
                Sign In
              </router-link>
              <router-link to="/register" class="sidebar-btn primary" @click="mobileMenuOpen = false">
                <Rocket :size="18" />
                Get Started
              </router-link>
            </div>
          </div>
        </div>
      </transition>

      <div
        v-if="mobileMenuOpen"
        class="sidebar-backdrop"
        @click="mobileMenuOpen = false"
      />
    </teleport>
  </nav>
</template>

<script>
import {
  Calculator,
  Home,
  LayoutDashboard,
  User,
  Shield,
  ChevronDown,
  Rocket,
  LogOut,
  LogIn,
  Menu,
  X
} from 'lucide-vue-next'

import api from '@/services/api'

export default {
  components: {
    Calculator,
    Home,
    LayoutDashboard,
    User,
    Shield,
    ChevronDown,
    Rocket,
    LogOut,
    LogIn,
    Menu,
    X
  },

  data() {
    return {
      isScrolled: false,
      mobileMenuOpen: false,
      userMenuOpen: false,
      username: null,  // 🔥 Use API data instead of localStorage
      navLinks: [
        { label: 'Home', path: '/', icon: 'Home' },
        { label: 'Dashboard', path: '/dashboard', icon: 'LayoutDashboard' }
      ]
    }
  },

  computed: {
    isGuest() {
      return localStorage.getItem('is_guest') === 'true'
    },
    isTransparent() {
      return this.$route.path === '/' && !this.isScrolled
    }
  },

  async mounted() {
    window.addEventListener('scroll', () => {
      this.isScrolled = window.scrollY > 20
    })

    // 🔥 Fetch user data on mount
    await this.fetchUser()
  },

  methods: {
    // 🔥 Fetch current user from API
    async fetchUser() {
      try {
        const res = await api.get('/auth/me/', { withCredentials: true })
        
        if (res.data.is_authenticated) {
          this.username = res.data.username
          localStorage.removeItem('is_guest')  // Clear guest mode if authenticated
        } else {
          this.username = null
        }
      } catch (error) {
      
        this.username = null
      }
    },

    closeMenus() {
      this.userMenuOpen = false
      this.mobileMenuOpen = false
    },

    async logout() {
      try {
        await api.post('/auth/logout/', {}, { withCredentials: true })
      } catch (error) {
     
      } finally {
        // Clear all local data
        localStorage.clear()
        this.username = null
        this.closeMenus()
        this.$router.push('/login')
      }
    },

    exitGuest() {
      localStorage.removeItem('is_guest')
      this.closeMenus()
      this.$router.push('/login')
    },

    isActive(path) {
      return this.$route.path === path
    }
  },

  // 🔥 Watch route changes to update user data
  watch: {
    '$route'() {
      this.fetchUser()
    }
  }
}
</script>


<style scoped>
/* NAVBAR + SIDEBAR MOBILE MENU */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999997;
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border-bottom: 1px solid rgba(0,0,0,0.08);
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.navbar.transparent {
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border-bottom: none;
}
.navbar.scrolled {
  background: rgba(255,255,255,0.98);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
.nav-container {
  max-width: 1480px;
  margin: 0 auto;
  padding: 1rem 5vw;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 70px;
}
/* Logo */
.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  transition: all 0.3s ease;
}
.logo-wrapper:hover {
  transform: translateY(-2px);
}
.logo-icon {
  width: 42px;
  height: 42px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(59,130,246,0.2);
}
.logo-text {
  font-size: 1.4rem;
  font-weight: 800;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
/* Desktop Nav Links */
.nav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.2rem;
  color: #64748b;
  font-weight: 500;
  font-size: 0.95rem;
  text-decoration: none;
  border-radius: 10px;
  transition: all 0.2s ease;
}
.nav-link:hover {
  color: #1e293b;
  background: rgba(59,130,246,0.06);
}
.nav-link.active {
  color: #3b82f6;
  background: rgba(59,130,246,0.08);
  font-weight: 600;
}
/* Desktop Auth & User Menu */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.auth-buttons {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.user-menu {
  position: relative;
  display: flex;
}
.user-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.6rem 1rem;
  background: rgba(59,130,246,0.06);
  border: 1px solid rgba(59,130,246,0.15);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}
.user-button:hover {
  background: rgba(59,130,246,0.1);
  border-color: rgba(59,130,246,0.25);
  transform: translateY(-2px);
}
.user-avatar {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}
.user-name {
  font-weight: 600;
  color: #1e293b;
}
.chevron {
  color: #64748b;
  transition: transform 0.3s ease;
}
.chevron.rotated {
  transform: rotate(180deg);
}
.user-dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  width: 280px;
  background: white;
  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 16px;
  box-shadow: 0 12px 32px rgba(0,0,0,0.12);
  overflow: hidden;
}
.dropdown-header {
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  background: linear-gradient(135deg, rgba(59,130,246,0.05), rgba(139,92,246,0.05));
}
.dropdown-avatar {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}
.dropdown-info {
  flex: 1;
}
.dropdown-name {
  font-weight: 600;
  color: #1e293b;
  font-size: 1rem;
}
.dropdown-email {
  font-size: 0.85rem;
  color: #64748b;
}
.dropdown-divider {
  height: 1px;
  background: rgba(0,0,0,0.06);
  margin: 0.5rem 0;
}
.dropdown-section {
  padding: 0.5rem;
}
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #64748b;
  font-size: 0.95rem;
  font-weight: 500;
  text-decoration: none;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  border-radius: 8px;
  transition: all 0.2s ease;
  cursor: pointer;
}
.dropdown-item:hover {
  background: rgba(59,130,246,0.06);
  color: #1e293b;
}
.dropdown-item.logout {
  color: #ef4444;
}
.dropdown-item.logout:hover {
  background: rgba(239,68,68,0.06);
}
.dropdown-backdrop {
  position: fixed;
  inset: 0;
  z-index: 999996;
  background: transparent;
}
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.25rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  transition: all 0.3s ease;
}
.btn-ghost {
  background: transparent;
  border: 1.5px solid rgba(0,0,0,0.15);
  color: #1e293b;
}
.btn-ghost:hover {
  background: rgba(0,0,0,0.04);
  border-color: rgba(0,0,0,0.25);
}
.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(59,130,246,0.25);
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(59,130,246,0.35);
}
/* Mobile Menu Toggle - Hidden by Default on Desktop */
.mobile-menu-btn {
  background: none;
  border: none;
  color: #1e293b;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: background 0.2s;
  display: none;
}
.mobile-menu-btn:hover {
  background: rgba(0,0,0,0.05);
}
/* ================================================
   MOBILE SIDEBAR - WITH !IMPORTANT FLAGS
=============================================== */
.mobile-sidebar {
  position: fixed !important;
  top: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 320px;
  max-width: 85vw;
  background: white !important;
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.15) !important;
  z-index: 2147483647 !important;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 1.25rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.03), rgba(139, 92, 246, 0.03));
}
.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.sidebar-logo-icon {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}
.sidebar-logo-text {
  font-size: 1.35rem;
  font-weight: 800;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.sidebar-close-btn {
  background: rgba(0, 0, 0, 0.05);
  border: none;
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}
.sidebar-close-btn:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #1e293b;
}
.sidebar-user-info {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1.25rem;
  margin: 1rem 1.25rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.08));
  border-radius: 14px;
  border: 1px solid rgba(59, 130, 246, 0.12);
}
.user-avatar-large {
  width: 52px;
  height: 52px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}
.user-details {
  flex: 1;
  min-width: 0;
}
.user-details .user-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.user-details .user-email {
  color: #64748b;
  font-size: 0.85rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sidebar-links {
  flex: 1;
  padding: 0.5rem 1.25rem;
}
.sidebar-section-title {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8;
  margin-bottom: 0.75rem;
  padding: 0 0.5rem;
}
.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.875rem 1rem;
  margin-bottom: 0.25rem;
  font-size: 0.975rem;
  font-weight: 500;
  color: #475569;
  text-decoration: none;
  border-radius: 10px;
  transition: all 0.2s;
}
.sidebar-link:hover {
  background: rgba(59, 130, 246, 0.08);
  color: #1e293b;
}
.sidebar-link.active {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.12), rgba(139, 92, 246, 0.08));
  color: #3b82f6;
  font-weight: 600;
}
.sidebar-actions {
  padding: 1.25rem;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(0, 0, 0, 0.01);
}
.sidebar-logout {
  width: 100%;
  padding: 0.875rem;
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 10px;
  color: #ef4444;
  font-weight: 600;
  font-size: 0.975rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  transition: all 0.2s;
}
.sidebar-logout:hover {
  background: rgba(239, 68, 68, 0.15);
}
.sidebar-auth-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}
.sidebar-btn {
  padding: 0.875rem 1rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.975rem;
  text-align: center;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  transition: all 0.2s;
}
.sidebar-btn.ghost {
  background: transparent;
  border: 2px solid #3b82f6;
  color: #3b82f6;
}
.sidebar-btn.ghost:hover {
  background: rgba(59, 130, 246, 0.08);
}
.sidebar-btn.primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}
.sidebar-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(59, 130, 246, 0.4);
}
/* Sidebar Backdrop */
.sidebar-backdrop {
  position: fixed !important;
  inset: 0 !important;
  background: rgba(0, 0, 0, 0.5) !important;
  z-index: 2147483646 !important;
  backdrop-filter: blur(4px);
}
/* Animations */
.sidebar-enter-active,
.sidebar-leave-active {
  transition: transform 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
}
.sidebar-enter-from,
.sidebar-leave-to {
  transform: translateX(100%);
}
.backdrop-enter-active,
.backdrop-leave-active {
  transition: opacity 0.3s ease;
}
.backdrop-enter-from,
.backdrop-leave-to {
  opacity: 0;
}
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
/* Responsive */
@media (max-width: 1024px) {
  .nav-links,
  .auth-buttons,
  .user-menu {
    display: none;
  }
 
  .mobile-menu-btn {
    display: block;
  }
}
@media (max-width: 380px) {
  .mobile-sidebar {
    width: 280px;
  }
 
  .sidebar-header {
    padding: 1.25rem 1rem;
  }
 
  .sidebar-logo-icon {
    width: 40px;
    height: 40px;
  }
 
  .sidebar-logo-text {
    font-size: 1.2rem;
  }
 
  .sidebar-user-info {
    margin: 0.875rem 1rem;
    padding: 1rem;
  }
 
  .user-avatar-large {
    width: 46px;
    height: 46px;
  }
 
  .sidebar-links {
    padding: 0.5rem 1rem;
  }
 
  .sidebar-actions {
    padding: 1rem;
  }
}
/* ===============================
   GUEST MODE BADGE
================================ */
/* ===============================
   MOBILE GUEST MODE CARD
================================ */
.sidebar-user-info.guest {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1rem 1.25rem;
  margin: 1rem 1.25rem;
  border-radius: 14px;
  background: linear-gradient(
    135deg,
    rgba(59, 130, 246, 0.12),
    rgba(139, 92, 246, 0.10)
  );
  border: 1px solid rgba(59, 130, 246, 0.25);
}

.sidebar-user-info.guest .user-avatar-large {
  background: linear-gradient(135deg, #6366f1, #3b82f6);
}

.sidebar-user-info.guest .user-name {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
}

.sidebar-user-info.guest .user-email {
  font-size: 0.8rem;
  font-weight: 600;
  color: #475569;
}
/* ===============================
   SIDEBAR AUTH ACTIONS (BOTTOM)
================================ */
.sidebar-actions {
  margin-top: auto; /* 👈 pushes to bottom */
  padding: 1.25rem;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  background: #ffffff;
}
/* Guest auth buttons */
.sidebar-auth-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Login */
.sidebar-btn.ghost {
  border: 2px solid #3b82f6;
  color: #3b82f6;
  font-weight: 700;
  background: transparent;
}

.sidebar-btn.ghost:hover {
  background: rgba(59, 130, 246, 0.08);
}

/* Signup */
.sidebar-btn.primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  font-weight: 700;
}

.sidebar-btn.primary:hover {
  transform: translateY(-2px);
}
.sidebar-links {
  padding-bottom: 1.5rem;
}

/* Name + badge wrapper */
.user-name-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1.1;
}

/* Username text */
.user-name {
  font-weight: 600;
  font-size: 0.9rem;
  color: #1e293b;
}
/* Dropdown positioning fix */
.user-dropdown {
  margin-top: 0.75rem;
  right: 0;
  min-width: 260px;
  z-index: 999999;
}
/* Guest dropdown CTA */
.dropdown-item.guest-cta {
  font-weight: 600;
  color: #1e293b;
}

/* Primary action */
.dropdown-item.guest-primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  margin: 0.5rem;
  border-radius: 10px;
}

.dropdown-item.guest-primary:hover {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
}

/* Secondary action */
.dropdown-item.guest-secondary {
  margin: 0 0.5rem 0.5rem;
}
/* ===============================
   MOBILE GUEST BADGE
================================ */
.sidebar-user-info.guest {
  border: 1px solid rgba(245, 158, 11, 0.25);
  background: linear-gradient(
    135deg,
    rgba(245, 158, 11, 0.12),
    rgba(217, 119, 6, 0.08)
  );
}

.sidebar-user-info.guest .user-name {
  font-weight: 800;
  color: #92400e;
}

.sidebar-user-info.guest .user-email {
  font-size: 0.75rem;
  font-weight: 600;
  color: #b45309;
}
@keyframes guestPulse {
  0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
  70% { box-shadow: 0 0 0 8px rgba(245, 158, 11, 0); }
  100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
}

.guest-badge {
  animation: guestPulse 2.5s infinite;
}
.user-button.guest {
  border: 1px dashed #f59e0b;
  background: rgba(245, 158, 11, 0.1);
}

.sidebar-user-info.guest {
  border: 1px solid rgba(245, 158, 11, 0.4);
  background: linear-gradient(
    135deg,
    rgba(245, 158, 11, 0.15),
    rgba(217, 119, 6, 0.1)
  );
}

.sidebar-logout {
  width: 100%;
  padding: 0.8rem;
  border-radius: 10px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  font-weight: 700;
}


</style>