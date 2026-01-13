<!-- src/views/Welcome.vue -->
<template>
  <div class="welcome-page">
    <Navbar />
    
    <!-- ================= HERO SECTION ================= -->
    <!-- Main landing section with dynamic CTAs based on user auth state -->
    <section class="hero-section">
      <div class="hero-container">
        <div class="hero-content">
          <!-- Top badge showing tech stack -->
          <div class="badge-wrapper">
            <div class="badge">
              <Sparkles :size="16" class="badge-icon" />
              <span>Django • Vue.js • STGI Assessment • Full-Stack Calculator • 2026</span>
            </div>
          </div>

          <!-- Hero title with gradient effect -->
          <h1 class="hero-title">
            <span class="title-line">Professional. Powerful. Precise.</span>
            <span class="title-gradient">
              CalculatorPro<span class="dot">.</span>
            </span>
          </h1>

          <!-- Description of main features -->
          <p class="hero-description">
            A feature-rich Django calculator with smart notes, weekly analytics, 
            dual access modes, and intelligent history management. Experience the 
            difference between guest and premium access.
          </p>

          <!-- Dynamic action buttons based on authentication state -->
          <div class="hero-actions">
            <!-- Case 1: User is already logged in with account -->
            <template v-if="isAuthenticated">
              <button 
                class="btn btn-primary" 
                onclick="window.location.href='/dashboard'"
              >
                <span>Go to Dashboard</span>
                <ArrowRight :size="20" />
              </button>
            </template>

            <!-- Case 2: User is in guest mode (temporary session) -->
            <template v-else-if="isGuest">
              <button 
                class="btn btn-primary" 
                onclick="window.location.href='/dashboard'"
              >
                <span>Resume as Guest</span>
                <ArrowRight :size="20" />
              </button>
              <!-- Clear guest mode and redirect to register -->
              <button 
                class="btn btn-secondary" 
                onclick="localStorage.removeItem('is_guest'); localStorage.removeItem('user'); sessionStorage.clear(); window.location.href='/register';"
              >
                <span>Register to Save History</span>
              </button>
            </template>

            <!-- Case 3: New visitor - show guest and login options -->
            <template v-else>
              <!-- Primary CTA: Guest mode for quick access -->
              <button 
                class="btn btn-primary" 
                onclick="localStorage.setItem('is_guest', 'true'); localStorage.removeItem('user'); window.location.href='/dashboard';"
              >
                <span>Continue as Guest</span>
                <ArrowRight :size="20" />
              </button>
              <!-- Secondary CTA: Full registration -->
              <button 
                class="btn btn-secondary" 
                onclick="window.location.href='/register'"
              >
                <span>Login for Premium</span>
              </button>
            </template>
          </div>

          <!-- Trust indicators showing key features -->
          <div class="trust-indicators">
            <div class="trust-item">
              <CheckCircle2 :size="16" />
              <span>Guest & Premium Modes</span>
            </div>
            <div class="trust-item">
              <CheckCircle2 :size="16" />
              <span>Smart Notes System</span>
            </div>
            <div class="trust-item">
              <CheckCircle2 :size="16" />
              <span>Weekly Analytics</span>
            </div>
          </div>
        </div>

        <!-- HERO VISUAL - Interactive calculator preview -->
        <div class="hero-visual">
          <!-- Main preview card showing live calculation -->
          <div class="visual-card">
            <div class="card-header">
              <div class="card-dots">
                <!-- macOS-style window dots -->
                <span></span><span></span><span></span>
              </div>
              <div class="card-title">Live Calculation</div>
            </div>
            <div class="card-content">
              <!-- Sample calculation display -->
              <div class="calc-display">
                <div class="calc-operation">125 × 4</div>
                <div class="calc-result">500</div>
                <div class="calc-note">
                  <FileText :size="14" style="display: inline; margin-right: 6px;" />
                  Monthly revenue calculation
                </div>
              </div>
              <!-- Recent calculations history preview -->
              <div class="calc-history">
                <div class="history-item">
                  <span>10 + 5</span>
                  <span>15</span>
                </div>
                <div class="history-item">
                  <span>20 ÷ 4</span>
                  <span>5</span>
                </div>
              </div>
            </div>
          </div>

          <!-- FLOATING CARDS - Animated feature highlights -->
          <div class="float-card float-1">
            <TrendingUp :size="16" />
            <span>Weekly Stats</span>
          </div>
          <div class="float-card float-2">
            <FileText :size="16" />
            <span>Smart Notes</span>
          </div>
          <div class="float-card float-3">
            <Shield :size="16" />
            <span>Secure Sessions</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ================= ACCESS COMPARISON SECTION ================= -->
    <!-- Side-by-side comparison of Guest vs Premium features -->
    <section class="comparison-section" id="access">
      <div class="section-container">
        <div class="section-header">
          <div class="section-badge">Access Modes</div>
          <h2 class="section-title">
            Guest vs Premium Access
          </h2>
          <p class="section-description">
            Start free as a guest or unlock unlimited power with premium access.
          </p>
        </div>
        
        <div class="comparison-grid">
          <!-- GUEST MODE CARD -->
          <div class="access-card guest-card">
            <div class="access-header">
              <div class="access-icon guest-icon">
                <User :size="28" />
              </div>
              <h3 class="access-title">Guest Mode</h3>
              <p class="access-subtitle">Try without registration</p>
            </div>
            <!-- Guest mode feature list with limitations -->
            <div class="access-features">
              <div class="feature-item enabled">
                <CheckCircle2 :size="18" />
                <span>Basic calculator operations</span>
              </div>
              <div class="feature-item enabled">
                <CheckCircle2 :size="18" />
                <span>View last 10 calculations</span>
              </div>
              <div class="feature-item enabled">
                <CheckCircle2 :size="18" />
                <span>Add notes to 2 calculations</span>
              </div>
              <div class="feature-item enabled">
                <CheckCircle2 :size="18" />
                <span>Weekly analytics dashboard</span>
              </div>
              <!-- Disabled features shown with X icon -->
              <div class="feature-item disabled">
                <XCircle :size="18" />
                <span>Cannot clear full history</span>
              </div>
              <div class="feature-item disabled">
                <XCircle :size="18" />
                <span>Cannot delete individual items</span>
              </div>
              <div class="feature-item disabled">
                <XCircle :size="18" />
                <span>Session data not permanent</span>
              </div>
            </div>
            <button class="btn-access" @click="continueAsGuest">
              Try as Guest
            </button>
          </div>

          <!-- PREMIUM MODE CARD -->
          <div class="access-card premium-card">
            <div class="premium-badge">Recommended</div>
            <div class="access-header">
              <div class="access-icon premium-icon">
                <Crown :size="28" />
              </div>
              <h3 class="access-title">Premium Access</h3>
              <p class="access-subtitle">Full power unleashed</p>
            </div>
            <!-- All features enabled for premium users -->
            <div class="access-features">
              <div class="feature-item enabled">
                <CheckCircle2 :size="18" />
                <span>Unlimited calculations</span>
              </div>
              <div class="feature-item enabled">
                <CheckCircle2 :size="18" />
                <span>Complete calculation history</span>
              </div>
              <div class="feature-item enabled">
                <CheckCircle2 :size="18" />
                <span>Unlimited notes on all calculations</span>
              </div>
              <div class="feature-item enabled">
                <CheckCircle2 :size="18" />
                <span>Weekly calculation analytics</span>
              </div>
              <div class="feature-item enabled">
                <CheckCircle2 :size="18" />
                <span>Delete individual history items</span>
              </div>
              <div class="feature-item enabled">
                <CheckCircle2 :size="18" />
                <span>Clear entire history anytime</span>
              </div>
              <div class="feature-item enabled">
                <CheckCircle2 :size="18" />
                <span>Secure & persistent cloud storage</span>
              </div>
            </div>
            <button class="btn-access premium-btn" @click="goRegister">
              Get Premium Free
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- ================= FEATURES SECTION ================= -->
    <!-- Detailed feature cards explaining core functionality -->
    <section class="features-section" id="features">
      <div class="section-container">
        <div class="section-header">
          <div class="section-badge">Features</div>
          <h2 class="section-title">
            Everything you need for<br />professional calculations
          </h2>
          <p class="section-description">
            Built with Django REST Framework & Vue.js for maximum performance.
          </p>
        </div>
        <div class="features-grid">
          <!-- Feature 1: Calculator -->
          <div class="feature-card">
            <div class="feature-icon" style="background:linear-gradient(135deg,#3b82f6,#2563eb)">
              <Calculator :size="24" />
            </div>
            <h3 class="feature-title">Advanced Calculator</h3>
            <p class="feature-description">
              Four basic operations with real-time validation, error handling, and instant results. Premium users get unlimited calculations.
            </p>
          </div>
          
          <!-- Feature 2: History Tracking -->
          <div class="feature-card">
            <div class="feature-icon" style="background:linear-gradient(135deg,#8b5cf6,#7c3aed)">
              <History :size="24" />
            </div>
            <h3 class="feature-title">Smart History Tracking</h3>
            <p class="feature-description">
              Every calculation stored with full details, timestamps, and notes. Guest mode: 10 items. Premium: unlimited with full control.
            </p>
          </div>
          
          <!-- Feature 3: Notes -->
          <div class="feature-card">
            <div class="feature-icon" style="background:linear-gradient(135deg,#10b981,#059669)">
              <FileText :size="24" />
            </div>
            <h3 class="feature-title">Calculation Notes</h3>
            <p class="feature-description">
              Add context to your calculations with smart notes. Guest users can add notes to 2 calculations. Premium users: unlimited notes.
            </p>
          </div>
          
          <!-- Feature 4: Analytics -->
          <div class="feature-card">
            <div class="feature-icon" style="background:linear-gradient(135deg,#f59e0b,#d97706)">
              <TrendingUp :size="24" />
            </div>
            <h3 class="feature-title">Weekly Analytics</h3>
            <p class="feature-description">
              Track your calculation patterns with weekly statistics. Available for both guest and premium users to monitor productivity.
            </p>
          </div>
          
          <!-- Feature 5: History Management -->
          <div class="feature-card">
            <div class="feature-icon" style="background:linear-gradient(135deg,#ec4899,#db2777)">
              <Trash2 :size="24" />
            </div>
            <h3 class="feature-title">History Management</h3>
            <p class="feature-description">
              Premium users can delete individual history items or clear entire history. Guest users have read-only access to their 10 recent items.
            </p>
          </div>
          
          <!-- Feature 6: Security -->
          <div class="feature-card">
            <div class="feature-icon" style="background:linear-gradient(135deg,#06b6d4,#0891b2)">
              <Shield :size="24" />
            </div>
            <h3 class="feature-title">Secure Authentication</h3>
            <p class="feature-description">
              Django-powered authentication with session management. Guest sessions for quick access. User accounts for permanent data storage.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ================= STATS SECTION ================= -->
    <!-- Quick stats showing key metrics -->
    <section class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-number">4</div>
          <div class="stat-label">Math Operations</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">2</div>
          <div class="stat-label">Access Modes</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">∞</div>
          <div class="stat-label">Premium Calculations</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">REST</div>
          <div class="stat-label">API Architecture</div>
        </div>
      </div>
    </section>

   <!-- ================= CALL TO ACTION SECTION ================= -->
