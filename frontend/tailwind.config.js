/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Main colors from Figma design
        text: '#FFFFFF',
        background: '#0C0E16',
        card: '#1A1B23',
        border: '#2E2F3E',
        muted: '#898CA9',
        
        // Gradient colors
        primary: {
          from: '#18C8FF',
          to: '#933FFE',
          DEFAULT: '#933FFE',
        },
        
        // Accent colors
        accent: '#B982FF',
        
        // Semantic colors
        success: '#2DE100',
        warning: '#FFB800',
        error: '#F03738',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(90deg, #18C8FF 0%, #933FFE 100%)',
      },
    },
  },
  plugins: [],
} 