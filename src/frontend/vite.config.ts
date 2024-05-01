// vite.config.ts
import { defineConfig } from "vite";
import { TanStackRouterVite } from "@tanstack/router-vite-plugin";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    proxy: {
      "/": {
        target: "http://localhost/",
      },
    },
  },
  plugins: [
    // ...,
    TanStackRouterVite(),
  ],
});