<!-- src/views/Login.vue -->
<template>
  <div class="auth-page">
    <Navbar />

    <div class="auth-wrapper">
   <!-- Left Side - Branding -->
<div class="auth-branding">
  <div class="branding-content">
    <div class="brand-badge">
      <Shield :size="16" />
      <span>Secure Login</span>
    </div>

    <h2 class="branding-title">
      Welcome back to<br>
      <span class="gradient-text">CalculatorPro</span>
    </h2>

    <p class="branding-description">
      Sign in to unlock premium features including unlimited calculations, 
      smart notes, and complete history management.
    </p>

    <div class="feature-list">
      <div class="feature-item">
        <div class="feature-icon">
          <FileText :size="18" />
        </div>
        <div class="feature-text">
          <strong>Unlimited Smart Notes</strong>
          <span>Add context to all your calculations with notes</span>
        </div>
      </div>

      <div class="feature-item">
        <div class="feature-icon">
          <TrendingUp :size="18" />
        </div>
        <div class="feature-text">
          <strong>Weekly Analytics</strong>
          <span>Track your calculation patterns and productivity</span>
        </div>
      </div>

      <div class="feature-item">
        <div class="feature-icon">
          <History :size="18" />
        </div>
        <div class="feature-text">
          <strong>Complete History Control</strong>
          <span>Delete individual items or clear entire history anytime</span>
        </div>
      </div>

      <div class="feature-item">
        <div class="feature-icon">
          <Database :size="18" />
        </div>
        <div class="feature-text">
          <strong>Secure Cloud Storage</strong>
          <span>Your data is permanently saved and accessible anywhere</span>
        </div>
      </div>
    </div>
  </div>
</div>


      <!-- Right Side - Login Form -->
      <div class="auth-form-section">
        <div class="auth-container">
          <div class="auth-card">
            <div class="card-header">
              <div class="header-icon">
                <LogIn :size="28" />
              </div>
              <h1>Sign in to your account</h1>
              <p class="header-subtitle">Enter your credentials to continue</p>
            </div>

            <form @submit.prevent="handleLogin" class="auth-form">
              <div class="form-group">
                <label for="username">
                  <User :size="16" />
                  <span>Username</span>
                </label>
                <div class="input-wrapper">
                  <input
                    id="username"
                    v-model="username"
                    type="text"
                    placeholder="Enter your username"
                    autocomplete="username"
                    required
                    :class="{ 'input-error': errors.username }"
                  />
                </div>
                <span v-if="errors.username" class="error-text">
                  <AlertCircle :size="14" />
                  {{ errors.username }}
                </span>
              </div>

              <div class="form-group">
                <label for="password">
                  <Lock :size="16" />
                  <span>Password</span>
                </label>
                <div class="input-wrapper password-wrapper">
                  <input
                    id="password"
                    v-model="password"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Enter your password"
                    autocomplete="current-password"
                    required
                    :class="{ 'input-error': errors.password }"
                  />
                  <button
                    type="button"
                    class="toggle-password"
                    @click="showPassword = !showPassword"
                    tabindex="-1"
                    :aria-label="showPassword ? 'Hide password' : 'Show password'"
                  >
                    <Eye v-if="showPassword" :size="18" />
                    <EyeOff v-else :size="18" />
                  </button>
                </div>
                <span v-if="errors.password" class="error-text">
                  <AlertCircle :size="14" />
                  {{ errors.password }}
                </span>
              </div>

              <div class="form-footer">
                <router-link to="/forgot-password" class="forgot-link">
                  Forgot password?
                </router-link>
              </div>

              <button
                type="submit"
                class="submit-btn"
                :disabled="loading"
                :class="{ 'loading': loading }"
              >
                <span v-if="loading" class="btn-content">
                  <span class="spinner"></span>
                  <span>Signing in...</span>
                </span>
                <span v-else class="btn-content">
                  <span>Sign In</span>
                  <ArrowRight :size="18" />
                </span>
              </button>
            </form>

            <div class="divider">
              <span>or</span>
            </div>

            <button class="guest-btn" @click="loginAsGuest">
              Continue as Guest
            </button>

            <div class="footer-links">
              <p>
                Don't have an account?
                <router-link to="/register" class="signup-link">
                  Create&nbsp;one&nbsp;now
                  <ArrowRight :size="14" />
                </router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Message Modal (Success / Error) -->
    <Modal
      v-if="showModal"
      :text="modalMessage"
      :type="modalType"
      @close="showModal = false"
    />

    <!-- Full-screen Loading Overlay -->
    <div v-if="isFullLoading" class="full-loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <p class="loading-text">Authenticating securely...</p>
      </div>
    </div>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script>
import {
  Eye,
  EyeOff,
  LogIn,
  User,
  Lock,
  ArrowRight,
  Shield,
  AlertCircle,
  FileText,
  TrendingUp,
  History,
  Database
} from 'lucide-vue-next'

import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import api from '@/services/api'
import Modal from '@/components/Modal.vue'

