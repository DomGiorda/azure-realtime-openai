import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
    base: "/",
    plugins: [react()],
    build: {
        outDir: "./dist",
        emptyOutDir: true,
        sourcemap: true
    },
    preview: {
        port: 3000,
        strictPort: true
    },
    resolve: {
        preserveSymlinks: true,
        alias: {
            "@": path.resolve(__dirname, "./src")
        }
    },
    server: {
        port: 3000,
        strictPort: true,
        host: true,
        origin: "http://0.0.0.0:3000",
        proxy: {
            "/realtime": {
                target: "ws://localhost:8765",
                ws: true,
                rewriteWsOrigin: true
            }
        }
    }
});
