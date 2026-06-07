<template>
  <button class="base-button" :class="`base-button--${variant}`" :disabled="disabled || loading">
    <span v-if="loading" class="base-button__content">
      <span class="base-button__spinner" aria-hidden="true"></span>
      <span>Carregando...</span>
    </span>
    <span v-else class="base-button__content">
      <slot />
    </span>
  </button>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    variant?: 'primary' | 'secondary' | 'outline' | 'gold'
    disabled?: boolean
    loading?: boolean
  }>(),
  {
    variant: 'primary',
    disabled: false,
    loading: false,
  },
)
</script>

<style scoped>
.base-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 46px;
  border: 0;
  border-radius: var(--radius-pill);
  cursor: pointer;
  padding: 0 22px;
  font-weight: 700;
  transition: transform 0.16s ease, box-shadow 0.16s ease, opacity 0.16s ease;
}

.base-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-soft);
}

.base-button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.base-button--primary {
  background: var(--color-primary);
  color: white;
}

.base-button--secondary {
  background: var(--color-secondary);
  color: white;
}

.base-button--outline {
  background: transparent;
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
}

.base-button--gold {
  background: var(--color-accent);
  color: white;
}

.base-button__content {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.base-button__spinner {
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: base-button-spin 0.75s linear infinite;
}

@keyframes base-button-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
