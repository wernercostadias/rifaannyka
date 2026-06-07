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
  background:
    linear-gradient(180deg, rgba(255, 248, 250, 0.96), rgba(255, 251, 245, 0.92));
  border-bottom: 1px solid rgba(33, 143, 139, 0.12);
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
  display: inline-flex;
  align-items: center;
  min-height: 42px;
  padding: 0 18px;
  border: 1px solid rgba(33, 143, 139, 0.22);
  border-radius: var(--radius-pill);
  background: rgba(250, 218, 221, 0.48);
  color: #17345f;
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.01em;
  box-shadow: 0 10px 24px rgba(244, 143, 177, 0.1);
  transition: transform 0.2s ease, background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}

.brand:hover {
  background: rgba(250, 218, 221, 0.7);
  border-color: rgba(33, 143, 139, 0.34);
  color: #218f8b;
  transform: translateY(-1px);
}

.header-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  border: 1px solid rgba(23, 52, 95, 0.06);
  padding: 0 18px;
  border-radius: var(--radius-pill);
  background: linear-gradient(135deg, #17345f, #218f8b);
  color: white;
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 0.01em;
  cursor: pointer;
  box-shadow: 0 14px 28px rgba(23, 52, 95, 0.18);
  transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
}

.header-action:hover {
  filter: brightness(1.04);
  box-shadow: 0 16px 32px rgba(23, 52, 95, 0.24);
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
    min-height: 38px;
    padding-inline: 14px;
    font-size: 14px;
  }

  .header-action {
    min-height: 38px;
    padding-inline: 14px;
    font-size: 12px;
    text-align: center;
  }

  .site-footer {
    padding: 24px 0;
    font-size: 14px;
  }
}
</style>