<section class="cta-section">
  <div class="cta-container">
    <div class="cta-icon">
      <Zap :size="48" />
    </div>
    <h2 class="cta-title">Ready to supercharge your calculations?</h2>
    
    <p class="cta-description">
      <template v-if="isAuthenticated">
        You're all set! Head to your dashboard to continue.
      </template>
      <template v-else-if="isGuest">
     You're in Guest mode — upgrade to Premium for unlimited features and permanent storage!
      </template>
      <template v-else>
        Create a free account for unlimited calculations, smart notes, weekly analytics,
        and full history management. No credit card required.
      </template>
    </p>

    <div class="cta-buttons">
      <!-- 1. Already Logged in -->
      <template v-if="isAuthenticated">
        <button 
          class="btn btn-primary-large"
          onclick="window.location.href='/dashboard'"
        >
          Go to Dashboard
          <ArrowRight :size="20" />
        </button>
      </template>

      <!-- 2. Guest Mode -->
      <template v-else-if="isGuest">
        <button 
          class="btn btn-primary-large"
          onclick="window.location.href='/dashboard'"
        >
          Continue in Dashboard
          <ArrowRight :size="20" />
        </button>
        
        <button 
          class="btn btn-secondary-large"
          onclick="localStorage.removeItem('is_guest'); localStorage.removeItem('user'); localStorage.removeItem('username'); sessionStorage.clear(); window.location.href='/register';"
        >
        Upgrade to Premium
        </button>
      </template>

      <!-- 3. New Visitor -->
      <template v-else>
        <button 
          class="btn btn-primary-large"
          onclick="window.location.href='/register'"
        >
          Get Premium Access Free
          <ArrowRight :size="20" />
        </button>
        
        <button 
          class="btn btn-secondary-large"
          onclick="localStorage.setItem('is_guest', 'true'); localStorage.removeItem('user'); window.location.href='/dashboard';"
        >
          Try as Guest
        </button>
      </template>
    </div>
  </div>
