<!-- src/components/Modal.vue -->
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card" @click.stop>
      <!-- Icon with gradient background -->
      <div class="modal-icon-wrapper" :class="type">
        <component :is="iconComponent" :size="40" />
      </div>

      <!-- Message -->
      <h3 class="modal-title">
        {{ titleText }}
      </h3>
      <p class="modal-text">{{ text }}</p>

      <!-- Action Button -->
      <button class="modal-action-btn" @click="$emit('close')">
        {{ buttonText }}
        <ArrowRight v-if="type === 'success'" :size="18" />
      </button>
    </div>
  </div>
</template>

<script>
import { CheckCircle, AlertTriangle, ArrowRight, ShieldAlert } from 'lucide-vue-next'

export default {
  name: 'Modal',
  props: {
    text: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'error',
      validator: value => ['error', 'success', 'warning'].includes(value)
    }
  },
  components: {
    CheckCircle,
    AlertTriangle,
    ArrowRight,
    ShieldAlert
  },
  computed: {
    iconComponent() {
      if (this.type === 'success') return 'CheckCircle'
      if (this.type === 'warning') return 'ShieldAlert'
      return 'AlertTriangle'
    },
    titleText() {
      if (this.type === 'success') return 'Success!'
      if (this.type === 'warning') return 'Oops!'
      return 'Error!'
    },
    buttonText() {
      if (this.type === 'success') return 'Continue'
      if (this.type === 'warning') return 'Try Again'
      return 'Close'
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
  animation: fadeIn 0.3s ease-out;
}

.modal-card {
  background: white;
  border-radius: 24px;
  width: 90%;
  max-width: 420px;
  padding: 2.5rem 2rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
  text-align: center;
  position: relative;
  overflow: hidden;
  animation: modalPop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Icon wrapper with gradient */
.modal-icon-wrapper {
  width: 90px;
  height: 90px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.modal-icon-wrapper.success {
  background: linear-gradient(135deg, #10b981, #059669);
}

.modal-icon-wrapper.error {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.modal-icon-wrapper.warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

/* Title & Text */
.modal-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 0.75rem;
  letter-spacing: -0.02em;
}

.modal-text {
  font-size: 1.1rem;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 2rem;
}

/* Action Button */
.modal-action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 1rem 2.2rem;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 0.61, 0.36, 1);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.modal-action-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.45);
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes modalPop {
  from {
    opacity: 0;
    transform: scale(0.85) translateY(40px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Responsive */
@media (max-width: 480px) {
  .modal-card {
    padding: 2rem 1.5rem;
  }
  .modal-title {
    font-size: 1.6rem;
  }
  .modal-text {
    font-size: 1rem;
  }
}
</style>