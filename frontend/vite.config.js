import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    // optimizeDeps: {
    //     include: ['msw'],
    // },
    server: {
        proxy: {
            '/api': {
                target: 'https://www.inbanglist.com',
                changeOrigin: true,
                secure: false,
                rewrite: (path) => path.replace(/^\/api/, '/api'), // 여기서 /api 부분을 유지합니다.
            },
        },
    },
});
