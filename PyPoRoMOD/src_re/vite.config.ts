// vite.config.ts
import { defineConfig } from "vite";
import dts from "vite-plugin-dts";

export default defineConfig({
    plugins: [
        dts({
            insertTypesEntry: true,
        }),
    ],
    build: {
        lib: {
            entry: "src/main.ts", // Adjust to your main TypeScript file
            name: "MyLibrary", // Global variable name for your library
            fileName: (format) => `my-library.${format}.js`,
        },
        rollupOptions: {
            output: {
                format: "iife", // Immediately Invoked Function Expression for single file
                entryFileNames: "bundle.js",
                extend: true,
            },
        },
        minify: false, // Disable minification to preserve names
        sourcemap: true,
    },
});
