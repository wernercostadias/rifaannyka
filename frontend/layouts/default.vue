<template>
  <div class="app-shell">
    <header class="site-header">
      <div class="container header-content">
        <NuxtLink to="/" class="brand">Rifa Beneficente</NuxtLink>
        <span class="badge">Ajude essa campanha</span>
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

.badge {
  padding: 8px 12px;
  border-radius: var(--radius-pill);
  background: rgba(212, 175, 55, 0.16);
  color: #7c6318;
  font-size: 13px;
  font-weight: 600;
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

  .badge {
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
