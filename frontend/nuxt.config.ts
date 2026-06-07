export default defineNuxtConfig({
  compatibilityDate: '2026-06-04',
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      title: 'Rifa Estudantil da Annyka',
      meta: [
        {
          name: 'description',
          content:
            'Participe da Rifa Estudantil da Annyka e ajude uma estudante dedicada a conquistar um notebook para seguir evoluindo nos estudos e no estágio.',
        },
        { name: 'theme-color', content: '#17345F' },
        { property: 'og:type', content: 'website' },
        { property: 'og:title', content: 'Rifa Estudantil da Annyka' },
        {
          property: 'og:description',
          content:
            'Sua ajuda faz toda a diferença. Contribua com a Rifa Estudantil da Annyka e apoie essa nova etapa de estudos.',
        },
        { property: 'og:image', content: '/images/capaannyka.jpeg' },
        { property: 'og:locale', content: 'pt_BR' },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'Rifa Estudantil da Annyka' },
        {
          name: 'twitter:description',
          content:
            'Contribua com a Rifa Estudantil da Annyka e ajude na conquista de um notebook para os estudos.',
        },
        { name: 'twitter:image', content: '/images/capaannyka.jpeg' },
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
        { rel: 'shortcut icon', href: '/favicon.svg' },
      ],
    },
  },
  nitro: {
    preset: 'cloudflare',
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000/api/v1',
      mercadoPagoPublicKey: process.env.NUXT_PUBLIC_MERCADOPAGO_PUBLIC_KEY || process.env.MERCADOPAGO_PUBLIC_KEY || '',
      enablePaymentSimulation: process.env.NUXT_PUBLIC_ENABLE_PAYMENT_SIMULATION === 'true',
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
