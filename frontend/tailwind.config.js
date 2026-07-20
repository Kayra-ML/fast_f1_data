/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "background": "#ffffff",
        "surface-container-lowest": "#ffffff",
        "surface-container-high": "#f1f5f9",
        "on-background": "#111827",
        "on-surface": "#1f2937",
        "on-surface-variant": "#6b7280",
        
        "primary": "#FF8700", /* McLaren Papaya Orange */
        "primary-fixed": "#FF9933",
        "on-primary": "#ffffff",
        
        "tertiary": "#10b981", 
        "secondary-fixed": "#3b82f6", 
        
        "error": "#ef4444",
        "error-container": "#fee2e2",
        "on-error": "#ffffff",
        
        "surface-tint": "#FF8700",
        "outline-variant": "#e5e7eb",
        "outline": "#d1d5db",
      },
      borderRadius: {
        "DEFAULT": "0.125rem",
        "lg": "0.25rem",
        "xl": "0.5rem",
        "full": "0.75rem"
      },
      spacing: {
        "gutter": "16px",
        "panel-gap": "1px",
        "margin-desktop": "32px",
        "margin-mobile": "16px",
        "unit": "4px"
      },
      fontFamily: {
        "headline-lg-mobile": ["JetBrains Mono", "monospace"],
        "body-md": ["Inter", "sans-serif"],
        "headline-sm": ["JetBrains Mono", "monospace"],
        "headline-md": ["JetBrains Mono", "monospace"],
        "label-lg": ["JetBrains Mono", "monospace"],
        "label-md": ["JetBrains Mono", "monospace"],
        "headline-lg": ["JetBrains Mono", "monospace"],
        "label-sm": ["JetBrains Mono", "monospace"],
        "display-lg": ["JetBrains Mono", "monospace"],
        "body-sm": ["Inter", "sans-serif"],
        "body-lg": ["Inter", "sans-serif"]
      }
    },
  },
  plugins: [],
}