export default {
  name: 'Login',

  components: {
    Navbar,
    Footer,
    Modal,
    Eye,
    EyeOff,
    LogIn,
    User,
    Lock,
    ArrowRight,
    Shield,
    AlertCircle,
    FileText,
    TrendingUp,
    History,
    Database
  },

  data() {
    return {
      username: '',
      password: '',
      showPassword: false,
      loading: false,
      isFullLoading: false,
      showModal: false,
      modalMessage: '',
      modalType: 'error',
      errors: {}
    }
  },

  methods: {
    async handleLogin() {
      this.loading = true
      this.isFullLoading = true
      this.errors = {}

      try {
        await api.post(
          '/auth/login/',
          {
            username: this.username,
            password: this.password
          },
          { withCredentials: true }
        )

        // clear guest flag
        localStorage.removeItem('is_guest')

        // success UI
        this.modalMessage = 'Login successful!'
        this.modalType = 'success'
        this.showModal = true

    
        const redirectTo = this.$route.query.redirect || '/dashboard'

        setTimeout(() => {
          this.$router.push(redirectTo)
        }, 600)

      } catch (err) {
        this.modalMessage =
          err.response?.data?.error || 'Invalid credentials'
        this.modalType = 'error'
        this.showModal = true
      } finally {
        this.loading = false
        this.isFullLoading = false
      }
    },

    loginAsGuest() {
      // Guest mode (session-based)
      localStorage.setItem('is_guest', 'true')

      // Ensure no auth leftovers
      localStorage.removeItem('user')

      this.$router.push('/dashboard')
    }
  }
}
</script>


<style scoped>
/* ================= GLOBAL ================= */
.auth-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%);
  position: relative;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.auth-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: calc(100vh - 70px);
  flex: 1;
}

/* Left Side - Branding */
.auth-branding {
  background: #f8f9fa;
  padding: 0 5vw;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  position: relative;
  overflow: hidden;
  min-height: 100vh;
}

.branding-content {
  max-width: 520px;
  position: relative;
  z-index: 1;
  padding: 80px 60px 0;
  margin: 0 auto;
  width: 100%;
}

.brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--primary);
  border-radius: 6px;
  color: white;
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.branding-title {
  font-size: 3rem;
  font-weight: 900;
  color: #1e293b;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
}

.gradient-text {
  display: block;
  color: #1e293b;
}

.branding-description {
  font-size: 1.15rem;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 3rem;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.feature-icon {
  width: 40px;
  height: 40px;
  background: #1e293b;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.feature-text {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  color: #1e293b;
}

.feature-text strong {
  font-size: 1.05rem;
  font-weight: 600;
}

.feature-text span {
  font-size: 0.95rem;
  color: #64748b;
}

/* Right Side - Form */
.auth-form-section {
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 60px;
}

.auth-container {
  width: 100%;
  max-width: 480px;
}

.auth-card {
  background: white;
  border-radius: 24px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  padding: 3rem 2.5rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.card-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.header-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 1.5rem;
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.25);
}

.card-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.header-subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
}

/* Form Styles */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.95rem;
}

label svg {
  color: var(--text-muted);
}

.input-wrapper {
  position: relative;
}

input {
  width: 100%;
  padding: 1rem 1.25rem;
  background: #f8fafc;
  border: 2px solid transparent;
  border-radius: 12px;
  font-size: 1rem;
  color: var(--text-primary);
  transition: all 0.3s ease;
}

input:focus {
  outline: none;
  background: white;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

input::placeholder {
  color: var(--text-muted);
}

.input-error {
  border-color: var(--danger) !important;
  background: rgba(239, 68, 68, 0.02) !important;
}

.error-text {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: var(--danger);
  font-size: 0.85rem;
  font-weight: 500;
}

.password-wrapper {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.5rem;
  line-height: 1;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.toggle-password:hover {
  background: rgba(0, 0, 0, 0.04);
  color: var(--text-primary);
}

.form-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: -0.5rem;
}

.forgot-link {
  color: var(--primary);
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s ease;
}

.forgot-link:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}

.submit-btn {
  width: 100%;
  padding: 1.15rem;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  margin-top: 0.5rem;
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
}

.spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.divider {
  position: relative;
  text-align: center;
  margin: 2rem 0 1.5rem;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: rgba(0, 0, 0, 0.1);
}

.divider span {
  position: relative;
  background: white;
  padding: 0 1rem;
  color: var(--text-muted);
  font-size: 0.9rem;
  font-weight: 500;
}

.footer-links {
  text-align: center;
}

.footer-links p {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.signup-link {
  color: var(--primary);
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.signup-link:hover {
  color: var(--primary-dark);
  gap: 0.5rem;
}

/* Guest Button */
.guest-btn {
  width: 100%;
  padding: 1.05rem;
  background: white;
  border: 2px dashed rgba(59, 130, 246, 0.4);
  border-radius: 12px;
  color: var(--primary);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  margin-bottom: 1.5rem;
}

.guest-btn:hover {
  background: rgba(59, 130, 246, 0.05);
  border-color: var(--primary);
  transform: translateY(-2px);
}

/* Full Screen Loading Overlay */
.full-loading-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.92);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 4000;
}

.loading-content {
  text-align: center;
  color: white;
}

.loading-spinner {
  width: 64px;
  height: 64px;
  border: 6px solid rgba(255, 255, 255, 0.2);
  border-top: 6px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

.loading-text {
  font-size: 1.3rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* Responsive */
@media (max-width: 1024px) {
  .auth-wrapper {
    grid-template-columns: 1fr;
  }
  .auth-branding {
    display: none;
  }
  .auth-form-section {
    padding: 60px 30px;
  }
}

@media (max-width: 480px) {
  .auth-form-section {
    padding: 40px 20px;
  }
  .auth-card {
    padding: 2rem 1.5rem;
  }
  .card-header h1 {
    font-size: 1.5rem;
  }
  .header-icon {
    width: 50px;
    height: 50px;
  }
}
</style>