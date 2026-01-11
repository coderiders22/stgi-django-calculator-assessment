<template>
  <div class="calculator-wrapper">
    <!-- Professional Info Banner -->
    <div class="info-banner" :class="isGuest ? 'guest-mode' : 'premium-mode'">
      <div class="banner-icon">
        <ShieldAlert v-if="isGuest" :size="24" />
        <CheckCircle2 v-else :size="24" />
      </div>
      <div class="banner-content">
        <div class="banner-title">
          {{ isGuest ? 'Guest Mode Active' : 'Premium Access Active' }}
        </div>
        <div class="banner-description" v-if="isGuest">
          Limited access features enabled
        </div>
        <div class="banner-description" v-else>
          Congratulations! Aap ab saare premium features ko full access kar sakte hai.
        </div>
        <div class="feature-list" v-if="isGuest">
          <div class="feature-item success">
            <CheckCircle2 :size="16" />
            <span>View last 10 calculations</span>
          </div>
          <div class="feature-item disabled">
            <XCircle :size="16" />
            <span>Cannot clear history</span>
          </div>
          <div class="feature-item disabled">
            <XCircle :size="16" />
            <span>Cannot delete individual items</span>
          </div>
        </div>
        <div class="feature-list" v-else>
          <div class="feature-item success">
            <CheckCircle2 :size="16" />
            <span>Unlimited calculations</span>
          </div>
          <div class="feature-item success">
            <CheckCircle2 :size="16" />
            <span>Full history access</span>
          </div>
          <div class="feature-item success">
            <CheckCircle2 :size="16" />
            <span>Advanced features unlocked</span>
          </div>
        </div>
      </div>
      <button v-if="isGuest" class="upgrade-button" @click="$router.push('/login')">
        <span>Login for Full Access</span>
        <ArrowRight :size="18" />
      </button>
    </div>

    <!-- Display Section -->
    <div class="calculator-display">
      <div class="display-header">
        <div class="display-label">
          <CalcIcon :size="16" />
          <span>Current Calculation</span>
        </div>
        <button
          class="clear-btn"
          @click="clearAll"
          title="Clear inputs"
          :disabled="loading"
        >
          <RotateCcw :size="16" />
        </button>
      </div>
      <div class="expression-display">
        <span v-if="a !== null || b !== null" class="expression-text">
          {{ a ?? 0 }} {{ op }} {{ b ?? 0 }}
        </span>
        <span v-else class="placeholder-text">
          Enter your calculation
        </span>
      </div>
    </div>

    <!-- Inputs Section -->
    <div class="calculator-inputs">
      <div class="input-group">
        <label class="input-label">
          <Hash :size="14" /> First Number
        </label>
        <input
          ref="firstInput"
          v-model="a"
          type="number"
          class="input-field"
          placeholder="0"
          @input="onInputA"
          @keyup.enter="focusSecondInput"
        />
      </div>

      <div class="operator-group">
        <label class="input-label">Operator</label>
        <div class="operator-buttons">
          <button
            v-for="o in operators"
            :key="o.value"
            class="operator-btn"
            :class="{ active: op === o.value }"
            @click="op = o.value"
          >
            <component :is="o.icon" :size="20" />
            <span>{{ o.display }}</span>
          </button>
        </div>
      </div>

      <div class="input-group">
        <label class="input-label">
          <Hash :size="14" /> Second Number
        </label>
        <input
          ref="secondInput"
          v-model="b"
          type="number"
          class="input-field"
          placeholder="0"
          @input="onInputB"
          @keyup.enter="calculate"
        />
      </div>
    </div>

    <!-- Calculate Button -->
    <button
      class="calculate-btn"
      :disabled="loading || !canCalculate"
      @click="calculate"
    >
      <span v-if="loading" class="btn-content">
        <span class="spinner"></span>
        Calculating...
      </span>
      <span v-else class="btn-content">
        <Zap :size="18" />
        Calculate
        <ArrowRight :size="18" />
      </span>
    </button>

    <!-- Result Section -->
    <transition name="result">
      <div v-if="result !== null" class="result-section">
        <div class="result-header">
          <CheckCircle2 :size="20" />
          Result
        </div>
        <div class="result-value">
          {{ formatResult(result) }}
        </div>
        <div class="result-actions">
          <button class="result-action-btn" @click="copyResult">
            <Copy :size="16" />
            {{ copied ? 'Copied!' : 'Copy' }}
          </button>
          <button class="result-action-btn" @click="clearResult">
            <X :size="16" />
            Clear
          </button>
        </div>
      </div>
    </transition>

    <!-- Modal -->
    <Modal
      v-if="showModal"
      :text="modalText"
      :type="modalType"
      @close="showModal = false"
    />
  </div>
