import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: {
          DEFAULT: "#090909",
          secondary: "#111111",
          elevated: "#171717",
        },
        foreground: {
          DEFAULT: "#FFFFFF",
          muted: "#A3A3A3",
        },
        border: {
          DEFAULT: "#292929",
          muted: "#1f1f1f",
        },
        accent: {
          red: "#E53935",
          deep: "#A61B1B",
          soft: "rgba(229, 57, 53, 0.10)",
        },
      },
      fontFamily: {
        sans: ["Inter", "Geist", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
