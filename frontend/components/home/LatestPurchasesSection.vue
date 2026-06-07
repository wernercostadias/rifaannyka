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

        <div v-if="showLoadMore" class="load-more-wrap">
          <BaseButton variant="outline" @click="$emit('show-more')">
            Ver mais participantes
          </BaseButton>
        </div>
      </div>
      <p v-else class="muted">Ainda não temos compras confirmadas ou reservas recentes.</p>
    </BaseCard>
  </section>
</template>

<script setup lang="ts">
import type { PublicPurchase } from '~/types/raffle'

defineProps<{
  latestPurchases: PublicPurchase[]
  showLoadMore: boolean
}>()

defineEmits<{
  'show-more': []
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
  gap: 10px;
}

.latest-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border: 1px solid rgba(33, 143, 139, 0.16);
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.72);
  padding: 12px 14px;
}

.latest-item strong {
  display: block;
  margin-bottom: 2px;
  color: #17345f;
}

.latest-item p {
  margin-bottom: 0;
  color: var(--color-muted);
  font-size: 14px;
}

.latest-numbers {
  color: #17345f;
  font-weight: 800;
  font-size: 14px;
  text-align: right;
}

.load-more-wrap {
  display: flex;
  justify-content: center;
  margin-top: 4px;
}

@media (max-width: 720px) {
  .section-heading,
  .latest-item {
    align-items: stretch;
    flex-direction: column;
  }
}

@media (max-width: 560px) {
  .latest-list {
    gap: 8px;
  }

  .latest-item {
    gap: 8px;
    padding: 10px 12px;
  }

  .latest-item strong {
    font-size: 15px;
  }

  .latest-item p,
  .latest-numbers {
    font-size: 13px;
    align-self: flex-start;
    text-align: left;
  }
}
</style>
