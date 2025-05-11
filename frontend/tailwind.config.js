/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {
      colors: {
        // Main colors from specified scheme
        text: '#ffffff',
        background: '#000000',
        primary: '#bc2424',
        secondary: '#e2e2e2',
        accent: '#bc2424',
        
        // Additional UI colors
        card: '#141414',
        border: '#333333',
        
        // Semantic colors
        success: '#4CAF50',
        warning: '#FFC107',
        error: '#F44336',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
} 