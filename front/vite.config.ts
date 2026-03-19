import { paraglide } from '@inlang/paraglide-js-adapter-sveltekit/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit(), paraglide({ project: './project.inlang', outdir: './src/lib/paraglide' })],

  resolve: {
    conditions: ['browser', 'svelte']
  },

	test: {
		include: ['src/**/*.{test,spec}.{js,ts}'],
		globals: true,
    environment: 'jsdom',
    setupFiles: ['./vitest-setup.ts']
	}
});
