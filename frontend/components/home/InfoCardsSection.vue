<template>
  <section class="info-grid">
    <BaseCard class="poster-card prize-card">
      <div class="badge-circle badge-circle--gift" aria-hidden="true">
        <svg viewBox="0 0 48 48" fill="none">
          <rect x="10" y="20" width="28" height="18" rx="2.5" stroke="currentColor" stroke-width="2.6"/>
          <path d="M24 20V38" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>
          <path d="M10 27H38" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>
          <path d="M24 20H15.5C12.4624 20 10 17.5376 10 14.5C10 11.4624 12.4624 9 15.5 9C20 9 22.5 12.5 24 16C25.5 12.5 28 9 32.5 9C35.5376 9 38 11.4624 38 14.5C38 17.5376 35.5376 20 32.5 20H24Z" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="paint-ribbon">Prêmios</div>

      <div class="prize-panel">
        <div class="prize-copy">
          <div class="prize-block">
            <h3>1º Prêmio</h3>
            <ul class="heart-list">
              <li>Um dia de princesa no salão</li>
              <li>Escova</li>
              <li>Prancha</li>
              <li>Manicure e pedicure</li>
              <li>Design simples de sobrancelha</li>
            </ul>
            <img src="/images/kit-escova.png" alt="Kit de pincéis, escova, prancha e acessórios" class="prize-image prize-image--mobile">
          </div>

          <div class="prize-divider"></div>

          <div class="prize-block">
            <h3>2º Prêmio</h3>
            <ul class="heart-list">
              <li>Um kit Boticário Body Splash + Loção Hidratante</li>
            </ul>
            <img src="/images/kit-boticario.png" alt="Kit com body splash e loção hidratante" class="prize-image prize-image--mobile prize-image--mobile-second">
          </div>
        </div>

        <div class="prize-art">
          <img src="/images/kit-escova.png" alt="Dia de princesa prancha e acessórios" class="prize-image prize-image--top">
          <img src="/images/kit-boticario.png" alt="Kit com body splash e loção hidratante" class="prize-image prize-image--bottom">
        </div>
      </div>
    </BaseCard>

    <BaseCard class="poster-card support-card">
      <div class="badge-circle badge-circle--heart" aria-hidden="true">
        <svg viewBox="0 0 48 48" fill="none">
          <path d="M24 39C11 30.5 8 22.5 8 16.5C8 11.2533 12.2533 7 17.5 7C21.1074 7 24.2458 9.0142 26 12.0017C27.7542 9.0142 30.8926 7 34.5 7C39.7467 7 44 11.2533 44 16.5C44 22.5 41 30.5 28 39L26 40.3L24 39Z" stroke="currentColor" stroke-width="2.8" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="support-frame">
        <h3 class="support-title">Sua ajuda faz toda a diferença!</h3>
        <p class="support-text">
          Ao participar, você não está apenas concorrendo a prêmios incríveis,
          mas também investindo no futuro de uma estudante dedicada e cheia de sonhos.
        </p>
        <strong class="thanks">Obrigada pelo carinho e por acreditar!</strong>
        <span class="support-heart" aria-hidden="true">♡</span>
      </div>
    </BaseCard>
  </section>
</template>

<style scoped>
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 22px;
  margin-top: 26px;
}

.poster-card {
  position: relative;
}

.info-grid :deep(.base-card) {
  position: relative;
  overflow: visible;
  border: 2px solid rgba(128, 212, 216, 0.72);
  border-radius: 26px;
  background:
    radial-gradient(circle at top left, rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.82) 42%, rgba(233, 249, 250, 0.9)),
    linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(236, 251, 251, 0.96));
  box-shadow: 0 10px 26px rgba(38, 77, 108, 0.08);
}

.badge-circle {
  position: absolute;
  top: -18px;
  left: -8px;
  z-index: 3;
  display: grid;
  place-items: center;
  width: 78px;
  height: 78px;
  border: 4px solid rgba(20, 53, 95, 0.14);
  border-radius: 50%;
  color: white;
  box-shadow: 0 8px 20px rgba(24, 52, 95, 0.15);
}

.badge-circle svg {
  width: 40px;
  height: 40px;
}

