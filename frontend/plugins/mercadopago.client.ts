declare global {
  interface Window {
    MercadoPago?: new (publicKey: string, options?: Record<string, unknown>) => unknown
  }
}

export default defineNuxtPlugin(async () => {
  const config = useRuntimeConfig()
  const publicKey = config.public.mercadoPagoPublicKey

  async function loadScript() {
    if (window.MercadoPago) {
      return
    }

    await new Promise<void>((resolve, reject) => {
      const existing = document.querySelector('script[data-mercadopago-sdk="true"]')
      if (existing) {
        existing.addEventListener('load', () => resolve(), { once: true })
        existing.addEventListener('error', () => reject(new Error('Falha ao carregar MercadoPago.js')), { once: true })
        return
      }

      const script = document.createElement('script')
      script.src = 'https://sdk.mercadopago.com/js/v2'
      script.async = true
      script.dataset.mercadopagoSdk = 'true'
      script.onload = () => resolve()
      script.onerror = () => reject(new Error('Falha ao carregar MercadoPago.js'))
      document.head.appendChild(script)
    })
  }

  let instance: unknown = null
  let loadError: string | null = null

  if (publicKey) {
    try {
      await loadScript()
      if (window.MercadoPago) {
        instance = new window.MercadoPago(publicKey)
      }
    } catch (error) {
      loadError = error instanceof Error ? error.message : 'Falha ao carregar MercadoPago.js'
    }
  }

  return {
    provide: {
      mercadoPago: instance,
      mercadoPagoPublicKey: publicKey,
      mercadoPagoLoadError: loadError,
    },
  }
})
