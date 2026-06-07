<template>
  <section id="numeros" ref="sectionEl" class="numbers-section">
    <div class="ticket-heading">
      <span class="side-mark">⌁</span>
      <h2>Escolha seu número!</h2>
      <span class="side-mark">⌁</span>
    </div>

    <BaseCard>
      <div class="ticket-subhead">
        <p>Selecione de 001 a {{ String(raffle?.total_numbers || 200).padStart(3, '0') }}</p>
        <div v-if="raffle" class="price-pill">R$ {{ raffle.price_per_number }} cada</div>
      </div>

      <p v-if="pending">Carregando números...</p>
      <div v-else-if="errorMessage" class="empty-state">
        <strong>{{ errorMessage }}</strong>
        <p>Rode <code>just seed</code> para criar uma rifa demo ativa com 200 números, ou ative uma rifa pelo admin.</p>
      </div>
      <template v-else>
        <NumberGrid :numbers="visibleNumbers" :selected="selectedNumbers" @toggle="$emit('toggle-number', $event)" />
        <div v-if="showLoadMore" class="load-more-wrap">
          <BaseButton variant="outline" @click="$emit('show-more')">
            Ver mais números
          </BaseButton>
        </div>
      </template>

      <div class="selection-bar">
        <div>
          <strong>{{ selectedNumbers.length }} número(s) escolhido(s)</strong>
          <p>{{ selectedNumbers.join(', ') || 'Nenhum número selecionado ainda' }}</p>
        </div>
        <div class="selection-actions">
          <span>Total: R$ {{ totalAmount }}</span>
          <BaseButton :disabled="selectedNumbers.length === 0" @click="$emit('open-buyer-modal')">
            Continuar
          </BaseButton>
        </div>
      </div>
    </BaseCard>
  </section>
</template>

<script setup lang="ts">
import type { Raffle, RaffleNumber } from '~/types/raffle'

defineProps<{
  raffle: Raffle | null
  pending: boolean
  errorMessage: string
  visibleNumbers: RaffleNumber[]
  selectedNumbers: number[]
  showLoadMore: boolean
  totalAmount: string
}>()

defineEmits<{
  'toggle-number': [number: number]
  'show-more': []
  'open-buyer-modal': []
}>()

const sectionEl = ref<HTMLElement | null>(null)

defineExpose({
  sectionEl,
})
</script>

<style scoped>
.numbers-section {
  margin-top: 24px;
}

.numbers-section :deep(.base-card) {
  border: 2px solid rgba(33, 143, 139, 0.38);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 10px 0 rgba(74, 74, 74, 0.06), var(--shadow-card);
}

.ticket-heading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 18px;
  margin-bottom: -2px;
  text-align: center;
}

.ticket-heading h2 {
  position: relative;
  margin: 0;
  border-radius: 10px 4px 10px 4px;
  background: #17345f;
  color: white;
  padding: 10px 36px;
  font-size: 25px;
  font-weight: 900;
  text-transform: uppercase;
}

.ticket-heading h2::before,
.ticket-heading h2 > span::after {
  content: "";
  position: absolute;
  top: 50%;
  width: 80px;
  height: 2px;
  background: rgba(33, 143, 139, 0.5);
}

.ticket-heading h2::before {
  right: calc(100% + 18px);
}

.ticket-heading h2 > span::after {
  left: calc(100% + 18px);
}

.side-mark {
  color: #218f8b;
  font-size: 44px;
  font-weight: 900;
}

.ticket-subhead {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 16px;
}

.ticket-subhead p {
  margin: 0;
  color: #17345f;
  font-weight: 800;
}

.price-pill {
  flex: 0 0 auto;
  border-radius: var(--radius-pill);
  background: rgba(212, 175, 55, 0.16);
  color: #7c6318;
  padding: 10px 14px;
  font-weight: 800;
}

.empty-state {
  display: grid;
  gap: 8px;
  border: 1px dashed rgba(244, 143, 177, 0.42);
  border-radius: var(--radius-md);
  background: var(--color-background);
  padding: 18px;
}

.empty-state p {
  margin-bottom: 0;
  color: var(--color-muted);
}

code {
  border-radius: var(--radius-sm);
  background: var(--color-primary-light);
  color: var(--color-highlight);
  padding: 2px 6px;
  font-weight: 800;
}

.selection-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-top: 20px;
  border-top: 1px solid rgba(33, 143, 139, 0.22);
  padding-top: 18px;
}

.selection-bar p {
  margin-bottom: 0;
  color: var(--color-muted);
  overflow-wrap: anywhere;
}

.load-more-wrap {
  display: flex;
  justify-content: center;
  margin-top: 14px;
}

.selection-actions {
  display: flex;
  align-items: center;
  gap: 14px;
  font-weight: 800;
}

@media (max-width: 720px) {
  .ticket-heading h2 {
    padding-inline: 18px;
    font-size: 18px;
  }

  .ticket-heading h2::before,
  .ticket-heading h2::after {
    display: none;
  }

  .ticket-subhead,
  .selection-bar,
  .selection-actions {
    align-items: stretch;
    flex-direction: column;
  }

  .ticket-subhead p,
  .price-pill {
    text-align: center;
  }
}

@media (max-width: 560px) {
  .ticket-heading {
    gap: 8px;
  }

  .side-mark {
    font-size: 30px;
  }

  .numbers-section :deep(.base-card) {
    padding: 14px;
  }

  .selection-actions {
    gap: 10px;
  }

  .selection-actions span {
    text-align: center;
  }
}
</style>
