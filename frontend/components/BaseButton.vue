<template>
  <button class="base-button" :class="`base-button--${variant}`" :disabled="disabled || loading">
    <span v-if="loading">Carregando...</span>
    <slot v-else />
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
</style>
