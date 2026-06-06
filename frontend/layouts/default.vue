<template>
  <div class="app-shell">
    <header class="site-header">
      <div class="container header-content">
        <NuxtLink to="/" class="brand" @click="scrollToTop">Inicio</NuxtLink>
        <button class="header-action" type="button" @click="openPurchaseLookup">
          Ver meus numeros
        </button>
      </div>
    </header>

    <main>
      <slot />
    </main>

    <footer class="site-footer">
      <div class="container">
        Obrigado por fazer parte dessa corrente do bem.
      </div>
    </footer>
  </div>
</template>
 
<script setup lang="ts">
function scrollToTop() {
  if (window.location.pathname === '/') {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

function openPurchaseLookup() {
  window.dispatchEvent(new CustomEvent('open-purchase-lookup'))
}
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgba(255, 248, 250, 0.92);
  border-bottom: 1px solid rgba(244, 143, 177, 0.18);
  backdrop-filter: blur(10px);
}

.header-content {
  min-height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.brand {
  color: var(--color-highlight);
  font-size: 18px;
  font-weight: 700;
}

.header-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 0;
  padding: 8px 12px;
  border-radius: var(--radius-pill);
  background: rgba(212, 175, 55, 0.16);
  color: #7c6318;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.header-action:hover {
  background: rgba(212, 175, 55, 0.26);
  transform: translateY(-1px);
}

main {
  flex: 1;
}

.site-footer {
  padding: 32px 0;
  color: var(--color-muted);
  text-align: center;
}

@media (max-width: 560px) {
  .header-content {
    min-height: 58px;
    gap: 10px;
  }

  .brand {
    font-size: 16px;
  }

  .header-action {
    padding: 6px 10px;
    font-size: 11px;
    text-align: center;
  }

  .site-footer {
    padding: 24px 0;
    font-size: 14px;
  }
}
</style>
