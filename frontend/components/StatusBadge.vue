<template>
  <span class="status-badge" :class="`status-badge--${status}`">
    {{ label }}
  </span>
</template>

<script setup lang="ts">
const props = defineProps<{
  status: 'pending' | 'reserved' | 'paid' | 'canceled' | 'expired' | string
}>()

const labels: Record<string, string> = {
  pending: 'Pendente',
  reserved: 'Reservado',
  paid: 'Pago',
  canceled: 'Cancelado',
  expired: 'Expirado',
}

const label = computed(() => labels[props.status] || props.status)
</script>

<style scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  border-radius: var(--radius-pill);
  padding: 0 10px;
  font-size: 13px;
  font-weight: 700;
}

.status-badge--pending {
  background: var(--color-warning);
}

.status-badge--reserved {
  background: var(--color-reserved);
}

.status-badge--paid {
  background: var(--color-success);
}

.status-badge--canceled {
  background: var(--color-neutral);
}

.status-badge--expired {
  background: var(--color-danger);
}
</style>
