<template>
  <div class="container page">
    <RaffleHero :raffle="raffle" @choose="scrollToNumbers" />

    <section id="numeros" ref="numbersSection" class="numbers-section">
      <div class="ticket-heading">
        <span class="side-mark">⌁</span>
        <h2>Escolha seu número!</h2>
        <span class="side-mark">⌁</span>
      </div>

      <BaseCard>
        <div class="ticket-subhead">
          <p>Selecione de 001 a {{ String(raffle?.total_numbers || 200).padStart(3, '0') }}</p>
          <div v-if="raffle" class="price-pill">R$ {{ raffle.price_per_number }} cada</div>
        </div>

        <p v-if="pending">Carregando números...</p>
        <div v-else-if="errorMessage" class="empty-state">
          <strong>{{ errorMessage }}</strong>
          <p>Rode <code>just seed</code> para criar uma rifa demo ativa com 200 números, ou ative uma rifa pelo admin.</p>
        </div>
        <template v-else>
          <NumberGrid :numbers="visibleNumbers" :selected="selectedNumbers" @toggle="toggleNumber" />
          <div v-if="showLoadMore" class="load-more-wrap">
            <BaseButton variant="outline" @click="showMoreNumbers">
              Ver mais números
            </BaseButton>
          </div>
        </template>

        <div class="selection-bar">
          <div>
            <strong>{{ selectedNumbers.length }} número(s) escolhido(s)</strong>
            <p>{{ selectedNumbers.join(', ') || 'Nenhum número selecionado ainda' }}</p>
          </div>
          <div class="selection-actions">
            <span>Total: R$ {{ totalAmount }}</span>
            <BaseButton :disabled="selectedNumbers.length === 0" @click="buyerModalOpen = true">
              Continuar
            </BaseButton>
          </div>
        </div>
      </BaseCard>
    </section>

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
                <li>Um kit de pincéis com hidratação</li>
                <li>Escova</li>
                <li>Prancha</li>
                <li>Manicure e pedicure</li>
                <li>Design simples de sobrancelha</li>
              </ul>
            </div>

            <div class="prize-divider"></div>

            <div class="prize-block">
              <h3>2º Prêmio</h3>
              <ul class="heart-list">
                <li>Um kit Boticário Body Splash + Loção Hidratante</li>
              </ul>
            </div>
          </div>

          <div class="prize-art">
            <img src="/images/kit-escova.png" alt="Kit de pincéis, escova, prancha e acessórios" class="prize-image prize-image--top">
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

    <BaseModal
      :open="lookupModalOpen"
      title="Ver meus numeros"
      eyebrow="Consulta rápida"
      @close="lookupModalOpen = false"
    >
      <form class="modal-form" @submit.prevent="lookupPurchases">
        <p class="muted">
          Digite seu nome completo ou celular para conferir seus números e quando a reserva ou compra foi feita.
        </p>
        <BaseInput
          v-model="lookupQuery"
          label="Nome completo ou celular"
          placeholder="Ex.: Ana Silva ou 91999991234"
          :error="lookupError"
        />

        <BaseButton :loading="lookupLoading" :disabled="!canLookup" type="submit">
          Buscar meus números
        </BaseButton>
      </form>

      <div v-if="lookupResults.length" class="lookup-results">
        <article
          v-for="item in lookupResults"
          :key="item.reference"
          class="lookup-card"
        >
          <div class="lookup-card__header">
            <div>
              <strong>{{ item.buyer_name }}</strong>
              <p>{{ item.buyer_phone }}</p>
            </div>
            <StatusBadge :status="item.status" />
          </div>

          <p class="lookup-card__numbers">
            Numeros: {{ formatNumbers(item.numbers) }}
          </p>
          <p class="lookup-card__meta">
            {{ item.status_label }} em {{ formatPurchaseDate(item.created_at) }}
          </p>
        </article>
      </div>

      <p v-else-if="lookupSearched" class="muted lookup-empty">
        Nenhuma reserva ou compra foi encontrada com esses dados nesta rifa.
      </p>
    </BaseModal>

    <BaseModal :open="buyerModalOpen" title="Seus dados" eyebrow="2. Identificação" @close="buyerModalOpen = false">
      <form class="modal-form" @submit.prevent="submitPurchase">
        <p class="muted">Esses dados ficam vinculados à sua reserva, sem precisar criar conta.</p>
        <BaseInput v-model="buyer.full_name" label="Nome completo" />
        <BaseInput v-model="buyer.phone" label="Celular" placeholder="(91) 99999-9999" />
        <BaseInput v-model="buyer.cpf" label="CPF" placeholder="000.000.000-00" />

        <div class="modal-summary">
          <span>Números: {{ selectedNumbers.join(', ') }}</span>
          <strong>Total: R$ {{ totalAmount }}</strong>
        </div>

        <BaseButton :disabled="!canSubmit" :loading="submitting">
          Reservar e escolher pagamento
        </BaseButton>
      </form>
    </BaseModal>

    <BaseModal :open="paymentModalOpen" title="Forma de pagamento" eyebrow="3. Pagamento" @close="paymentModalOpen = false">
      <div class="payment-options">
        <button
          class="payment-option"
          :class="{ 'payment-option--active': paymentMethod === 'pix' }"
          type="button"
          @click="paymentMethod = 'pix'"
        >
          <strong>Pix</strong>
          <span>Gerar código copia e cola</span>
        </button>
      </div>

      <p v-if="!mercadoPagoReady" class="payment-warning">
        {{ mercadoPagoErrorMessage }}
      </p>

      <div v-if="purchase" class="payment-box">
        <StatusBadge :status="purchase.status" />
        <p>Reserva criada para {{ purchase.buyer.first_name }}.</p>
        <p class="muted">Referência: {{ purchase.reference }}</p>
      </div>

      <div v-if="payment" class="pix-box">
        <strong>Pix copia e cola</strong>
        <img v-if="payment.qr_code" class="pix-qr" :src="`data:image/jpeg;base64,${payment.qr_code}`" alt="QR Code Pix">
        <textarea readonly :value="payment.qr_code_text" />
        <BaseButton variant="outline" type="button" @click="copyPix">Copiar código Pix</BaseButton>
      </div>

      <div class="modal-actions">
        <BaseButton v-if="!payment" :disabled="!mercadoPagoReady" :loading="creatingPayment" @click="createPixPayment">
          Gerar pagamento Pix
        </BaseButton>
        <p v-else class="muted payment-note">Aguardando confirmação do pagamento pelo Mercado Pago.</p>
      </div>
    </BaseModal>
  </div>