</section>

    <!-- ================= FOOTER ================= -->
    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import api from '@/services/api'

// Import all necessary icons from lucide-vue-next
import {
  ArrowRight,
  CheckCircle2,
  XCircle,
  Calculator,
  History,
  Users,
  FileText,
  Zap,
  Shield,
  User,
  Crown,
  TrendingUp,
  Trash2,
  Sparkles
} from 'lucide-vue-next'

export default {
  name: 'Welcome',

  components: {
    Navbar,
    Footer,
    ArrowRight,
    CheckCircle2,
    XCircle,
    Calculator,
    History,
    Users,
    FileText,
    Zap,
    Shield,
    User,
    Crown,
    TrendingUp,
    Trash2,
    Sparkles
  },

  data() {
    return {
      // Store username from localStorage for instant UI state
      // This prevents UI flicker before API call completes
      username: localStorage.getItem('username'),
      authChecked: false // Flag to track if auth verification is complete
    }
  },

  computed: {
    // Check if user has a valid authenticated session
    isAuthenticated() {
      return !!this.username
    },

    // Check if user is in guest mode (no account but using app)
    isGuest() {
      return !this.isAuthenticated && localStorage.getItem('is_guest') === 'true'
    }
  },

  mounted() {
    // Verify authentication status with backend on component load
    this.syncAuth()
  },

  methods: {
    // Sync authentication state with Django backend
    async syncAuth() {
      try {
        // Call Django /auth/me/ endpoint to check session validity
        const res = await api.get('/auth/me/', { withCredentials: true })

        if (res.data.is_authenticated) {
          // User has valid session - update local state
          this.username = res.data.username
          localStorage.setItem('username', res.data.username)
          localStorage.removeItem('is_guest') // Clear guest flag if logged in
        } else {
          // No valid session - clear auth data
          this.clearAuth()
        }
      } catch {
        // API call failed - assume not authenticated
        this.clearAuth()
      } finally {
        this.authChecked = true
      }
    },

    // Clear all authentication data from localStorage
    clearAuth() {
      this.username = null
      localStorage.removeItem('username')
    },

    // Navigate to dashboard (for authenticated users)
    goDashboard() {
      this.$router.push('/dashboard')
    },

    // Navigate to login page
    goLogin() {
      this.$router.push('/login')
    },

    // Navigate to registration page
    goRegister() {
      this.$router.push('/register')
    },

    // Set guest mode flag and redirect to dashboard
    continueAsGuest() {
      localStorage.setItem('is_guest', 'true')
      this.$router.push('/dashboard')
    }
  }
}
</script>

