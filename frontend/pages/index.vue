<template>
  <div class="container page">
    <RaffleHero :raffle="raffle" @choose="scrollToNumbers" />

    <NumbersSection
      ref="numbersSection"
      :raffle="raffle"
      :pending="pending"
      :error-message="errorMessage"
      :visible-numbers="visibleNumbers"
      :selected-numbers="selectedNumbers"
      :show-load-more="showLoadMore"
      :total-amount="totalAmount"
      @toggle-number="toggleNumber"
      @show-more="showMoreNumbers"
      @open-buyer-modal="buyerModalOpen = true"
    />

    <InfoCardsSection />

    <LatestPurchasesSection
      :latest-purchases="visibleLatestPurchases"
      :show-load-more="showMoreLatestPurchases"
      @show-more="loadMoreLatestPurchases"
    />

    <PurchaseLookupModal
      :open="lookupModalOpen"
      :search-type="lookupSearchType"
      :query="lookupQuery"
      :error="lookupError"
      :loading="lookupLoading"
      :can-lookup="canLookup"
      :searched="lookupSearched"
      :results="lookupResults"
      :format-numbers="formatNumbers"
      :format-purchase-date="formatPurchaseDate"
      @close="lookupModalOpen = false"
      @submit="lookupPurchases"
      @update:search-type="updateLookupSearchType"
      @update:query="updateLookupQuery"
    />

    <BuyerDetailsModal
      :open="buyerModalOpen"
      :buyer="buyer"
      :errors="buyerErrors"
      :selected-numbers="selectedNumbers"
      :total-amount="totalAmount"
      :can-submit="canSubmit"
      :submitting="submitting"
      @close="buyerModalOpen = false"
      @submit="submitPurchase"
      @update:full-name="updateBuyerFullName"
      @update:email="updateBuyerEmail"
      @update:phone="updateBuyerPhone"
      @update:cpf="updateBuyerCpf"
    />

    <PaymentModal
      :open="paymentModalOpen"
      :mercado-pago-ready="mercadoPagoReady"
      :mercado-pago-error-message="mercadoPagoErrorMessage"
      :purchase="purchase"
      :payment="payment"
      :payment-confirmed="paymentConfirmed"
      :payment-expired="paymentExpired"
      :payment-summary-text="paymentSummaryText"
      :payment-status-message="paymentStatusMessage"
      :payment-simulation-enabled="paymentSimulationEnabled"
      :simulating-payment="simulatingPayment"
      :full-buyer-name="fullBuyerName"
      :reservation-deadline-label="reservationDeadlineLabel"
      :payment-pending-hint="paymentPendingHint"
      :format-numbers="formatNumbers"
      @close="paymentModalOpen = false"
      @copy-pix="copyPix"
      @simulate-payment="simulatePayment"
    />
  </div>
</template>

<script setup lang="ts">
import confetti from 'canvas-confetti'

import BuyerDetailsModal from '~/components/home/BuyerDetailsModal.vue'
import InfoCardsSection from '~/components/home/InfoCardsSection.vue'
import LatestPurchasesSection from '~/components/home/LatestPurchasesSection.vue'
import NumbersSection from '~/components/home/NumbersSection.vue'
import PaymentModal from '~/components/home/PaymentModal.vue'
import PurchaseLookupModal from '~/components/home/PurchaseLookupModal.vue'
import type {
  BuyerFormData,
  BuyerFormErrors,
  LookupPurchase,
  PaymentResponse,
  PublicPurchase,
  PurchaseResponse,
  Raffle,
  RaffleNumber,
} from '~/types/raffle'

