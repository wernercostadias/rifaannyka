<template>
  <BaseModal :open="open" title="Seus dados" eyebrow="2. Identificação" @close="$emit('close')">
    <form class="modal-form" @submit.prevent="$emit('submit')">
      <p class="muted">Esses dados ficam vinculados à sua reserva, sem precisar criar conta.</p>
      <BaseInput
        :model-value="buyer.full_name"
        label="Nome completo"
        name="full_name"
        autocomplete="name"
        :error="errors.full_name"
        @update:model-value="$emit('update:full-name', $event)"
      />
      <BaseInput
        :model-value="buyer.email"
        label="E-mail"
        name="email"
        type="email"
        placeholder="voce@email.com"
        inputmode="email"
        autocomplete="email"
        :error="errors.email"
        @update:model-value="$emit('update:email', $event)"
      />
      <BaseInput
        :model-value="buyer.phone"
        label="Celular"
        name="phone"
        placeholder="(91) 99999-9999"
        inputmode="tel"
        autocomplete="tel"
        :maxlength="15"
        :error="errors.phone"
        @update:model-value="$emit('update:phone', $event)"
      />
      <BaseInput
        :model-value="buyer.cpf"
        label="CPF"
        name="cpf"
        placeholder="000.000.000-00"
        inputmode="numeric"
        autocomplete="off"
        :maxlength="14"
        :error="errors.cpf"
        @update:model-value="$emit('update:cpf', $event)"
      />

      <div class="modal-summary">
        <span>Números: {{ selectedNumbers.join(', ') }}</span>
        <strong>Total: R$ {{ totalAmount }}</strong>
      </div>

      <BaseButton :disabled="!canSubmit" :loading="submitting">
        Pagar
      </BaseButton>
    </form>
  </BaseModal>
</template>

<script setup lang="ts">
import type { BuyerFormData, BuyerFormErrors } from '~/types/raffle'

defineProps<{
  open: boolean
  buyer: BuyerFormData
  errors: BuyerFormErrors
  selectedNumbers: number[]
  totalAmount: string
  canSubmit: boolean
  submitting: boolean
}>()

defineEmits<{
  close: []
  submit: []
  'update:full-name': [value: string]
  'update:email': [value: string]
  'update:phone': [value: string]
  'update:cpf': [value: string]
}>()
</script>

<style scoped>
.muted {
  color: var(--color-muted);
}

.modal-form {
  display: grid;
  gap: 14px;
}

.modal-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border-radius: var(--radius-md);
  background: rgba(244, 143, 177, 0.12);
  padding: 14px;
}

@media (max-width: 560px) {
  .modal-summary {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
