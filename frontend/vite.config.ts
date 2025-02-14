import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  envDir: "./environments",
  // // FOR DOCKER ENABLE BELOW
  // server: {
  //   host: '0.0.0.0',
  //   port: 5173,
  // }
});