const api = useApi()
const { $mercadoPago, $mercadoPagoPublicKey, $mercadoPagoLoadError, $mercadoPagoDeviceId } = useNuxtApp()
const runtimeConfig = useRuntimeConfig()
const numbersSection = ref<{ sectionEl: HTMLElement | null } | null>(null)
const raffle = ref<Raffle | null>(null)
const numbers = ref<RaffleNumber[]>([])
const latestPurchases = ref<PublicPurchase[]>([])
const selectedNumbers = ref<number[]>([])
const pending = ref(true)
const submitting = ref(false)
const simulatingPayment = ref(false)
const errorMessage = ref('')
const purchase = ref<PurchaseResponse | null>(null)
const payment = ref<PaymentResponse | null>(null)
const buyerModalOpen = ref(false)
const paymentModalOpen = ref(false)
const lookupModalOpen = ref(false)
const isMobileNumbers = ref(false)
const visibleNumberCount = ref(Number.POSITIVE_INFINITY)
const lookupSearchType = ref<'name' | 'cpf'>('name')
const lookupQuery = ref('')
const lookupLoading = ref(false)
const lookupError = ref('')
const lookupSearched = ref(false)
const lookupResults = ref<LookupPurchase[]>([])
const celebratedPaymentId = ref<number | null>(null)
const DESKTOP_INITIAL_NUMBERS = 70
const DESKTOP_LOAD_STEP = 70
const MOBILE_INITIAL_NUMBERS = 50
const MOBILE_LOAD_STEP = 50
const INITIAL_LATEST_PURCHASES = 10
const LOAD_MORE_LATEST_PURCHASES = 10
const visibleLatestPurchasesCount = ref(INITIAL_LATEST_PURCHASES)

const buyer = reactive<BuyerFormData>({
  full_name: '',
  email: '',
  phone: '',
  cpf: '',
})

const totalAmount = computed(() => {
  const price = Number(raffle.value?.price_per_number || 0)
  return (price * selectedNumbers.value.length).toFixed(2).replace('.', ',')
})

const orderedNumbers = computed(() => {
  const priorityByStatus: Record<string, number> = {
    available: 0,
    reserved: 1,
    paid: 2,
    canceled: 3,
  }

  return [...numbers.value].sort((left, right) => {
    const leftPriority = priorityByStatus[left.status] ?? 99
    const rightPriority = priorityByStatus[right.status] ?? 99

    if (leftPriority !== rightPriority) {
      return leftPriority - rightPriority
    }

    return left.number - right.number
  })
})

const visibleLatestPurchases = computed(() => latestPurchases.value.slice(0, visibleLatestPurchasesCount.value))

const showMoreLatestPurchases = computed(() => latestPurchases.value.length > visibleLatestPurchasesCount.value)

const visibleNumbers = computed(() => orderedNumbers.value.slice(0, visibleNumberCount.value))

const showLoadMore = computed(() => {
  return visibleNumberCount.value < orderedNumbers.value.length
})