.badge-circle--gift {
  background: linear-gradient(180deg, #2f9b9a 0%, #218f8b 100%);
}

.badge-circle--heart {
  background: #17345f;
}

.paint-ribbon {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  margin: 4px auto 20px;
  width: fit-content;
  min-height: 48px;
  background: linear-gradient(90deg, #2da1a0 0%, #23918f 55%, #2ca7a4 100%);
  color: white;
  padding: 0 24px;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 30px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  clip-path: polygon(3% 8%, 97% 4%, 100% 42%, 96% 96%, 2% 94%, 0 48%);
  box-shadow: 0 10px 14px rgba(35, 145, 143, 0.18);
}

.paint-ribbon::after {
  content: "";
  position: absolute;
  top: 50%;
  left: calc(100% + 18px);
  width: 170px;
  height: 3px;
  background: rgba(128, 212, 216, 0.78);
  transform: translateY(-50%);
}

.paint-ribbon::before {
  content: "";
  position: absolute;
  inset: -2px 6px -2px 4px;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.16);
  opacity: 0.75;
  pointer-events: none;
}

.prize-panel {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 250px;
  gap: 18px;
  align-items: start;
}

.prize-block h3,
.support-title {
  margin: 0 0 8px;
  color: #218f8b;
  font-size: 28px;
  font-weight: 900;
  text-transform: uppercase;
}

.prize-copy {
  display: grid;
  gap: 18px;
}

.heart-list {
  display: grid;
  gap: 7px;
  margin: 0;
  padding: 0;
  list-style: none;
  color: #17345f;
  font-size: 20px;
  line-height: 1.35;
}

.heart-list li {
  position: relative;
  padding-left: 24px;
}

.heart-list li::before {
  content: "♥";
  position: absolute;
  top: 2px;
  left: 0;
  color: #ef78a5;
  font-size: 14px;
}

.prize-divider {
  height: 1px;
  border-top: 2px dashed rgba(173, 205, 213, 0.7);
}

.prize-art {
  display: grid;
  align-content: start;
  justify-items: center;
  gap: 8px;
  padding-top: 4px;
}

.prize-image {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: 18px;
  background: rgba(255, 251, 243, 0.95);
}

.prize-image--mobile {
  display: none;
}

.prize-image--top {
  max-width: 232px;
}

.prize-image--bottom {
  max-width: 206px;
}

.support-card {
  padding-top: 16px;
}

.support-frame {
  position: relative;
  min-height: 100%;
  border: 2px solid rgba(128, 212, 216, 0.45);
  border-radius: 24px;
  background: linear-gradient(180deg, rgba(232, 250, 251, 0.96), rgba(236, 249, 250, 0.86));
  padding: 38px 30px 26px 34px;
}

.support-title {
  margin: 0 auto 8px;
  max-width: 360px;
  text-align: center;
  font-size: 24px;
  line-height: 1.1;
}

.support-text {
  margin: 20px auto 0;
  max-width: 420px;
  color: #17345f;
  font-size: 18px;
  line-height: 1.48;
  text-align: center;
}

.thanks {
  display: block;
  margin-top: 18px;
  color: #17345f;
  font-family: "Parisienne", cursive;
  font-size: 42px;
  font-weight: 400;
  text-align: center;
}

.support-heart {
  position: absolute;
  right: 14px;
  bottom: 6px;
  color: rgba(239, 120, 165, 0.38);
  font-size: 56px;
}

@media (max-width: 720px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .prize-panel {
    grid-template-columns: 1fr;
  }

  .prize-art {
    grid-template-columns: 1fr 1fr;
    align-items: end;
  }

  .support-title,
  .heart-list {
    font-size: 20px;
  }

  .support-text {
    font-size: 17px;
  }

  .thanks {
    font-size: 36px;
  }
}

@media (max-width: 560px) {
  .info-grid :deep(.base-card) {
    padding: 14px;
  }

  .badge-circle {
    width: 66px;
    height: 66px;
    top: -12px;
    left: -4px;
  }

  .badge-circle svg {
    width: 32px;
    height: 32px;
  }

  .paint-ribbon {
    margin: 14px auto 18px;
    min-height: 38px;
    padding: 0 18px;
    font-size: 18px;
  }

  .paint-ribbon::after {
    width: 44px;
  }

  .prize-panel {
    grid-template-columns: 1fr;
  }

  .prize-art {
    display: none;
  }

  .prize-block h3,
  .support-title {
    font-size: 18px;
  }

  .heart-list,
  .support-text {
    font-size: 15px;
  }

  .prize-block {
    display: grid;
    gap: 10px;
  }

  .prize-image--mobile {
    display: block;
    width: min(100%, 210px);
    margin: 6px auto 0;
    padding: 8px;
    border-radius: 20px;
  }

  .prize-image--mobile-second {
    width: min(100%, 190px);
  }

  .support-frame {
    padding: 34px 18px 22px;
  }

  .thanks {
    font-size: 28px;
    line-height: 1;
    text-align: center;
  }

  .support-heart {
    right: 10px;
    bottom: 4px;
    font-size: 48px;
  }
}
</style>