</template>

<script setup lang="ts">
type Raffle = {
  id: number
  title: string
  description: string
  beneficiary_name: string
  image?: string
  goal_amount: string
  price_per_number: string
  raised_amount: string
  progress_percentage: string
  sold_count: number
  total_numbers: number
}

type RaffleNumber = {
  id: number
  number: number
  status: string
  owner_name?: string
}

type PublicPurchase = {
  buyer_name: string
  buyer_phone: string
  numbers: number[]
  status: string
  created_at: string
}

type LookupPurchase = {
  reference: string
  buyer_name: string
  buyer_phone: string
  numbers: number[]
  status: string
  status_label: string
  created_at: string
}

const api = useApi()
const { $mercadoPago, $mercadoPagoPublicKey, $mercadoPagoLoadError } = useNuxtApp()
const numbersSection = ref<HTMLElement | null>(null)
const raffle = ref<Raffle | null>(null)
const numbers = ref<RaffleNumber[]>([])
const latestPurchases = ref<PublicPurchase[]>([])
const selectedNumbers = ref<number[]>([])
const pending = ref(true)
const submitting = ref(false)
const creatingPayment = ref(false)
const errorMessage = ref('')
const purchase = ref<any>(null)
const payment = ref<any>(null)
const buyerModalOpen = ref(false)
const paymentModalOpen = ref(false)
const lookupModalOpen = ref(false)
const paymentMethod = ref<'pix'>('pix')
const isMobileNumbers = ref(false)
const visibleNumberCount = ref(Number.POSITIVE_INFINITY)
const lookupQuery = ref('')
const lookupLoading = ref(false)
const lookupError = ref('')
const lookupSearched = ref(false)
const lookupResults = ref<LookupPurchase[]>([])
const DESKTOP_INITIAL_NUMBERS = 70
const DESKTOP_LOAD_STEP = 70
const MOBILE_INITIAL_NUMBERS = 50
const MOBILE_LOAD_STEP = 50

const buyer = reactive({
  full_name: '',
  phone: '',
  cpf: '',
})

const totalAmount = computed(() => {
  const price = Number(raffle.value?.price_per_number || 0)
  return (price * selectedNumbers.value.length).toFixed(2).replace('.', ',')
})

