<template>
  <BaseModal :open="open" title="" eyebrow="3. Pagamento" @close="$emit('close')">
    <p v-if="!mercadoPagoReady" class="payment-warning">
      {{ mercadoPagoErrorMessage }}
    </p>

    <div v-if="purchase && !paymentConfirmed" class="payment-box">
      <div class="payment-box__header">
        <StatusBadge :status="purchase.status" />
        <span v-if="reservationDeadlineLabel" class="payment-deadline">
          Pague até {{ reservationDeadlineLabel }}
        </span>
      </div>
      <p class="payment-summary">{{ paymentSummaryText }}</p>
      <p v-if="paymentPendingHint" class="payment-hint">{{ paymentPendingHint }}</p>
    </div>

    <div v-if="paymentConfirmed && purchase" class="payment-success">
      <div class="payment-success__spark" aria-hidden="true">✦</div>
      <div class="payment-success__spark payment-success__spark--right" aria-hidden="true">✦</div>
      <p class="payment-success__eyebrow">Pagamento confirmado</p>
      <h3>Seus números já estão garantidos.</h3>
      <p class="payment-success__lead">
        Obrigado, <strong>{{ fullBuyerName }}</strong>. Sua participação foi confirmada com sucesso.
      </p>
      <div class="payment-success__numbers">
        <span>Seus números</span>
        <strong>{{ formatNumbers(purchase.numbers) }}</strong>
      </div>
    </div>

    <div v-if="payment && !paymentConfirmed && !paymentExpired" class="pix-box">
      <img v-if="payment.qr_code" class="pix-qr" :src="`data:image/jpeg;base64,${payment.qr_code}`" alt="QR Code Pix">
      <textarea readonly :value="payment.qr_code_text" />
      <BaseButton variant="outline" type="button" @click="$emit('copy-pix')">Copiar código Pix</BaseButton>
    </div>

    <div class="modal-actions">
      <template v-if="payment && !paymentConfirmed">
        <p class="muted payment-note">{{ paymentStatusMessage }}</p>
        <BaseButton
          v-if="paymentSimulationEnabled && payment.status !== 'paid' && !paymentExpired"
          variant="outline"
          type="button"
          :loading="simulatingPayment"
          @click="$emit('simulate-payment')"
        >
          Simular pagamento
        </BaseButton>
      </template>
    </div>
  </BaseModal>
</template>

<script setup lang="ts">
import type { PaymentResponse, PurchaseResponse } from '~/types/raffle'

defineProps<{
  open: boolean
  mercadoPagoReady: boolean
  mercadoPagoErrorMessage: string
  purchase: PurchaseResponse | null
  payment: PaymentResponse | null
  paymentConfirmed: boolean
  paymentExpired: boolean
  paymentSummaryText: string
  paymentStatusMessage: string
  paymentSimulationEnabled: boolean
  simulatingPayment: boolean
  fullBuyerName: string
  reservationDeadlineLabel: string
  paymentPendingHint: string
  formatNumbers: (items: number[]) => string
}>()

defineEmits<{
  close: []
  'copy-pix': []
  'simulate-payment': []
}>()
</script>

<style scoped>
.muted {
  color: var(--color-muted);
}

.payment-box,
.pix-box {
  display: grid;
  gap: 8px;
  border-radius: var(--radius-md);
  background: var(--color-background);
  padding: 14px;
}

.pix-qr {
  width: min(100%, 220px);
  margin-inline: auto;
  border-radius: 12px;
  background: white;
  padding: 10px;
}

.payment-box,
.pix-box,
.modal-actions {
  margin-top: 14px;
}

.payment-summary {
  margin: 0;
  color: #17345f;
  line-height: 1.5;
}

.payment-box__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.payment-deadline {
  color: #7b678f;
  font-size: 12px;
  font-weight: 700;
}

.payment-hint {
  margin: 0;
  color: #6c7f93;
  font-size: 12px;
  line-height: 1.45;
}

.payment-success {
  position: relative;
  overflow: hidden;
  display: grid;
  gap: 12px;
  margin-top: 14px;
  border: 1px solid rgba(42, 163, 159, 0.28);
  border-radius: 24px;
  background:
    radial-gradient(circle at top, rgba(255, 255, 255, 0.96), rgba(255, 255, 255, 0.84) 52%, rgba(233, 249, 250, 0.94)),
    linear-gradient(135deg, rgba(255, 248, 252, 0.92), rgba(233, 248, 250, 0.96));
  padding: 22px 18px;
  text-align: center;
  box-shadow: 0 14px 32px rgba(23, 52, 95, 0.1);
}

.payment-success::after {
  content: "";
  position: absolute;
  inset: auto -18% -48% -18%;
  height: 140px;
  background: radial-gradient(circle, rgba(239, 120, 165, 0.12), transparent 64%);
  pointer-events: none;
}

.payment-success__spark {
  position: absolute;
  top: 18px;
  left: 18px;
  color: #ef78a5;
  font-size: 22px;
}

.payment-success__spark--right {
  right: 18px;
  left: auto;
  color: #2aa39f;
}

.payment-success__eyebrow {
  margin: 0;
  color: #2aa39f;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.payment-success h3 {
  margin: 0;
  color: #17345f;
  font-size: 28px;
  line-height: 1.05;
}

.payment-success__lead {
  margin: 0;
  color: #35506f;
  font-size: 17px;
  line-height: 1.5;
}

.payment-success__numbers {
  display: grid;
  gap: 4px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.78);
  padding: 14px 16px;
}

.payment-success__numbers span {
  color: #6c7f93;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.payment-success__numbers strong {
  color: #17345f;
  font-size: 28px;
  line-height: 1.1;
}

.payment-note {
  margin: 0;
  text-align: center;
}

.payment-warning {
  margin-top: 14px;
  color: #9b1c1c;
  font-weight: 700;
}

textarea {
  width: 100%;
  min-height: 92px;
  resize: vertical;
  border: 1px solid rgba(244, 143, 177, 0.28);
  border-radius: var(--radius-md);
  color: var(--color-text);
  padding: 10px;
}

@media (max-width: 560px) {
  .payment-box__header {
    align-items: start;
    flex-direction: column;
  }
}
</style>
