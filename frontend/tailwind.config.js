module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563eb',
          50: '#f3f7ff',
          100: '#e6efff',
          200: '#bfe0ff',
          600: '#1d4ed8'
        },
        brand: {
          DEFAULT: '#0ea5a4'
        }
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'Segoe UI', 'Roboto', 'Helvetica', 'Arial'],
      },
      boxShadow: {
        'card-lg': '0 8px 30px rgba(2,6,23,0.08)'
      },
      borderRadius: {
        'lg-2': '14px'
      }
    },
  },
  plugins: [],
}
