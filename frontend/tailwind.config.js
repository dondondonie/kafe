/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        coffee: {
          50: '#faf8f3',
          100: '#f5f1e8',
          200: '#e8dcc8',
          300: '#d4bfa8',
          400: '#b8996d',
          500: '#8b7355',
          600: '#6b5747',
          700: '#543d2d',
          800: '#3d2817',
          900: '#2a1810',
        }
      }
    },
  },
  plugins: [],
}
