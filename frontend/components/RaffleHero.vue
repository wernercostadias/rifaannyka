<template>
  <section class="poster-hero">
    <div class="decor decor-cap" aria-hidden="true">
      <svg viewBox="0 0 96 72">
        <path d="M12 24 48 10l36 14-36 14L12 24Z" />
        <path d="M28 33v11c0 4 9 10 20 10s20-6 20-10V33" />
        <path d="M78 27v18" />
        <path d="M48 21l10 4" />
        <circle cx="78" cy="49" r="4.5" />
      </svg>
    </div>

    <div class="decor decor-heart-one" aria-hidden="true">♡</div>
    <div class="decor decor-heart-two" aria-hidden="true">♡</div>
    <div class="decor decor-star-one" aria-hidden="true">☆</div>
    <div class="decor decor-star-two" aria-hidden="true">☆</div>

    <div class="hero-copy">
      <div class="title-wrap">
        <h1>
          <span class="title-raffle">Rifa</span>
          <span class="title-student">Estudantil</span>
        </h1>
      </div>

      <div class="future-ribbon">
        <span>♥</span>
        Juntos pelo futuro da Annyka!
      </div>

      <div class="story">
        <p>
          Meu nome é <strong>Ânnyka Yasmin</strong>, tenho <strong>16 anos</strong> e
          sigo meus estudos com dedicação. Sou fluente em
          <strong>inglês</strong> e estou começando uma nova etapa como
          <strong>estagiária</strong>.
        </p>
        <p>
          Neste momento, conquistar um <strong>notebook</strong> vai me ajudar a
          ampliar meus estudos e acompanhar com mais estrutura as atividades do
          curso de especialização no <strong>IEMA</strong>.
        </p>
      </div>
    </div>
    <div class="message-cloud">
      Sua ajuda transforma sonhos em conquistas!
    </div>

    <div class="hero-media">
      <div class="photo-frame">
        <img :src="heroImage" :alt="raffle?.title || 'Foto da Annyka'" class="hero-photo">
      </div>

      <div class="price-seal">
        <span>Valor da rifa</span>
        <strong>{{ formattedPrice }}</strong>
      </div>

      <blockquote>
        <span>“</span>
        Educação é o que me move. Com o seu apoio, posso ir mais longe!
      </blockquote>

      <div class="goal-card">
        <div class="goal-card__values">
          <div class="goal-card__group">
            <span class="goal-card__label">Arrecadado</span>
            <strong class="goal-card__amount">{{ formattedRaisedAmount }}</strong>
          </div>
          <div class="goal-card__group">
            <span class="goal-card__label">Meta</span> 
            <strong class="goal-card__amount">{{ formattedGoalAmount }}</strong>
          </div>
        </div>
        <p>{{ soldCountLabel }}</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const props = defineProps<{
  raffle?: {
    title: string
    description: string
    beneficiary_name: string
    image?: string
    goal_amount?: string | number
    price_per_number?: string | number
    raised_amount?: string | number
    progress_percentage?: string | number
    sold_count?: number
    total_numbers?: number
  } | null
}>()

const heroImage = '/images/img.png'

const currencyFormatter = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

const formattedPrice = computed(() => {
  const price = Number(props.raffle?.price_per_number || 0)
  return currencyFormatter.format(price)
})

const formattedGoalAmount = computed(() => {
  const amount = Number(props.raffle?.goal_amount || 0)
  return currencyFormatter.format(amount)
})

const formattedRaisedAmount = computed(() => {
  const amount = Number(props.raffle?.raised_amount || 0)
  return currencyFormatter.format(amount)
})

const soldCountLabel = computed(() => {
  const soldCount = props.raffle?.sold_count || 0
  const totalNumbers = props.raffle?.total_numbers || 0
  return `${soldCount} de ${totalNumbers} rifas vendidas`
})
</script>

<style scoped>
.poster-hero {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 220px 360px;
  gap: 18px;
  align-items: start;
  min-height: 430px;
  padding: 44px 34px 28px;
  border-radius: 18px;
  background: transparent;
  color: #17345f;
  overflow: hidden;
}

.hero-copy {
  position: relative;
  z-index: 2;
  padding-top: 18px;
}

.title-wrap {
  position: relative;
}

