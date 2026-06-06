declare global {
  interface Window {
    MercadoPago?: new (publicKey: string, options?: Record<string, unknown>) => unknown
    MP_DEVICE_SESSION_ID?: string
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

  async function loadSecurityScript() {
    await new Promise<void>((resolve, reject) => {
      const existing = document.querySelector('script[data-mercadopago-security="true"]')
      if (existing) {
        existing.addEventListener('load', () => resolve(), { once: true })
        existing.addEventListener('error', () => reject(new Error('Falha ao carregar security.js')), { once: true })
        return
      }

      const script = document.createElement('script')
      script.src = 'https://www.mercadopago.com/v2/security.js'
      script.async = true
      script.dataset.mercadopagoSecurity = 'true'
      script.onload = () => resolve()
      script.onerror = () => reject(new Error('Falha ao carregar security.js'))
      document.head.appendChild(script)
    })
  }

  let instance: unknown = null
  let loadError: string | null = null
  let deviceId = ''

  if (publicKey) {
    try {
      await loadSecurityScript()
      await loadScript()
      if (window.MercadoPago) {
        instance = new window.MercadoPago(publicKey)
      }
      deviceId = window.MP_DEVICE_SESSION_ID || ''
    } catch (error) {
      loadError = error instanceof Error ? error.message : 'Falha ao carregar MercadoPago.js'
    }
  }

  return {
    provide: {
      mercadoPago: instance,
      mercadoPagoPublicKey: publicKey,
      mercadoPagoLoadError: loadError,
      mercadoPagoDeviceId: deviceId,
    },
  }
})
