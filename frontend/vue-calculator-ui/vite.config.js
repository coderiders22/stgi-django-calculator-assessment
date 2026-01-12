import { fileURLToPath, URL } from 'node:url'
import { defineConfig, loadEnv } from 'vite' 
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig(({ mode }) => {   

  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [
      vue(),
      vueDevTools(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    server: {
      host: '127.0.0.1',
      port: 5173,
      proxy: {
        '/api': {
          target: env.VITE_API_URL,   
          changeOrigin: true,
          secure: true,
          ws: true,



          configure: (proxy, _options) => {
            proxy.on('proxyReq', (proxyReq, req, _res) => {
              console.log('[Proxy →]', req.method, req.url)
            })
            proxy.on('proxyRes', (proxyRes, req, _res) => {
              console.log('[Proxy ←]', proxyRes.statusCode, req.method, req.url)
            })
            proxy.on('error', (err, req, _res) => {
              console.error('[Proxy Error]', err.message, '→', req.url)
            })
          }
        }
      }
    }
  }
})