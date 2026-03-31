/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
      "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
      "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
      extend: {
        colors: {
          brand: {
            50: "#f0f7ff",
            100: "#dfeeff",
            200: "#b8dbff",
            300: "#78bfff",
            400: "#3a9eff",
            500: "#0a7aff",
            600: "#005fdb",
            700: "#004bb3",
            800: "#003d8f",
            900: "#003375",
          },
          surface: {
            primary: "#0a0a0f",
            secondary: "#12121a",
            tertiary: "#1a1a26",
            elevated: "#222233",
          },
          text: {
            primary: "#f0f0f5",
            secondary: "#9595a8",
            muted: "#5e5e72",
          },
        },
        fontFamily: {
          display: ['"DM Sans"', "sans-serif"],
          body: ['"IBM Plex Sans"', "sans-serif"],
          mono: ['"JetBrains Mono"', "monospace"],
        },
        animation: {
          "fade-in": "fadeIn 0.4s ease-out",
          "slide-up": "slideUp 0.4s ease-out",
          "pulse-dot": "pulseDot 1.4s infinite ease-in-out",
        },
        keyframes: {
          fadeIn: {
            "0%": { opacity: "0" },
            "100%": { opacity: "1" },
          },
          slideUp: {
            "0%": { opacity: "0", transform: "translateY(12px)" },
            "100%": { opacity: "1", transform: "translateY(0)" },
          },
          pulseDot: {
            "0%, 80%, 100%": { transform: "scale(0.4)", opacity: "0.4" },
            "40%": { transform: "scale(1)", opacity: "1" },
          },
        },
      },
    },
    plugins: [],
  };