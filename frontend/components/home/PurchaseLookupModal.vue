<template>
  <BaseModal
    :open="open"
    title="Ver meus numeros"
    eyebrow="Consulta rápida"
    @close="$emit('close')"
  >
    <form class="modal-form" @submit.prevent="$emit('submit')">
      <p class="muted">
        Escolha como deseja buscar para conferir seus números e quando a reserva ou compra foi feita.
      </p>

      <div class="lookup-methods" role="radiogroup" aria-label="Forma de busca">
        <button
          type="button"
          class="lookup-method"
          :class="{ 'lookup-method--active': searchType === 'name' }"
          @click="$emit('update:search-type', 'name')"
        >
          Buscar por nome
        </button>
        <button
          type="button"
          class="lookup-method"
          :class="{ 'lookup-method--active': searchType === 'cpf' }"
          @click="$emit('update:search-type', 'cpf')"
        >
          Buscar por CPF
        </button>
      </div>

      <BaseInput
        v-if="searchType === 'name'"
        :model-value="query"
        label="Nome completo"
        placeholder="Ex.: Ana Silva"
        autocomplete="name"
        :error="error"
        @update:model-value="$emit('update:query', $event)"
      />

      <BaseInput
        v-else
        :model-value="query"
        label="CPF"
        name="lookup_cpf"
        placeholder="000.000.000-00"
        inputmode="numeric"
        autocomplete="off"
        :maxlength="14"
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
  searchType: 'name' | 'cpf'
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
  'update:search-type': [value: 'name' | 'cpf']
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

.lookup-methods {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.lookup-method {
  min-height: 46px;
  border: 1px solid rgba(33, 143, 139, 0.18);
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.82);
  color: #17345f;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s ease, border-color 0.2s ease, background-color 0.2s ease;
}

.lookup-method:hover {
  transform: translateY(-1px);
  border-color: rgba(33, 143, 139, 0.3);
  background: rgba(250, 218, 221, 0.3);
}

.lookup-method--active {
  border-color: rgba(33, 143, 139, 0.42);
  background: rgba(33, 143, 139, 0.1);
  box-shadow: 0 0 0 3px rgba(33, 143, 139, 0.08);
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
  .lookup-methods {
    grid-template-columns: 1fr;
  }

  .lookup-card__header {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
