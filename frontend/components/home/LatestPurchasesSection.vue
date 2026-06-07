<template>
  <section class="latest-section">
    <div class="section-heading compact">
      <div>
        <span class="step">Participantes</span>
        <h2>Últimas pessoas que compraram</h2>
      </div>
    </div>

    <BaseCard>
      <div v-if="latestPurchases.length" class="latest-list">
        <article v-for="item in latestPurchases" :key="`${item.buyer_name}-${item.created_at}`" class="latest-item">
          <div>
            <strong>{{ item.buyer_name }}</strong>
            <p>{{ item.buyer_phone }}</p>
          </div>
          <div class="latest-numbers">
            {{ item.numbers.slice(0, 6).join(', ') }}
          </div>
        </article>
      </div>
      <p v-else class="muted">Ainda não temos compras confirmadas ou reservas recentes.</p>
    </BaseCard>
  </section>
</template>

<script setup lang="ts">
import type { PublicPurchase } from '~/types/raffle'

defineProps<{
  latestPurchases: PublicPurchase[]
}>()
</script>

<style scoped>
.latest-section {
  margin-top: 24px;
}

.section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.section-heading.compact {
  align-items: start;
}

.step {
  color: var(--color-highlight);
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
}

h2,
p {
  margin-top: 0;
}

h2 {
  margin-bottom: 8px;
  color: #17345f;
}

.muted {
  color: var(--color-muted);
}

.latest-list {
  display: grid;
  gap: 12px;
}

.latest-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border: 1px solid rgba(33, 143, 139, 0.16);
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.72);
  padding: 14px;
}

.latest-item p {
  margin-bottom: 0;
  color: var(--color-muted);
}

.latest-numbers {
  color: #17345f;
  font-weight: 800;
}

@media (max-width: 720px) {
  .section-heading,
  .latest-item {
    align-items: stretch;
    flex-direction: column;
  }
}

@media (max-width: 560px) {
  .latest-numbers {
    align-self: flex-start;
  }
}
</style>
