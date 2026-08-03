/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        brand: {
          dark: '#030712',
          panel: '#0B1329',
          accent: '#3B82F6',
          cyber: '#1E40AF',
        }
      }
    },
  },
  plugins: [],
}
