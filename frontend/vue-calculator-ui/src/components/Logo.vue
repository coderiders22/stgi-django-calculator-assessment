<!-- src/components/Logo.vue -->
<template>
  <div class="logo-wrapper" :class="{ small: small }">
    <svg viewBox="0 0 380 100" class="logo-svg">
      <text x="0" y="72" class="text-calc">Calc</text>
      <text x="172" y="72" class="text-pro">Pro</text>
    </svg>
  </div>
</template>

<script>
export default {
  props: { small: Boolean }
}
</script>

<style scoped>
.logo-wrapper {
  display: inline-flex;
  align-items: center;
}
.logo-svg {
  height: 42px;
  width: auto;
}
.text-calc {
  font-family: 'Inter', system-ui, sans-serif;
  font-weight: 800;
  font-size: 68px;
  fill: var(--text-primary);
  letter-spacing: -0.04em;
}
.text-pro {
  font-family: 'Inter', system-ui, sans-serif;
  font-weight: 900;
  font-size: 68px;
  fill: var(--primary);
  letter-spacing: -0.03em;
}

.small .logo-svg {
  height: 32px;
}
.small .text-calc,
.small .text-pro {
  font-size: 52px;
}
</style>