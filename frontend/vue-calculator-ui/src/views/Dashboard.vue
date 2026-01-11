<!-- src/views/Dashboard.vue -->
<template>
  <div class="dashboard-wrapper">
    <!-- Top Navbar -->
    <Navbar />
    <main class="dashboard-main">
      <div class="dashboard-container">
        <!-- ================= HEADER ================= -->
        <header class="dashboard-header">
          <div class="header-content">
            <div class="header-text">
              <div class="greeting-badge">
                <Sparkles :size="16" />
                <span>{{ greetingTime }}</span>
              </div>
              <h1 class="header-title">
                Welcome back,
                <span class="user-highlight">{{ username }}</span>
              </h1>
              <p class="header-subtitle">
                Your professional calculation workspace is ready
              </p>
            </div>
            <div class="header-stats">
              <div class="stat-card">
                <div class="stat-icon">
                  <CalcIcon :size="20" />
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ totalCalculations }}</div>
                  <div class="stat-label">Total Calculations</div>
                </div>
              </div>
              <div class="stat-card">
                <div
                  class="stat-icon"
                  style="background: linear-gradient(135deg,#10b981,#059669)"
                >
                  <TrendingUp :size="20" />
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ weekCalculations }}</div>
                  <div class="stat-label">This Week</div>
                </div>
              </div>
            </div>
          </div>
        </header>
        <!-- ================= QUICK ACTIONS ================= -->
        <section class="quick-actions">
          <div class="section-header">
            <Zap :size="20" />
            <h2>Quick Actions</h2>
          </div>
          <div class="actions-grid">
            <button class="action-card" @click="focusCalculator">
              <div class="action-icon">
                <Plus :size="24" />
              </div>
              <div class="action-content">
                <div class="action-title">New Calculation</div>
                <div class="action-subtitle">Start a fresh calculation</div>
              </div>
            </button>
            <button class="action-card" @click="scrollToHistory">
              <div
                class="action-icon"
                style="background: linear-gradient(135deg,#8b5cf6,#7c3aed)"
              >
                <HistoryIcon :size="24" />
              </div>
              <div class="action-content">
                <div class="action-title">View History</div>
                <div class="action-subtitle">Browse past calculations</div>
              </div>
            </button>
          </div>
        </section>
        <!-- ================= MAIN GRID ================= -->
        <section class="content-grid">
          <!-- Calculator -->
          <div class="section-card">
            <div class="card-header">
              <div class="card-header-left">
                <div class="card-icon">
                  <CalcIcon :size="20" />
                </div>
                <h3>Calculator</h3>
              </div>
            </div>
            <div class="card-content">
              <Calculator
                ref="calculatorRef"
                @calculated="onCalculated"
              />
            </div>
          </div>
          <!-- History -->
          <div class="section-card" ref="historySection">
            <div class="card-header">
              <div class="card-header-left">
                <div
                  class="card-icon"
                  style="background: linear-gradient(135deg,#8b5cf6,#7c3aed)"
                >
                  <HistoryIcon :size="20" />
                </div>
                <h3>Recent History</h3>
              </div>
            </div>
            <div class="card-content history-content">
           <History ref="historyRef" :isGuest="isGuest" />
            </div>
          </div>
        </section>
      </div>
    </main>
    <!-- Common Footer Component -->
    <Footer />
  </div>