h1 {
  margin: 0;
  line-height: 0.78;
}

.title-raffle {
  display: block;
  color: #17345f;
  font-family: "Cormorant Garamond", Georgia, "Times New Roman", serif;
  font-size: clamp(78px, 10vw, 132px);
  font-weight: 700;
  letter-spacing: 0;
}

.title-student {
  display: block;
  margin-top: 10px;
  color: #218f8b;
  font-family: "Parisienne", "Brush Script MT", "Segoe Script", cursive;
  font-size: clamp(72px, 8.8vw, 122px);
  font-weight: 400;
  line-height: 0.78;
}

.future-ribbon {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin: 28px 0 22px;
  border-radius: var(--radius-pill);
  background: var(--color-primary-light);
  color: #17345f;
  padding: 10px 22px;
  font-size: 19px;
  font-weight: 900;
  text-transform: uppercase;
}

.future-ribbon span {
  color: #17345f;
  font-size: 24px;
}

.story {
  max-width: 590px;
  display: grid;
  gap: 14px;
  margin: 0;
  padding-left: 20px;
  border-left: 4px solid rgba(33, 143, 139, 0.2);
  color: #17345f;
  font-size: 19px;
  line-height: 1.56;
  text-wrap: pretty;
}

.story p {
  margin: 0;
}

.story strong {
  color: #218f8b;
  font-weight: 900;
}

.message-cloud {
  position: relative;
  z-index: 2;
  justify-self: center;
  width: 210px;
  margin-top: 6px;
  color: #17345f;
  font-size: 18px;
  font-weight: 900;
  line-height: 1.22;
  text-align: center;
  text-transform: uppercase;
}

.message-cloud::before {
  content: "";
  position: absolute;
  inset: -28px -22px;
  z-index: -1;
  border: 5px solid var(--color-primary);
  border-bottom-color: transparent;
  border-radius: 48% 52% 44% 56% / 58% 42% 58% 42%;
  transform: rotate(-8deg);
}

.hero-media {
  position: relative;
  z-index: 2;
  display: grid;
  justify-items: center;
  gap: 8px;
  padding-bottom: 20px;
}

.photo-frame {
  position: relative;
  z-index: 1;
  width: 320px;
  aspect-ratio: 0.78;
  overflow: hidden;
  background: transparent;
}

.photo-frame::before {
  content: "";
  position: absolute;
  inset: 18px 24px 8px;
  z-index: 0;
  border-radius: 46% 54% 34% 34% / 28% 28% 38% 38%;
  background:
    radial-gradient(circle at 50% 24%, rgba(250, 218, 221, 0.9), rgba(250, 218, 221, 0.4) 46%, transparent 72%),
    radial-gradient(circle at 50% 72%, rgba(33, 143, 139, 0.14), transparent 66%);
  filter: blur(8px);
}

.hero-photo,
.placeholder {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  object-fit: contain;
  background: transparent;
  color: var(--color-highlight);
  font-weight: 900;
}

.hero-photo {
  object-position: center top;
  transform: translateX(0) translateY(0) scale(1.14);
  transform-origin: center top;
}

.price-seal {
  position: absolute;
  right: 2px;
  top: 194px;
  z-index: 5;
  display: grid;
  place-items: center;
  align-content: center;
  width: 148px;
  height: 148px;
  border: 6px solid white;
  border-radius: 47% 53% 49% 51% / 52% 48% 52% 48%;
  background: #218f8b;
  color: white;
  box-shadow: var(--shadow-card);
  text-align: center;
  text-transform: uppercase;
  gap: 6px;
  padding: 18px 14px;
}

.price-seal::after {
  content: "";
  position: absolute;
  inset: -10px;
  border: 2px solid rgba(33, 143, 139, 0.42);
  border-radius: 53% 47% 51% 49% / 48% 52% 48% 52%;
}

.price-seal span {
  max-width: 96px;
  font-size: 12px;
  font-weight: 900;
  line-height: 1.1;
  text-align: center;
}

.price-seal strong {
  display: block;
  font-size: 24px;
  line-height: 1;
  white-space: nowrap;
}

blockquote {
  position: relative;
  width: min(100%, 340px);
  z-index: 1;
  margin: 10px 0 0;
  border-radius: 36px 12px 36px 12px;
  background: rgba(250, 218, 221, 0.55);
  color: #17345f;
  padding: 24px 20px 18px 54px;
  font-size: 17px;
  font-weight: 800;
  line-height: 1.35;
}

