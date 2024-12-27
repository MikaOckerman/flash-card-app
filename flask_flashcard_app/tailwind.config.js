/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
    "./app/**/*.py",
    "./blueprints/**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        background: 'hsl(180, 10%, 15%)', // Dark muted green-grey
        primary: 'hsl(180, 60%, 40%)',   // Stronger green
        secondary: 'hsl(180, 30%, 30%)', // Muted teal
        accent: 'hsl(50, 93%, 23%)',     // Golden yellow for accents
        light: 'hsl(0, 0%, 87%)',     // Light grey for text or highlights
        'charcoal-green': 'hsl(165, 40%, 13%)',
      },
    },
  },
  plugins: [],
}