const mercadoPagoReady = computed(() => Boolean($mercadoPago && $mercadoPagoPublicKey))
const paymentSimulationEnabled = Boolean(runtimeConfig.public.enablePaymentSimulation)
const mercadoPagoErrorMessage = computed(() => {
  if ($mercadoPagoLoadError) {
    return 'Nao foi possivel carregar o Mercado Pago. Tente novamente em instantes.'
  }
  return 'Mercado Pago.js ainda nao foi inicializado. Verifique a NUXT_PUBLIC_MERCADOPAGO_PUBLIC_KEY no ambiente.'
})
const fullBuyerName = computed(() => {
  if (!purchase.value) {
    return ''
  }

  return `${purchase.value.buyer.first_name} ${purchase.value.buyer.last_name}`.trim()
})
const paymentConfirmed = computed(() => {
  return payment.value?.status === 'paid' || purchase.value?.status === 'paid'
})
const paymentExpired = computed(() => {
  return purchase.value?.status === 'expired' || purchase.value?.status === 'canceled'
})
const paymentStatusMessage = computed(() => {
  if (!purchase.value || !payment.value) {
    return 'Preparando pagamento...'
  }
  if (paymentConfirmed.value) {
    return 'Pagamento confirmado. Seus numeros ja estao garantidos.'
  }
  if (paymentExpired.value) {
    return 'Essa reserva expirou. Escolha seus numeros novamente para gerar um novo Pix.'
  }
  return 'Ao pagar aguarde a confirmação do pagamento.'
})
const reservationDeadlineLabel = computed(() => {
  if (!purchase.value?.reservation_expires_at) {
    return ''
  }

  return new Intl.DateTimeFormat('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(purchase.value.reservation_expires_at))
})
const paymentPendingHint = computed(() => {
  if (paymentExpired.value) {
    return 'O prazo terminou e este Pix nao pode mais ser usado.'
  }

  return 'Nao feche esta tela antes de concluir o pagamento, a menos que voce desista da reserva.'
})
const paymentSummaryText = computed(() => {
  if (!purchase.value) {
    return ''
  }

  const buyerName = fullBuyerName.value
  const formattedNumbers = formatNumbers(purchase.value.numbers)

  if (paymentExpired.value) {
    return `A reserva dos numeros ${formattedNumbers} expirou porque o pagamento nao foi concluido a tempo.`
  }

  return `Obrigado, ${buyerName}. Seus numeros ${formattedNumbers} estao reservados aguardando o pagamento.`
})

const canSubmit = computed(() => {
  return (
    selectedNumbers.value.length > 0 &&
    Boolean(buyer.full_name.trim()) &&
    Boolean(buyer.email.trim()) &&
    Boolean(buyer.phone) &&
    Boolean(buyer.cpf) &&
    !buyerErrors.value.full_name &&
    !buyerErrors.value.email &&
    !buyerErrors.value.phone &&
    !buyerErrors.value.cpf &&
    mercadoPagoReady.value
  )
})

const canLookup = computed(() => {
  const query = lookupQuery.value.trim()
  if (lookupSearchType.value === 'cpf') {
    return onlyDigits(query).length === 11
  }
  return query.length >= 3
})

let paymentStatusInterval: ReturnType<typeof setInterval> | null = null

const buyerErrors = computed<BuyerFormErrors>(() => ({
  full_name: validateFullName(buyer.full_name),
  email: validateEmail(buyer.email),
  phone: validatePhone(buyer.phone),
  cpf: validateCpf(buyer.cpf),
}))

onMounted(async () => {
  syncNumberViewport()
  window.addEventListener('resize', syncNumberViewport)
  window.addEventListener('open-purchase-lookup', openPurchaseLookup)
  await loadRaffle()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', syncNumberViewport)
  window.removeEventListener('open-purchase-lookup', openPurchaseLookup)
  stopPaymentStatusPolling()
})

watch(paymentModalOpen, (isOpen) => {
  if (!isOpen) {
    stopPaymentStatusPolling()
    return
  }

  if (payment.value && payment.value.status !== 'paid' && purchase.value?.status === 'reserved') {
    startPaymentStatusPolling()
  }
})

async function loadRaffle() {
  pending.value = true
  try {
    raffle.value = await api('/raffles/active/')
    if (raffle.value) {
      await Promise.all([loadNumbers(), loadLatestPurchases()])
    }
  } catch {
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
  visibleLatestPurchasesCount.value = INITIAL_LATEST_PURCHASES
}

function openPurchaseLookup() {
  lookupSearchType.value = 'name'
  lookupQuery.value = ''
  lookupError.value = ''
  lookupSearched.value = false
  lookupResults.value = []
  lookupModalOpen.value = true
}

function scrollToNumbers() {
  numbersSection.value?.sectionEl?.scrollIntoView({ behavior: 'smooth' })
}

function toggleNumber(number: number) {
  if (selectedNumbers.value.includes(number)) {
    selectedNumbers.value = selectedNumbers.value.filter((item) => item !== number)
    return
  }
  selectedNumbers.value = [...selectedNumbers.value, number].sort((a, b) => a - b)
}

function onlyDigits(value: string) {
  return value.replace(/\D/g, '')
}

function formatPhone(value: string) {
  const digits = onlyDigits(value).slice(0, 11)
  if (digits.length <= 2) {
    return digits.length ? `(${digits}` : ''
  }
  if (digits.length <= 7) {
    return `(${digits.slice(0, 2)}) ${digits.slice(2)}`
  }
  if (digits.length <= 10) {
    return `(${digits.slice(0, 2)}) ${digits.slice(2, 6)}-${digits.slice(6)}`
  }
  return `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`
}

function formatCpf(value: string) {
  const digits = onlyDigits(value).slice(0, 11)
  if (digits.length <= 3) return digits
  if (digits.length <= 6) return `${digits.slice(0, 3)}.${digits.slice(3)}`
  if (digits.length <= 9) return `${digits.slice(0, 3)}.${digits.slice(3, 6)}.${digits.slice(6)}`
  return `${digits.slice(0, 3)}.${digits.slice(3, 6)}.${digits.slice(6, 9)}-${digits.slice(9)}`
}

function validateFullName(value: string) {
  const normalized = value.trim().replace(/\s+/g, ' ')
  if (!normalized) {
    return ''
  }
  const parts = normalized.split(' ')
  if (parts.length < 2) {
    return 'Informe nome e sobrenome.'
  }
  if (parts.some((part) => part.length < 2)) {
    return 'Cada parte do nome deve ter pelo menos 2 letras.'
  }
  return ''
}

function validatePhone(value: string) {
  const digits = onlyDigits(value)
  if (!digits) {
    return ''
  }
  if (digits.length !== 11) {
    return 'Informe um celular com DDD e 11 digitos.'
  }
  if (digits[2] !== '9') {
    return 'Informe um celular valido com nono digito.'
  }
  return ''
}

function validateEmail(value: string) {
  const normalized = value.trim()
  if (!normalized) {
    return ''
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailPattern.test(normalized)) {
    return 'Informe um e-mail valido.'
  }

  return ''
}

function isValidCpfDigits(digits: string) {
  if (digits.length !== 11 || /^(\d)\1{10}$/.test(digits)) {
    return false
  }

  let sum = 0
  for (let index = 0; index < 9; index += 1) {
    sum += Number(digits[index]) * (10 - index)
  }
  let remainder = (sum * 10) % 11
  if (remainder === 10) remainder = 0
  if (remainder !== Number(digits[9])) {
    return false
  }

  sum = 0
  for (let index = 0; index < 10; index += 1) {
    sum += Number(digits[index]) * (11 - index)
  }
  remainder = (sum * 10) % 11
  if (remainder === 10) remainder = 0
  return remainder === Number(digits[10])
}

function validateCpf(value: string) {
  const digits = onlyDigits(value)
  if (!digits) {
    return ''
  }
  if (digits.length !== 11) {
    return 'Informe um CPF com 11 digitos.'
  }
  if (!isValidCpfDigits(digits)) {
    return 'Informe um CPF valido.'
  }
  return ''
}

function updateBuyerFullName(value: string) {
  buyer.full_name = value.replace(/\s+/g, ' ').replace(/^\s+/, '')
}

function updateBuyerEmail(value: string) {
  buyer.email = value.trim()
}

function updateBuyerPhone(value: string) {
  buyer.phone = formatPhone(value)
}

function updateBuyerCpf(value: string) {
  buyer.cpf = formatCpf(value)
}

function updateLookupSearchType(value: 'name' | 'cpf') {
  lookupSearchType.value = value
  lookupQuery.value = ''
  lookupError.value = ''
  lookupSearched.value = false
  lookupResults.value = []
}

function updateLookupQuery(value: string) {
  lookupQuery.value = lookupSearchType.value === 'cpf' ? formatCpf(value) : value.replace(/\s+/g, ' ').replace(/^\s+/, '')
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
          email: buyer.email,
          phone: buyer.phone,
          cpf: buyer.cpf,
        },
        numbers: selectedNumbers.value,
        payment_provider: 'mercadopago',
        device_id: $mercadoPagoDeviceId || '',
      },
    })
    purchase.value = response.purchase
    payment.value = response.payment
    buyerModalOpen.value = false
    paymentModalOpen.value = true
    await Promise.all([loadNumbers(), loadLatestPurchases()])
    selectedNumbers.value = []
    startPaymentStatusPolling()
  } catch {
    errorMessage.value = 'Nao foi possivel iniciar o pagamento. Nenhum numero foi reservado.'
  } finally {
    submitting.value = false
  }
}