const visibleNumbers = computed(() => numbers.value.slice(0, visibleNumberCount.value))

const showLoadMore = computed(() => {
  return visibleNumberCount.value < numbers.value.length
})

const mercadoPagoReady = computed(() => Boolean($mercadoPago && $mercadoPagoPublicKey))
const mercadoPagoErrorMessage = computed(() => {
  if ($mercadoPagoLoadError) {
    return 'Nao foi possivel carregar o Mercado Pago. Tente novamente em instantes.'
  }
  return 'Mercado Pago.js ainda nao foi inicializado. Verifique a NUXT_PUBLIC_MERCADOPAGO_PUBLIC_KEY no ambiente.'
})

const canSubmit = computed(() => {
  return selectedNumbers.value.length > 0 && buyer.full_name && buyer.phone && buyer.cpf && mercadoPagoReady.value
})

const canLookup = computed(() => {
  const query = lookupQuery.value.trim()
  const digits = query.replace(/\D/g, '')
  return query.length >= 3 || digits.length >= 4
})

onMounted(async () => {
  syncNumberViewport()
  window.addEventListener('resize', syncNumberViewport)
  window.addEventListener('open-purchase-lookup', openPurchaseLookup)
  await loadRaffle()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', syncNumberViewport)
  window.removeEventListener('open-purchase-lookup', openPurchaseLookup)
})

async function loadRaffle() {
  pending.value = true
  try {
    raffle.value = await api('/raffles/active/')
    if (raffle.value) {
      await Promise.all([loadNumbers(), loadLatestPurchases()])
    }
  } catch (error) {
    errorMessage.value = 'Não foi possível carregar a rifa ativa.'
  } finally {
    pending.value = false
  }
}

async function loadNumbers() {
  if (!raffle.value) {
    return
  }
  numbers.value = await api(`/raffles/${raffle.value.id}/numbers/`)
  syncNumberViewport()
}

async function loadLatestPurchases() {
  if (!raffle.value) {
    return
  }
  latestPurchases.value = await api(`/purchases/latest/?raffle_id=${raffle.value.id}`)
}

function openPurchaseLookup() {
  lookupError.value = ''
  lookupModalOpen.value = true
}

function scrollToNumbers() {
  numbersSection.value?.scrollIntoView({ behavior: 'smooth' })
}

function toggleNumber(number: number) {
  if (selectedNumbers.value.includes(number)) {
    selectedNumbers.value = selectedNumbers.value.filter((item) => item !== number)
    return
  }
  selectedNumbers.value = [...selectedNumbers.value, number].sort((a, b) => a - b)
}

async function submitPurchase() {
  if (!raffle.value || !canSubmit.value) {
    return
  }

  submitting.value = true
  errorMessage.value = ''
  payment.value = null
  try {
    const response = await api('/purchases/', {
      method: 'POST',
      body: {
        raffle_id: raffle.value.id,
        buyer: {
          full_name: buyer.full_name,
          phone: buyer.phone,
          cpf: buyer.cpf,
        },
        numbers: selectedNumbers.value,
        payment_provider: 'mercadopago',
      },
    })
    purchase.value = response.purchase
    payment.value = response.payment
    buyerModalOpen.value = false
    paymentModalOpen.value = true
    await Promise.all([loadNumbers(), loadLatestPurchases()])
    selectedNumbers.value = []
  } catch (error) {
    errorMessage.value = 'Nao foi possivel iniciar o pagamento. Nenhum numero foi reservado.'
  } finally {
    submitting.value = false
  }
}

async function createPixPayment() {
  if (!purchase.value || payment.value) {
    return
  }

  creatingPayment.value = true
  try {
    payment.value = await api('/payments/', {
      method: 'POST',
      body: {
        purchase_reference: purchase.value.reference,
        provider: 'mercadopago',
      },
    })
  } finally {
    creatingPayment.value = false
  }
}

async function copyPix() {
  if (payment.value?.qr_code_text) {
    await navigator.clipboard.writeText(payment.value.qr_code_text)
  }
}