<style scoped>
/* ================= GLOBAL STYLES ================= */
.welcome-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%);
  overflow-x: hidden;
}

/* ================= HERO SECTION ================= */
.hero-section {
  padding: 70px 5vw 100px;
  position: relative;
  min-height: calc(100vh - 70px);
  display: flex;
  align-items: center;
}

/* Subtle gradient background effect behind hero */
.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 1200px;
  height: 600px;
  background: radial-gradient(circle at 50% 0%, rgba(59, 130, 246, 0.08) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
}

/* Two-column layout for hero content */
.hero-container {
  max-width: 1320px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.badge-wrapper {
  display: flex;
  justify-content: flex-start;
}

/* Tech stack badge with subtle animation */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 50px;
  background: rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.2);
  color: var(--primary);
  font-weight: 600;
  font-size: 0.9rem;
  animation: badge-float 3s ease-in-out infinite;
}

.badge-icon {
  color: var(--primary);
}

/* Smooth floating animation for badge */
@keyframes badge-float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-4px); }
}

.hero-title {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Responsive font sizing using clamp */
.title-line {
  font-size: clamp(2rem, 4vw, 3.2rem);
  font-weight: 700;
  line-height: 1.2;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

/* Gradient text effect for main branding */
.title-gradient {
  font-size: clamp(3rem, 6vw, 5rem);
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.03em;
}

.dot {
  color: var(--accent);
  -webkit-text-fill-color: var(--accent);
}

.hero-description {
  font-size: 1.2rem;
  line-height: 1.7;
  color: var(--text-secondary);
  max-width: 600px;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

/* Base button styles with smooth transitions */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  border: none;
  text-decoration: none;
}

/* Primary button with gradient and shadow */
.btn-primary {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.25);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.35);
}

