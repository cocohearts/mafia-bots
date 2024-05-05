import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapter(),
    alias: {
      '@/*': './src/lib',
    },
    csrf: { checkOrigin: false },
  },
  preprocess: vitePreprocess(),
};
export default config;