async function copyPix() {
  if (payment.value?.qr_code_text) {
    await navigator.clipboard.writeText(payment.value.qr_code_text)
  }
}

async function refreshPaymentStatus() {
  if (!payment.value || !purchase.value) {
    return
  }

  const response = await api(`/payments/${payment.value.id}/status/`, {
    query: {
      purchase_reference: purchase.value.reference,
    },
  })
  payment.value = response.payment
  purchase.value = response.purchase

  if (paymentConfirmed.value) {
    celebratePaymentSuccess()
    stopPaymentStatusPolling()
    await Promise.all([loadNumbers(), loadLatestPurchases()])
    return
  }

  if (paymentExpired.value) {
    stopPaymentStatusPolling()
    await Promise.all([loadNumbers(), loadLatestPurchases()])
  }
}

function startPaymentStatusPolling() {
  stopPaymentStatusPolling()
  paymentStatusInterval = setInterval(() => {
    refreshPaymentStatus().catch(() => {})
  }, 5000)
}

function stopPaymentStatusPolling() {
  if (paymentStatusInterval) {
    clearInterval(paymentStatusInterval)
    paymentStatusInterval = null
  }
}

async function simulatePayment() {
  if (!payment.value || paymentExpired.value) {
    return
  }

  simulatingPayment.value = true
  try {
    payment.value = await api(`/payments/${payment.value.id}/confirm-local/`, {
      method: 'POST',
    })
    await refreshPaymentStatus()
  } finally {
    simulatingPayment.value = false
  }
}

