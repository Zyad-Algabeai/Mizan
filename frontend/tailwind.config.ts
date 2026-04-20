import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./contexts/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Base dark canvas — same tokens work for both markets
        bg: {
          DEFAULT: "#0a0a0b",
          elev: "#111113",
          card: "#16161a",
          border: "#1f1f24",
        },
        fg: {
          DEFAULT: "#e7e7ea",
          muted: "#8a8a94",
          dim: "#555560",
        },
        // Theme accents (referenced via CSS variables at runtime)
        tasi: {
          DEFAULT: "#00D4AA",
          soft: "rgba(0, 212, 170, 0.12)",
          glow: "rgba(0, 212, 170, 0.35)",
        },
        us: {
          DEFAULT: "#FF6B35",
          soft: "rgba(255, 107, 53, 0.12)",
          glow: "rgba(255, 107, 53, 0.35)",
        },
        success: "#00D4AA",
        danger: "#FF4444",
        warn: "#F59E0B",
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "monospace"],
        arabic: ["var(--font-arabic)", "Noto Naskh Arabic", "serif"],
      },
      boxShadow: {
        card: "0 1px 0 rgba(255,255,255,0.03) inset, 0 8px 24px rgba(0,0,0,0.25)",
        glow: "0 0 0 1px var(--accent), 0 0 24px var(--accent-glow)",
      },
      borderRadius: {
        xl: "14px",
        "2xl": "20px",
      },
    },
  },
  plugins: [],
};

export default config;
