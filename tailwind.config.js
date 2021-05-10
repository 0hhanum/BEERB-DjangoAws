module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      spacing: {
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh"
      },
      boxShadow: {
        "y-md": "0 4px 6px -1px rgba(253, 184, 30, 0.1), 0 2px 4px -1px rgba(253, 184, 30, 0.06)",
        "y-lg": "4px 8px 15px 3px rgba(253, 184, 30, 0.3), 0 6px 4px -2px rgba(253, 184, 30, 0.15)",
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