function celebratePaymentSuccess() {
  if (!payment.value || celebratedPaymentId.value === payment.value.id || !import.meta.client) {
    return
  }

  celebratedPaymentId.value = payment.value.id

  const defaults = {
    spread: 70,
    ticks: 220,
    gravity: 0.9,
    startVelocity: 40,
    scalar: 1,
    colors: ['#17345f', '#2aa39f', '#ef78a5', '#f3d57d'],
  }

  confetti({
    ...defaults,
    particleCount: 140,
    origin: { x: 0.18, y: 0.35 },
    angle: 60,
  })

  confetti({
    ...defaults,
    particleCount: 140,
    origin: { x: 0.82, y: 0.35 },
    angle: 120,
  })

  window.setTimeout(() => {
    confetti({
      ...defaults,
      particleCount: 110,
      spread: 110,
      startVelocity: 32,
      origin: { x: 0.5, y: 0.28 },
    })
  }, 220)
}

async function lookupPurchases() {
  if (!raffle.value) {
    return
  }

  const query = lookupQuery.value.trim()
  if (lookupSearchType.value === 'name' && query.length < 3) {
    lookupError.value = 'Informe pelo menos 3 letras do nome.'
    lookupResults.value = []
    lookupSearched.value = false
    return
  }

  if (lookupSearchType.value === 'cpf') {
    const cpfError = validateCpf(query)
    if (cpfError) {
      lookupError.value = cpfError
      lookupResults.value = []
      lookupSearched.value = false
      return
    }
  }

  if (!query) {
    lookupError.value = 'Informe os dados para buscar seus números.'
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
    visibleNumberCount.value = Math.min(targetInitialCount, orderedNumbers.value.length || targetInitialCount)
  }
}

function showMoreNumbers() {
  const step = isMobileNumbers.value ? MOBILE_LOAD_STEP : DESKTOP_LOAD_STEP
  visibleNumberCount.value = Math.min(visibleNumberCount.value + step, orderedNumbers.value.length)
}

function loadMoreLatestPurchases() {
  visibleLatestPurchasesCount.value = Math.min(
    visibleLatestPurchasesCount.value + LOAD_MORE_LATEST_PURCHASES,
    latestPurchases.value.length,
  )
}
</script>

<style scoped>
.page {
  padding-bottom: 48px;
}

@media (max-width: 560px) {
  .page {
    padding-bottom: 34px;
  }
}
</style>
