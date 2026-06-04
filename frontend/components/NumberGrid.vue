<template>
  <div class="number-grid">
    <button
      v-for="item in numbers"
      :key="item.id"
      class="number-cell"
      :class="cellClass(item)"
      :disabled="item.status !== 'available'"
      @click="$emit('toggle', item.number)"
    >
      <span v-if="item.status === 'paid' && item.owner_name" class="number-cell__badge number-cell__badge--paid">
        {{ item.owner_name }}
      </span>
      <span v-else-if="item.status === 'reserved'" class="number-cell__badge number-cell__badge--reserved">
        Reservado
      </span>
      <span class="number-cell__value">{{ String(item.number).padStart(3, '0') }}</span>
    </button>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  numbers: Array<{ id: number; number: number; status: string; owner_name?: string }>
  selected: number[]
}>()

defineEmits<{
  toggle: [number: number]
}>()

function cellClass(item: { number: number; status: string }) {
  if (props.selected.includes(item.number)) {
    return 'number-cell--selected'
  }
  return `number-cell--${item.status}`
}
</script>

<style scoped>
.number-grid {
  display: grid;
  grid-template-columns: repeat(10, minmax(58px, 1fr));
  gap: 6px;
}

.number-cell {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 58px;
  padding: 16px 8px 8px;
  border: 1px solid rgba(33, 143, 139, 0.58);
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.78);
  color: #17345f;
  cursor: pointer;
  font-size: 18px;
  font-weight: 800;
  transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease, background 0.16s ease;
}

.number-cell:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 16px rgba(23, 52, 95, 0.08);
}

.number-cell__value {
  line-height: 1;
  transition: opacity 0.16s ease;
}

.number-cell__badge {
  position: absolute;
  top: 4px;
  left: 4px;
  right: 4px;
  overflow: hidden;
  border-radius: 8px 8px 10px 10px;
  background: rgba(33, 143, 139, 0.16);
  color: var(--color-primary);
  padding: 3px 6px;
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.02em;
  line-height: 1.1;
  text-align: center;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.number-cell__badge--reserved {
  background: rgba(190, 145, 226, 0.18);
  color: #8d5db6;
}

.number-cell--selected {
  border-color: var(--color-primary);
  background: var(--color-primary);
  color: white;
}

.number-cell--reserved {
  border-color: rgba(223, 197, 242, 0.9);
  background: rgba(239, 224, 250, 0.88);
  cursor: not-allowed;
}

@media (max-width: 760px) {
  .number-grid {
    grid-template-columns: repeat(5, minmax(0, 1fr));
  }

  .number-cell {
    min-height: 50px;
    font-size: 15px;
  }

  .number-cell__badge {
    font-size: 8px;
  }
}

@media (max-width: 480px) {
  .number-grid {
    gap: 5px;
  }

  .number-cell {
    min-height: 44px;
    border-radius: 10px;
    font-size: 13px;
  }

  .number-cell__badge {
    top: 3px;
    left: 3px;
    right: 3px;
  }
}

.number-cell--paid,
.number-cell--canceled {
  border-color: rgba(171, 208, 205, 0.9);
  background: rgba(231, 246, 244, 0.96);
  color: #1b5b69;
  cursor: not-allowed;
}

.number-cell--paid .number-cell__badge {
  background: rgba(33, 143, 139, 0.22);
  color: #1f8581;
}

.number-cell--paid .number-cell__value {
  opacity: 0.92;
}

.number-cell--reserved .number-cell__value,
.number-cell--canceled .number-cell__value {
  opacity: 0.86;
}
</style>
