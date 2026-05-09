/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class', // Enable class-based dark mode
  content: [
    "./app/components/**/*.{js,vue,ts}",
    "./app/layouts/**/*.vue",
    "./app/pages/**/*.vue",
    "./app/plugins/**/*.{js,ts}",
    "./app/app.vue",
  ],
  theme: {
    extend: {
      colors: {
        neon: '#00ffff',
        // Theme colors backed by CSS variables so they flip with the .dark class
        'theme-bg': 'var(--bg)',
        'theme-text': 'var(--text)',
      },
    },
  },
  plugins: [],
}