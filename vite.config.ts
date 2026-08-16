import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'
import { fileURLToPath, URL } from 'node:url'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    VitePWA({
      registerType: 'prompt',
      includeAssets: ['favicons/favicon.ico', 'favicons/favicon.svg', 'icons/apple-touch-icon.png'],
      manifest: {
        name: 'siballe',
        short_name: 'siballe',
        description: 'Memorize core phrases for everyday situations, by target language.',
        start_url: '/',
        scope: '/',
        display: 'standalone',
        background_color: '#ffffff',
        theme_color: '#ffffff',
        icons: [
          { src: '/icons/icon-192.png', sizes: '192x192', type: 'image/png', purpose: 'any' },
          { src: '/icons/icon-512.png', sizes: '512x512', type: 'image/png', purpose: 'any' },
          { src: '/icons/maskable-icon-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' }
        ]
      },
      workbox: {
        // App shell only - phrase content (JSON + audio) is runtime-cached below
        // instead of precached, since the catalog will grow to thousands of
        // situations and most users only ever touch a handful of languages.
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
        runtimeCaching: [
          {
            urlPattern: /\/data\/phrases\/.*\.json$/,
            handler: 'StaleWhileRevalidate',
            options: {
              cacheName: 'phrase-json',
              expiration: { maxEntries: 2000, maxAgeSeconds: 60 * 60 * 24 * 180 },
              cacheableResponse: { statuses: [0, 200] }
            }
          },
          {
            urlPattern: /\/data\/phrases\/.*\.mp3$/,
            handler: 'CacheFirst',
            options: {
              cacheName: 'phrase-audio',
              expiration: { maxEntries: 2000, maxAgeSeconds: 60 * 60 * 24 * 180 },
              cacheableResponse: { statuses: [0, 200] }
            }
          }
        ]
      }
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