blockquote span {
  position: absolute;
  left: 16px;
  top: 4px;
  color: #218f8b;
  font-size: 56px;
  line-height: 1;
}

.goal-card {
  width: min(100%, 336px);
  margin-top: 16px;
  background: transparent;
  padding: 0;
  text-align: left;
}

.goal-card__values {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
}

.goal-card__group {
  min-width: 0;
}

.goal-card__label {
  display: block;
  margin-bottom: 5px;
  color: #218f8b;
  font-size: 11px;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.goal-card__amount {
  display: block;
  color: #17345f;
  font-size: 30px;
  font-weight: 900;
  line-height: 1;
  white-space: nowrap;
}

.goal-card p {
  margin: 8px 0 0;
  color: rgba(23, 52, 95, 0.9);
  font-size: 12px;
  font-weight: 700;
}

.decor {
  position: absolute;
  z-index: 1;
  pointer-events: none;
}

.decor svg {
  width: 100%;
  height: 100%;
  fill: none;
  stroke: #218f8b;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 4;
}

.decor-cap {
  left: 18px;
  top: 4px;
  width: 96px;
  height: 72px;
}

.decor-heart-one {
  right: 40px;
  top: 92px;
  color: #218f8b;
  font-size: 42px;
  transform: rotate(-12deg);
}

.decor-heart-two {
  right: 138px;
  bottom: 26px;
  color: #218f8b;
  font-size: 46px;
  transform: rotate(10deg);
}

.decor-star-one {
  right: 320px;
  top: 18px;
  color: #218f8b;
  font-size: 50px;
  transform: rotate(12deg);
}

.decor-star-two {
  right: 26px;
  top: 22px;
  color: var(--color-primary);
  font-size: 44px;
  transform: rotate(18deg);
}

@media (max-width: 1180px) {
  .poster-hero {
    grid-template-columns: minmax(0, 1fr) 180px 320px;
    gap: 12px;
    padding: 34px 24px 24px;
  }

  .title-raffle {
    font-size: clamp(68px, 9vw, 110px);
  }

  .title-student {
    font-size: clamp(58px, 7vw, 92px);
  }

  .message-cloud {
    width: 172px;
    font-size: 16px;
    margin-top: 2px;
  }

  .photo-frame {
    width: 288px;
  }

  .price-seal {
    right: -2px;
    top: 172px;
    width: 134px;
    height: 134px;
  }

  .decor-star-one {
    right: 274px;
    top: 12px;
  }

  .decor-heart-two {
    right: 124px;
    bottom: 20px;
  }

  .goal-card {
    width: min(100%, 300px);
  }
}

@media (max-width: 980px) {
  .poster-hero {
    grid-template-columns: minmax(0, 1fr) 280px;
    gap: 18px 12px;
    min-height: 0;
    padding: 28px 18px 26px;
  }

  .hero-copy {
    grid-column: 1 / 2;
    padding-top: 8px;
  }

  .message-cloud {
    grid-column: 1 / 2;
    justify-self: start;
    width: 198px;
    margin-top: 10px;
    margin-left: 8px;
  }

  .message-cloud {
    font-size: 15px;
  }

  .hero-media {
    grid-column: 2 / 3;
    align-self: start;
    justify-self: center;
  }

  .story {
    font-size: 18px;
    gap: 12px;
    padding-left: 16px;
  }

  .photo-frame {
    width: 260px;
  }

  .price-seal {
    right: 0;
    top: 156px;
    width: 126px;
    height: 126px;
  }

  blockquote {
    width: min(100%, 280px);
    margin-top: 8px;
    font-size: 15px;
    padding: 22px 16px 16px 46px;
  }

  blockquote span {
    left: 12px;
    font-size: 46px;
  }

  .goal-card {
    width: min(100%, 284px);
    margin-top: 12px;
  }

  .decor-cap {
    left: 8px;
    top: 2px;
    width: 78px;
    height: 58px;
  }

  .decor-heart-one {
    right: 18px;
    top: 86px;
    font-size: 34px;
  }

  .decor-heart-two {
    right: 108px;
    bottom: 8px;
    font-size: 36px;
  }

  .decor-star-one {
    right: 214px;
    top: 14px;
    font-size: 40px;
  }

  .decor-star-two {
    right: 14px;
    top: 18px;
    font-size: 34px;
  }
}

@media (max-width: 560px) {
  .poster-hero {
    grid-template-columns: 1fr;
    gap: 6px;
    border-radius: 16px;
    margin-inline: 0;
    padding: 44px 14px 20px;
  }

  .hero-copy,
  .message-cloud,
  .hero-media {
    grid-column: auto;
  }

  .message-cloud {
    justify-self: end;
    width: 96px;
    margin: -2px 12px -10px 0;
    font-size: 8px;
    line-height: 1.14;
  }

  .message-cloud::before {
    inset: -14px -10px;
    border-width: 3px;
  }

  .story {
    font-size: 17px;
  }

  .title-raffle {
    font-size: 64px;
  }

  .title-student {
    font-size: 54px;
  }

  .future-ribbon {
    width: 100%;
    justify-content: center;
    padding: 10px 14px;
    font-size: 14px;
    text-align: center;
  }

  .photo-frame {
    width: min(100%, 244px);
  }

  .photo-frame::before {
    inset: 14px 16px 4px;
    filter: blur(7px);
  }

  .hero-media {
    position: relative;
    width: 292px;
    margin-inline: auto;
    justify-self: center;
  }

  .price-seal {
    right: 2px;
    top: 136px;
    width: 108px;
    height: 108px;
    padding: 14px 10px;
  }

  .price-seal span {
    max-width: 70px;
    font-size: 9px;
  }

  .price-seal strong {
    font-size: 17px;
  }

  blockquote {
    width: 262px;
    margin: -4px auto 0;
    padding-right: 14px;
    padding-left: 42px;
    font-size: 14px;
  }

  .goal-card {
    width: 262px;
    margin: 8px auto 0;
  }

  .goal-card__values {
    gap: 10px;
    justify-content: space-between;
  }

  .goal-card__amount {
    font-size: 20px;
    line-height: 1.05;
  }

  .goal-card p {
    font-size: 11px;
  }

  .decor-cap {
    left: 6px;
    top: 10px;
    width: 64px;
    height: 48px;
  }

  .decor-heart-one {
    right: 10px;
    top: 88px;
    font-size: 32px;
  }

  .decor-heart-two {
    right: 42px;
    top: 38px;
    bottom: auto;
    font-size: 24px;
  }

  .decor-star-one {
    right: 2px;
    left: auto;
    top: 14px;
    font-size: 30px;
  }

  .decor-star-two {
    right: 58px;
    top: 98px;
    font-size: 20px;
  }
}

@media (max-width: 400px) {
  .poster-hero {
    padding-inline: 10px;
    padding-top: 46px;
  }

  .title-raffle {
    font-size: 54px;
  }

  .title-student {
    font-size: 46px;
  }

  .message-cloud {
    width: 92px;
    margin-right: 8px;
  }

  .decor-heart-one {
    right: 8px;
    top: 84px;
  }

  .decor-heart-two {
    right: 34px;
    top: 40px;
  }

  .decor-star-one {
    right: 2px;
    top: 16px;
  }

  .decor-star-two {
    right: 48px;
    top: 94px;
  }

  .hero-media {
    width: 272px;
  }

  .photo-frame {
    width: 226px;
  }

  .photo-frame::before {
    inset: 12px 12px 2px;
  }

  .price-seal {
    right: 0;
    top: 128px;
    width: 108px;
    height: 108px;
  }

  blockquote {
    width: 244px;
  }

  .goal-card {
    width: 244px;
  }

  .goal-card__amount {
    font-size: 21px;
  }

  .price-seal {
    right: 6px;
    top: 142px;
    width: 100px;
    height: 100px;
  }

  .price-seal span {
    max-width: 64px;
    font-size: 8px;
  }

  .price-seal strong {
    font-size: 15px;
  }

  .goal-card__values {
    gap: 8px;
  }

  .goal-card__label {
    font-size: 10px;
  }

  .goal-card__amount {
    font-size: 18px;
  }

  .decor-cap {
    left: 4px;
    top: 10px;
    width: 58px;
    height: 44px;
  }
}
</style>
