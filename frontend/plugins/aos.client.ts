import AOS from 'aos'

export default defineNuxtPlugin(() => {
  AOS.init({
    duration: 700,
    easing: 'ease-out-cubic',
    once: true,
    offset: 80,
    mirror: false,
  })
})