/* Secondary button with border and subtle background */
.btn-secondary {
  background: rgba(255, 255, 255, 0.9);
  color: var(--text-primary);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.btn-secondary:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

/* Larger CTA buttons for emphasis */
.btn-primary-large {
  display: inline-flex;
  align-items: center;
  gap: 0.8rem;
  padding: 1.3rem 2.8rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1.15rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  border: none;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

.btn-primary-large:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4);
}

.btn-secondary-large {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 1.3rem 2.8rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1.15rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: white;
  color: var(--text-primary);
}

.btn-secondary-large:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

/* Trust indicators showing key features */
.trust-indicators {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.trust-item svg {
  color: var(--success);
}

/* ================= HERO VISUAL (Right Side) ================= */
.hero-visual {
  position: relative;
  height: 500px;
}

/* Main calculator preview card with glassmorphism effect */
.visual-card {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  max-width: 420px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.12);
  overflow: hidden;
  animation: float 6s ease-in-out infinite;
}

/* Gentle floating animation for preview card */
@keyframes float {
  0%, 100% { transform: translate(-50%, -50%) translateY(0px); }
  50% { transform: translate(-50%, -50%) translateY(-20px); }
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* macOS-style window control dots */
.card-dots {
  display: flex;
  gap: 6px;
}

.card-dots span {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.card-dots span:nth-child(2) {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.card-dots span:nth-child(3) {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.card-title {
  font-weight: 600;
  color: var(--text-primary);
}

.card-content {
  padding: 2rem 1.5rem;
}

/* Calculator display area */
.calc-display {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.calc-operation {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 0.8rem;
}

.calc-result {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 0.8rem;
}

/* Note display with left border accent */
.calc-note {
  font-size: 0.9rem;
  color: var(--accent);
  font-style: italic;
  padding: 0.6rem 1rem;
  background: rgba(139, 92, 246, 0.08);
  border-radius: 8px;
  border-left: 3px solid var(--accent);
  display: flex;
  align-items: center;
}

.calc-history {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1rem;
  background: rgba(59, 130, 246, 0.04);
  border-radius: 8px;
  font-size: 0.95rem;
}

.history-item span:first-child {
  color: var(--text-secondary);
}

.history-item span:last-child {
  font-weight: 600;
  color: var(--text-primary);
}

/* ================= FLOATING FEATURE CARDS ================= */
/* Small animated cards showcasing features */
.float-card {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.8rem 1.2rem;
  background: white;
  border-radius: 50px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
}

.float-card svg {
  color: var(--primary);
}

/* Position and animate each floating card differently */
.float-1 {
  top: 10%;
  right: -10%;
  animation: float-1 4s ease-in-out infinite;
}

.float-2 {
  bottom: 30%;
  right: -15%;
  animation: float-2 5s ease-in-out infinite 0.5s;
}

.float-3 {
  top: 60%;
  left: -12%;
  animation: float-3 4.5s ease-in-out infinite 1s;
}

/* Individual floating animations with different timing */
@keyframes float-1 {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-15px); }
}

@keyframes float-2 {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

@keyframes float-3 {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-12px); }
}

/* ================= ACCESS COMPARISON SECTION ================= */
.comparison-section {
  padding: 100px 5vw;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
}

.section-container {
  max-width: 1320px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 5rem;
}

/* Section badge for category identification */
.section-badge {
  display: inline-block;
  padding: 8px 18px;
  border-radius: 50px;
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.2);
  color: var(--accent);
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: clamp(2.5rem, 5vw, 3.5rem);
  font-weight: 800;
  line-height: 1.2;
  color: var(--text-primary);
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.section-description {
  font-size: 1.25rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
}

/* Responsive grid for comparison cards */
.comparison-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 2.5rem;
  max-width: 1000px;
  margin: 0 auto;
}

/* Base card styling for access modes */
.access-card {
  position: relative;
  padding: 3rem 2.5rem;
  background: white;
  border-radius: 24px;
  border: 2px solid rgba(0, 0, 0, 0.06);
  transition: all 0.4s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.guest-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);
}

