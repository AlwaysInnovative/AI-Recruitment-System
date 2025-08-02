module.exports = {
  plugins: {
    '@tailwindcss/postcss': {
      tailwindcss: { config: './tailwind.config.cjs' }
    },
    autoprefixer: {}
  }
}
