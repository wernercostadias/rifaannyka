<template>
  <BaseModal
    :open="open"
    title="Ver meus numeros"
    eyebrow="Consulta rápida"
    @close="$emit('close')"
  >
    <form class="modal-form" @submit.prevent="$emit('submit')">
      <p class="muted">
        Digite seu nome completo ou celular para conferir seus números e quando a reserva ou compra foi feita.
      </p>
      <BaseInput
        :model-value="query"
        label="Nome completo ou celular"
        placeholder="Ex.: Ana Silva ou 91999991234"
        :error="error"
        @update:model-value="$emit('update:query', $event)"
      />

      <BaseButton :loading="loading" :disabled="!canLookup" type="submit">
        Buscar meus números
      </BaseButton>
    </form>

    <div v-if="results.length" class="lookup-results">
      <article
        v-for="item in results"
        :key="item.reference"
        class="lookup-card"
      >
        <div class="lookup-card__header">
          <div>
            <strong>{{ item.buyer_name }}</strong>
            <p>{{ item.buyer_phone }}</p>
          </div>
          <StatusBadge :status="item.status" />
        </div>

        <p class="lookup-card__numbers">
          Numeros: {{ formatNumbers(item.numbers) }}
        </p>
        <p class="lookup-card__meta">
          {{ item.status_label }} em {{ formatPurchaseDate(item.created_at) }}
        </p>
      </article>
    </div>

    <p v-else-if="searched" class="muted lookup-empty">
      Nenhuma reserva ou compra foi encontrada com esses dados nesta rifa.
    </p>
  </BaseModal>
</template>

<script setup lang="ts">
import type { LookupPurchase } from '~/types/raffle'

defineProps<{
  open: boolean
  query: string
  error: string
  loading: boolean
  canLookup: boolean
  searched: boolean
  results: LookupPurchase[]
  formatNumbers: (items: number[]) => string
  formatPurchaseDate: (value: string) => string
}>()

defineEmits<{
  close: []
  submit: []
  'update:query': [value: string]
}>()
</script>

<style scoped>
.muted {
  color: var(--color-muted);
}

.modal-form,
.lookup-results {
  display: grid;
  gap: 14px;
}

.lookup-card {
  display: grid;
  gap: 8px;
  border: 1px solid rgba(33, 143, 139, 0.18);
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.74);
  padding: 14px;
}

.lookup-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.lookup-card__header p,
.lookup-card__numbers,
.lookup-card__meta {
  margin: 0;
}

.lookup-card__header p,
.lookup-card__meta {
  color: var(--color-muted);
}

.lookup-empty {
  margin-top: 14px;
}

@media (max-width: 720px) {
  .lookup-card__header {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