</template>
<script>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import Calculator from '@/components/Calculator.vue'
import History from '@/components/History.vue'
import api from '@/services/api'
import {
  Calculator as CalcIcon,
  Sparkles,
  TrendingUp,
  Zap,
  Plus,
  History as HistoryIcon
} from 'lucide-vue-next'
export default {
  name: 'Dashboard',
  components: {
    Navbar,
    Footer,
    Calculator,
    History,
    CalcIcon,
    Sparkles,
    TrendingUp,
    Zap,
    Plus,
    HistoryIcon
  },
  data() {
    return {
      username: 'Guest',
      isGuest: true,
      totalCalculations: 0,
      weekCalculations: 0
    }
  },
  computed: {
    greetingTime() {
      const hour = new Date().getHours()
      if (hour < 12) return 'Good Morning'
      if (hour < 18) return 'Good Afternoon'
      return 'Good Evening'
    }
  },
  async mounted() {
    await this.fetchUser()
    await this.refreshStats()
  },
  methods: {
    // Fetch user authentication status
    async fetchUser() {
      try {
        const res = await api.get('/auth/me/', {
          withCredentials: true
        })
        if (res.data.is_authenticated) {
          this.username = res.data.username
          this.isGuest = false
        } else {
          this.username = 'Guest'
          this.isGuest = true
        }
      } catch (err) {
        this.username = 'Guest'
        this.isGuest = true
      }
    },
    // Fetch calculation statistics
    async refreshStats() {
      try {
        const res = await api.get('/history/', {
          withCredentials: true
        })
        const history = res.data || []
        
        this.totalCalculations = history.length
        
        // Count this week's calculations (last 7 days)
        const now = new Date()
        const sevenDaysAgo = new Date(now.getTime() - (7 * 24 * 60 * 60 * 1000))
        
        this.weekCalculations = history.filter(item => {
          if (!item.created_at) return false
          const itemDate = new Date(item.created_at)
          return itemDate >= sevenDaysAgo
        }).length
        
      } catch (err) {
        console.error('Failed to load stats:', err)
        this.totalCalculations = 0
        this.weekCalculations = 0
      }
    },
    // Called when a new calculation is made
    onCalculated() {
      this.totalCalculations++
      this.weekCalculations++
      this.$refs.historyRef?.fetchHistory?.()
      // Refresh stats in background
      this.refreshStats()
    },
    focusCalculator() {
      this.$refs.calculatorRef?.$el
        ?.querySelector('input')
        ?.focus()
    },
    scrollToHistory() {
      this.$refs.historySection?.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      })
    }
  }
}
</script>
<style scoped>
.dashboard-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  display: flex;
  flex-direction: column;
  padding-top: 70px;
}
.dashboard-main {
  flex: 1;
  padding: 40px 0;
}
.dashboard-container {
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 60px;
  width: 100%;
}
/* Header Section */
.dashboard-header {
  margin-bottom: 3rem;
}
.header-content {
  background: white;
  border-radius: 24px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  padding: 3rem 2.5rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}
.greeting-badge {
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
.header-title {
  font-size: 3rem;
  font-weight: 900;
  color: #1e293b;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
}
.user-highlight {
  color: #1e293b;
}
.header-subtitle {
  font-size: 1.15rem;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 3rem;
}
.header-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: #f8fafc;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 16px;
  transition: all 0.3s ease;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}
.stat-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}
.stat-info {
  display: flex;
  flex-direction: column;
}
.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: #1e293b;
  line-height: 1;
  margin-bottom: 0.25rem;
}
.stat-label {
  font-size: 0.95rem;
  color: #64748b;
  font-weight: 500;
}
/* Quick Actions */
.quick-actions {
  margin-bottom: 3rem;
}
.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}
.section-header svg {
  color: #1e293b;
}
.section-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}
.action-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  text-align: left;
}
.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border-color: rgba(59, 130, 246, 0.15);
}
.action-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}
.action-content {
  display: flex;
  flex-direction: column;
}
.action-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.25rem;
}
.action-subtitle {
  font-size: 0.95rem;
  color: #64748b;
}
/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
}
.section-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}
.card-header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.card-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}
.card-header h3 {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}
.card-content {
  padding: 2rem;
}
.history-content {
  max-height: 500px;
  overflow-y: auto;
}
/* Responsive */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  .header-stats {
    grid-template-columns: 1fr;
  }
  .actions-grid {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 768px) {
  .dashboard-container {
    padding: 0 30px;
  }
  .header-content {
    padding: 2rem 1.5rem;
  }
  .card-header {
    padding: 1.25rem 1.5rem;
  }
  .card-content {
    padding: 1.5rem;
  }
}
@media (max-width: 480px) {
  .dashboard-main {
    padding: 20px 0 40px;
  }
  .dashboard-container {
    padding: 0 20px;
  }
  .header-content {
    padding: 1.5rem;
  }
  .header-title {
    font-size: 2rem;
  }
  .greeting-badge {
    font-size: 0.8rem;
    padding: 6px 12px;
  }
  .action-card {
    padding: 1.25rem;
  }
  .action-icon {
    width: 48px;
    height: 48px;
  }
}
</style>