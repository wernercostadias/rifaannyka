export default defineNuxtConfig({
  compatibilityDate: '2026-06-04',
  css: ['~/assets/css/main.css'],
  nitro: {
    preset: 'cloudflare',
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000/api/v1',
      mercadoPagoPublicKey: process.env.MERCADOPAGO_PUBLIC_KEY || '',
    },
  },
  modules: ['@nuxtjs/google-fonts'],
  googleFonts: {
    families: {
      'Cormorant Garamond': [700],
      Inter: [400, 500, 600, 700],
      Parisienne: [400],
    },
  },
})