async function lookupPurchases() {
  if (!raffle.value) {
    return
  }

  const query = lookupQuery.value.trim()
  const digits = query.replace(/\D/g, '')

  if (query.length < 3 && digits.length < 4) {
    lookupError.value = 'Informe pelo menos 3 letras do nome ou 4 digitos do celular.'
    lookupResults.value = []
    lookupSearched.value = false
    return
  }

  lookupLoading.value = true
  lookupError.value = ''
  lookupSearched.value = false

  try {
    lookupResults.value = await api('/purchases/lookup/', {
      query: {
        raffle_id: raffle.value.id,
        search: query,
      },
    })
    lookupSearched.value = true
  } catch (error: any) {
    lookupResults.value = []
    lookupError.value = error?.data?.search?.[0] || error?.data?.search || 'Nao foi possivel buscar seus numeros agora.'
  } finally {
    lookupLoading.value = false
  }
}

function formatNumbers(items: number[]) {
  return items.map((item) => String(item).padStart(3, '0')).join(', ')
}

function formatPurchaseDate(value: string) {
  return new Intl.DateTimeFormat('pt-BR', {
    dateStyle: 'short',
    timeStyle: 'short',
  }).format(new Date(value))
}

function syncNumberViewport() {
  const mobile = window.innerWidth <= 560
  const wasMobile = isMobileNumbers.value
  isMobileNumbers.value = mobile
  const targetInitialCount = mobile ? MOBILE_INITIAL_NUMBERS : DESKTOP_INITIAL_NUMBERS

  if (visibleNumberCount.value === Number.POSITIVE_INFINITY || mobile !== wasMobile) {
    visibleNumberCount.value = Math.min(targetInitialCount, numbers.value.length || targetInitialCount)
  }
}

function showMoreNumbers() {
  const step = isMobileNumbers.value ? MOBILE_LOAD_STEP : DESKTOP_LOAD_STEP
  visibleNumberCount.value = Math.min(visibleNumberCount.value + step, numbers.value.length)
}
</script>

<style scoped>
.page {
  padding-bottom: 48px;
}

.numbers-section,
.latest-section {
  margin-top: 24px;
}

.numbers-section :deep(.base-card) {
  border: 2px solid rgba(33, 143, 139, 0.38);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 10px 0 rgba(74, 74, 74, 0.06), var(--shadow-card);
}

.ticket-heading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 18px;
  margin-bottom: -2px;
  text-align: center;
}

.ticket-heading h2 {
  position: relative;
  margin: 0;
  border-radius: 10px 4px 10px 4px;
  background: #17345f;
  color: white;
  padding: 10px 36px;
  font-size: 25px;
  font-weight: 900;
  text-transform: uppercase;
}

.ticket-heading h2::before,
.ticket-heading h2 > span::after {
  content: "";
  position: absolute;
  top: 50%;
  width: 80px;
  height: 2px;
  background: rgba(33, 143, 139, 0.5);
}

.ticket-heading h2::before {
  right: calc(100% + 18px);
}

.ticket-heading h2 > span::after {
  left: calc(100% + 18px);
}

.side-mark {
  color: #218f8b;
  font-size: 44px;
  font-weight: 900;
}

.ticket-subhead {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 16px;
}

.ticket-subhead p {
  margin: 0;
  color: #17345f;
  font-weight: 800;
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

.price-pill {
  flex: 0 0 auto;
  border-radius: var(--radius-pill);
  background: rgba(212, 175, 55, 0.16);
  color: #7c6318;
  padding: 10px 14px;
  font-weight: 800;
}

.empty-state {
  display: grid;
  gap: 8px;
  border: 1px dashed rgba(244, 143, 177, 0.42);
  border-radius: var(--radius-md);
  background: var(--color-background);
  padding: 18px;
}

.empty-state p {
  margin-bottom: 0;
  color: var(--color-muted);
}

code {
  border-radius: var(--radius-sm);
  background: var(--color-primary-light);
  color: var(--color-highlight);
  padding: 2px 6px;
  font-weight: 800;
}

.selection-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-top: 20px;
  border-top: 1px solid rgba(33, 143, 139, 0.22);
  padding-top: 18px;
}

.selection-bar p {
  margin-bottom: 0;
  color: var(--color-muted);
  overflow-wrap: anywhere;
}

.load-more-wrap {
  display: flex;
  justify-content: center;
  margin-top: 14px;
}

.selection-actions {
  display: flex;
  align-items: center;
  gap: 14px;
  font-weight: 800;
}

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
  display: inline-flex;
  align-items: center;
  margin: 4px 0 20px 64px;
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
  padding: 26px 30px 26px 34px;
}

.support-title {
  max-width: 360px;
  font-size: 24px;
  line-height: 1.1;
}