</template>

<script>
import api from '@/services/api'
import Modal from '@/components/Modal.vue'
import {
  Calculator as CalcIcon,
  Hash,
  Zap,
  ArrowRight,
  CheckCircle2,
  Copy,
  X,
  RotateCcw,
  Plus,
  Minus,
  Asterisk,
  Divide,
  ShieldAlert,
  XCircle
} from 'lucide-vue-next'

export default {
  name: 'Calculator',
  props: {},
  components: {
    Modal,
    CalcIcon,
    Hash,
    Zap,
    ArrowRight,
    CheckCircle2,
    Copy,
    X,
    RotateCcw,
    Plus,
    Minus,
    Asterisk,
    Divide,
    ShieldAlert,
    XCircle
  },
  data() {
    return {
      a: null,
      b: null,
      op: '+',
      result: null,
      loading: false,
      showModal: false,
      modalText: '',
      modalType: 'error',
      copied: false,
      username: null,
      operators: [
        { value: '+', display: '+', icon: 'Plus' },
        { value: '-', display: '−', icon: 'Minus' },
        { value: '*', display: '×', icon: 'Asterisk' },
        { value: '/', display: '÷', icon: 'Divide' }
      ]
    }
  },
  computed: {
    canCalculate() {
      return this.a !== null && this.b !== null
    },
    isGuest() {
      // User is guest if not authenticated
      return !this.username && localStorage.getItem('is_guest') === 'true'
    }
  },
  methods: {
    // Fetch current user from API (just like Navbar)
    async fetchUser() {
      try {
        const res = await api.get('/auth/me/', { withCredentials: true })
        
        if (res.data.is_authenticated) {
          this.username = res.data.username
          localStorage.removeItem('is_guest') // Clear guest mode if authenticated
        } else {
          this.username = null
        }
      } catch (error) {
        this.username = null
      }
    },
    onInputA(e) {
      this.a = e.target.value === '' ? null : parseFloat(e.target.value)
    },
    onInputB(e) {
      this.b = e.target.value === '' ? null : parseFloat(e.target.value)
    },
    async calculate() {
      if (!this.canCalculate) return
      if (this.op === '/' && this.b === 0) {
        this.modalText = 'Cannot divide by zero.'
        this.modalType = 'error'
        this.showModal = true
        return
      }
      this.loading = true
      this.result = null
      try {
        const res = await api.post('/calculate/', {
          operand1: this.a,
          operand2: this.b,
          operator: this.op
        })
        this.result = res.data.result
        this.$emit('calculated')
      } catch (err) {
        if (err.response?.status === 403) {
          // Guest limit reached
          this.modalText = err.response.data.error || 'Guest limit reached. Login to unlock full access.'
          this.modalType = 'warning'
        } else {
          this.modalText =
            err.response?.data?.error ||
            'Calculation failed.'
          this.modalType = 'error'
        }
        this.showModal = true
      } finally {
        this.loading = false
      }
    },
    formatResult(value) {
      return new Intl.NumberFormat('en-US', {
        maximumFractionDigits: 10
      }).format(value)
    },
    async copyResult() {
      await navigator.clipboard.writeText(String(this.result))
      this.copied = true
      setTimeout(() => (this.copied = false), 2000)
    },
    clearResult() {
      this.result = null
    },
    clearAll() {
      this.a = null
      this.b = null
      this.op = '+'
      this.result = null
      this.$refs.firstInput?.focus()
    },
    focusSecondInput() {
      this.$refs.secondInput?.focus()
    }
  },
  async mounted() {
    // Fetch user data when component loads
    await this.fetchUser()
  },
  watch: {
    // Watch route changes to update user data
    '$route'() {
      this.fetchUser()
    }
  }
}
</script>

<style scoped>
.calculator-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Professional Info Banner */
.info-banner {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  padding: 1.5rem;
  border-radius: 16px;
  backdrop-filter: blur(12px);
  border: 1px solid;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  animation: slideDown 0.5s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.info-banner.guest-mode {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.15), rgba(245, 158, 11, 0.15));
  border-color: rgba(245, 158, 11, 0.3);
}

