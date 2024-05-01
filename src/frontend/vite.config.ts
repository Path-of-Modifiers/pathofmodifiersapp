// vite.config.ts
import { defineConfig } from "vite";
import { TanStackRouterVite } from "@tanstack/router-vite-plugin";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    proxy: {
      "/api": {
        target: "http://localhost/api",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""), // It removes the /api from the request address, so it will truly be used only for differentiation
      },
    },
  },
  plugins: [
    // ...,
    TanStackRouterVite(),
  ],
});
