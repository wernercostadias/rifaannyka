<template>
  <section class="base-card">
    <slot />
  </section>
</template>

<style scoped>
.base-card {
  background: var(--color-surface);
  border: 1px solid rgba(244, 143, 177, 0.16);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  padding: 20px;
}
</style>
