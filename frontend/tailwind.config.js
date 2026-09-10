/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        clinical: {
          bg: '#0B132B',
          card: '#1C2541',
          surface: '#1E293B',
          border: '#334155',
          accent: '#3A86FF',
          success: '#10B981',
          warning: '#F59E0B',
          danger: '#EF4444',
          incomplete: '#64748B',
        }
      }
    },
  },
  plugins: [],
}
