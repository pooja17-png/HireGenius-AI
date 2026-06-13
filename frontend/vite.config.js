import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The FastAPI backend runs on http://127.0.0.1:8000.
// We proxy /api -> backend so the frontend can use same-origin calls in dev.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