/* Premium card with highlighted border and shadow */
.premium-card {
  border: 2px solid var(--primary);
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.15);
}

.premium-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 30px 70px rgba(59, 130, 246, 0.25);
}

/* "Recommended" badge for premium card */
.premium-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  padding: 6px 20px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.access-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

/* Icon containers for each access type */
.access-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: white;
}

.guest-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.premium-icon {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
}

.access-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.access-subtitle {
  font-size: 1rem;
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

/* Feature list inside access cards */
.access-features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2.5rem;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 0.8rem;
  font-size: 0.95rem;
}

/* Enabled features with green check */
.feature-item.enabled {
  color: var(--text-primary);
}

.feature-item.enabled svg {
  color: var(--success);
  flex-shrink: 0;
  margin-top: 2px;
}

/* Disabled features with gray X */
.feature-item.disabled {
  color: var(--text-tertiary);
}

.feature-item.disabled svg {
  color: #cbd5e1;
}

/* CTA button for access cards */
.btn-access {
  width: 100%;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  border: 2px solid rgba(0, 0, 0, 0.1);
  background: white;
  color: var(--text-primary);
}

.btn-access:hover {
  background: var(--text-primary);
  color: white;
  transform: translateY(-2px);
}

/* Premium button with gradient */
.premium-btn {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  border: none;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.25);
}

.premium-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.35);
}

/* ================= FEATURES SECTION ================= */
.features-section {
  padding: 100px 5vw;
  background: white;
}

/* Responsive grid for feature cards */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

/* Individual feature card with hover effect */
.feature-card {
  padding: 2.5rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.9) 100%);
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  transition: all 0.4s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);
  border-color: rgba(59, 130, 246, 0.2);
}

/* Icon container for each feature */
.feature-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  color: white;
}

.feature-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.feature-description {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--text-secondary);
}

/* ================= STATS SECTION ================= */
/* Stats section with primary gradient background */
.stats-section {
  padding: 80px 5vw;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
}

.stats-grid {
  max-width: 1320px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 3rem;
}

.stat-card {
  text-align: center;
}

/* Large stat numbers */
.stat-number {
  font-size: 3.5rem;
  font-weight: 900;
  color: white;
  margin-bottom: 0.5rem;
  line-height: 1;
}

.stat-label {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.85);
  font-weight: 500;
}

/* ================= CALL TO ACTION SECTION ================= */
.cta-section {
  padding: 100px 5vw;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

/* Centered CTA container with subtle background */
.cta-container {
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
  padding: 5rem 3rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 30px;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

/* Animated icon for CTA */
.cta-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 2rem;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  animation: pulse 2s ease-in-out infinite;
}

/* Pulse animation for CTA icon */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.cta-title {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.cta-description {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 2.5rem;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.7;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

/* ================= RESPONSIVE DESIGN ================= */
/* Tablet and smaller screens */
@media (max-width: 1024px) {
  /* Stack hero into single column */
  .hero-container {
    grid-template-columns: 1fr;
    gap: 60px;
  }
  
  .hero-visual {
    height: 400px;
  }
  
  /* Hide floating cards on smaller screens for cleaner layout */
  .float-card {
    display: none;
  }
  
  /* Single column for comparison cards */
  .comparison-grid {
    grid-template-columns: 1fr;
    max-width: 500px;
  }
}

/* Mobile devices */
@media (max-width: 768px) {
  .hero-section {
    padding: 80px 5vw 60px;
  }
  
  .hero-content {
    gap: 1.5rem;
  }
  
  /* Stack action buttons vertically */
  .hero-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
  
  /* Stack trust indicators vertically */
  .trust-indicators {
    flex-direction: column;
    gap: 0.8rem;
  }
  
  /* Single column for features */
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  /* 2-column stats grid */
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
  }
  
  .stat-number {
    font-size: 2.5rem;
  }
  
  .cta-container {
    padding: 3rem 2rem;
  }
  
  /* Stack CTA buttons vertically */
  .cta-buttons {
    flex-direction: column;
  }
  
  .btn-primary-large,
  .btn-secondary-large {
    width: 100%;
    justify-content: center;
  }
}

/* Small mobile devices */
@media (max-width: 480px) {
  .visual-card {
    max-width: 100%;
  }
  
  .calc-result {
    font-size: 2rem;
  }
  
  /* Single column stats */
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .comparison-grid {
    grid-template-columns: 1fr;
  }
}
</style>