.support-text {
  margin: 20px 0 0;
  color: #17345f;
  font-size: 18px;
  line-height: 1.48;
}

.thanks {
  display: block;
  margin-top: 28px;
  color: #17345f;
  font-family: "Brush Script MT", "Segoe Script", cursive;
  font-size: 34px;
  font-weight: 400;
  line-height: 1;
}

.support-heart {
  position: absolute;
  right: 18px;
  bottom: 10px;
  color: #1ca19b;
  font-size: 58px;
  line-height: 1;
  transform: rotate(-10deg);
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
  border: 1px solid rgba(244, 143, 177, 0.14);
  border-radius: var(--radius-md);
  padding: 12px;
}

.latest-item strong,
.latest-numbers {
  overflow-wrap: anywhere;
}

.latest-item p {
  margin-bottom: 0;
  color: var(--color-muted);
}

.latest-numbers {
  border-radius: var(--radius-pill);
  background: var(--color-primary-light);
  color: var(--color-highlight);
  padding: 8px 10px;
  font-size: 13px;
  font-weight: 800;
}

.lookup-results {
  display: grid;
  gap: 12px;
  margin-top: 16px;
}

.lookup-card {
  display: grid;
  gap: 10px;
  border: 1px solid rgba(33, 143, 139, 0.18);
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.88);
  padding: 14px;
}

.lookup-card__header {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 12px;
}

.lookup-card__header p,
.lookup-card__numbers,
.lookup-card__meta,
.lookup-empty {
  margin-bottom: 0;
}

.lookup-card__numbers {
  color: #17345f;
  font-weight: 800;
}

.lookup-card__meta {
  color: var(--color-muted);
}

.modal-form {
  display: grid;
  gap: 14px;
}

.modal-summary,
.payment-box,
.pix-box {
  display: grid;
  gap: 8px;
  border-radius: var(--radius-md);
  background: var(--color-background);
  padding: 14px;
}

.pix-qr {
  width: min(100%, 220px);
  margin-inline: auto;
  border-radius: 12px;
  background: white;
  padding: 10px;
}

.payment-options {
  display: grid;
  gap: 10px;
}

.payment-option {
  display: grid;
  gap: 4px;
  border: 1px solid rgba(244, 143, 177, 0.28);
  border-radius: var(--radius-md);
  background: white;
  color: var(--color-text);
  cursor: pointer;
  padding: 14px;
  text-align: left;
}

.payment-option--active {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(244, 143, 177, 0.16);
}

.payment-box,
.pix-box,
.modal-actions {
  margin-top: 14px;
}

.payment-note {
  text-align: center;
}

.payment-warning {
  margin-top: 14px;
  color: #9b1c1c;
  font-weight: 700;
}

textarea {
  width: 100%;
  min-height: 92px;
  resize: vertical;
  border: 1px solid rgba(244, 143, 177, 0.28);
  border-radius: var(--radius-md);
  color: var(--color-text);
  padding: 10px;
}

@media (max-width: 720px) {
  .ticket-heading h2 {
    padding-inline: 18px;
    font-size: 18px;
  }

  .ticket-heading h2::before,
  .ticket-heading h2::after {
    display: none;
  }

  .ticket-subhead {
    align-items: stretch;
    flex-direction: column;
  }

  .ticket-subhead p,
  .price-pill {
    text-align: center;
  }

  .section-heading,
  .selection-bar,
  .selection-actions,
  .latest-item,
  .lookup-card__header {
    align-items: stretch;
    flex-direction: column;
  }

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
  .page {
    padding-bottom: 34px;
  }

  .ticket-heading {
    gap: 8px;
  }

  .side-mark {
    font-size: 30px;
  }

  .numbers-section :deep(.base-card),
  .info-grid :deep(.base-card) {
    padding: 14px;
  }

  .selection-actions {
    gap: 10px;
  }

  .selection-actions span,
  .total {
    text-align: center;
  }

  .latest-numbers {
    align-self: flex-start;
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
    margin: 10px 0 18px 46px;
    min-height: 38px;
    padding: 0 18px;
    font-size: 18px;
  }

  .paint-ribbon::after {
    width: 44px;
  }

  .prize-panel,
  .prize-art {
    grid-template-columns: 1fr;
  }

  .prize-block h3,
  .support-title {
    font-size: 18px;
  }

  .heart-list,
  .support-text {
    font-size: 15px;
  }

  .support-frame {
    padding: 18px 18px 22px 20px;
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
