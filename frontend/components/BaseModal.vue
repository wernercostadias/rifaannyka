<template>
  <Teleport to="body">
    <div v-if="open" class="modal-backdrop" @click.self="$emit('close')">
      <section class="modal-panel" role="dialog" aria-modal="true">
        <header class="modal-header">
          <div>
            <p v-if="eyebrow" class="eyebrow">{{ eyebrow }}</p>
            <h2>{{ title }}</h2>
          </div>
          <button class="close-button" type="button" aria-label="Fechar" @click="$emit('close')">x</button>
        </header>
        <slot />
      </section>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
defineProps<{
  open: boolean
  title: string
  eyebrow?: string
}>()

defineEmits<{
  close: []
}>()
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: grid;
  place-items: center;
  background: rgba(74, 74, 74, 0.42);
  padding: 20px;
}

.modal-panel {
  width: min(100%, 520px);
  max-height: min(760px, 100%);
  overflow: auto;
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  box-shadow: 0 24px 80px rgba(74, 74, 74, 0.24);
  padding: 22px;
}

.modal-header {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.eyebrow {
  margin: 0 0 6px;
  color: var(--color-highlight);
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
}

h2 {
  margin: 0;
  color: var(--color-highlight);
}

.close-button {
  width: 34px;
  height: 34px;
  border: 0;
  border-radius: var(--radius-pill);
  background: var(--color-primary-light);
  color: var(--color-highlight);
  cursor: pointer;
  font-weight: 800;
}
</style>