.info-banner.premium-mode {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.15));
  border-color: rgba(16, 185, 129, 0.3);
}

.info-banner:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
}

.banner-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  transition: transform 0.3s ease;
}

.guest-mode .banner-icon {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: white;
}

.premium-mode .banner-icon {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.info-banner:hover .banner-icon {
  transform: scale(1.1) rotate(5deg);
}

.banner-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.banner-title {
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.guest-mode .banner-title {
  color: #92400e;
}

.premium-mode .banner-title {
  color: #065f46;
}

.banner-description {
  font-size: 0.9rem;
  font-weight: 500;
  opacity: 0.85;
  line-height: 1.5;
}

.guest-mode .banner-description {
  color: #78350f;
}

.premium-mode .banner-description {
  color: #047857;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-top: 0.25rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.875rem;
  font-weight: 500;
  padding: 0.4rem 0;
  transition: transform 0.2s ease;
}

.feature-item:hover {
  transform: translateX(4px);
}

.feature-item.success {
  color: #166534;
}

.feature-item.disabled {
  color: #92400e;
  opacity: 0.8;
}

.premium-mode .feature-item.success {
  color: #065f46;
}

.upgrade-button {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.25);
  white-space: nowrap;
  align-self: flex-start;
}

.upgrade-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(245, 158, 11, 0.35);
  background: linear-gradient(135deg, #d97706, #b45309);
}

.upgrade-button:active {
  transform: translateY(0);
}

/* Display Section */
.calculator-display {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.08));
  border: 1px solid rgba(59, 130, 246, 0.15);
  border-radius: 16px;
  padding: 1.5rem;
}

.display-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.display-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 600;
}

.clear-btn {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: white;
  color: var(--text-primary);
  transform: rotate(180deg);
}

.expression-display {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  min-height: 2.5rem;
  display: flex;
  align-items: center;
}

.expression-text {
  color: var(--primary);
}

.placeholder-text {
  color: var(--text-muted);
  font-size: 1.2rem;
  font-weight: 500;
}

/* Inputs Section */
.calculator-inputs {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.input-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-primary);
  font-size: 0.9rem;
  font-weight: 600;
}

.input-field {
  width: 100%;
  padding: 1rem 1.25rem;
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
  transition: all 0.3s ease;
}

.input-field:focus {
  outline: none;
  background: white;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.input-field::placeholder {
  color: var(--text-muted);
  font-weight: 400;
}

/* Operator Buttons */
.operator-group {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.operator-buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}

.operator-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  padding: 1rem 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 1.5rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.operator-btn:hover {
  background: white;
  border-color: rgba(59, 130, 246, 0.2);
  transform: translateY(-2px);
}

.operator-btn.active {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  border-color: var(--primary);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.operator-btn span {
  font-size: 0.75rem;
  font-weight: 600;
}

/* Calculate Button */
.calculate-btn {
  width: 100%;
  padding: 1.25rem;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
  margin-top: 0.5rem;
}

.calculate-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
}

.calculate-btn:disabled {
  background: linear-gradient(135deg, #cbd5e1, #94a3b8);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
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

/* Result Section */
.result-section {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(5, 150, 105, 0.08));
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: var(--success);
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.result-value {
  font-size: 3rem;
  font-weight: 800;
  color: var(--success);
  margin-bottom: 1rem;
  word-break: break-all;
  line-height: 1.2;
}

.result-actions {
  display: flex;
  gap: 0.75rem;
}

.result-action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 10px;
  color: var(--success);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.result-action-btn:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
}

/* Animations */
.result-enter-active,
.result-leave-active {
  transition: all 0.4s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.result-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.result-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

/* Responsive Design */
@media (max-width: 768px) {
  .info-banner {
    flex-direction: column;
    gap: 1rem;
  }

  .banner-icon {
    width: 40px;
    height: 40px;
  }

  .upgrade-button {
    width: 100%;
    justify-content: center;
  }

  .operator-buttons {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .expression-display {
    font-size: 1.5rem;
  }

  .result-value {
    font-size: 2.5rem;
  }

  .result-actions {
    flex-direction: column;
  }

  .feature-list {
    gap: 0.5rem;
  }

  .feature-item {
    font-size: 0.8rem;
  }
}
</style>