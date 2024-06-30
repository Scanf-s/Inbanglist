/** @type {import('tailwindcss').Config} */
export default {
    content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
    theme: {
        container: {
            padding: 0,
            margin: 0,
        },
        extend: {
            fontFamily: {
                sans: ['Poppins', 'ui-sans-serif', 'system-ui'],
            },
            animation: {
                'ping-slow': 'ping 1.5s linear infinite',
                'spin-slow': 'spin 2s linear infinite',
                shimmer: 'shimmer 1.5s infinite linear',
            },
            keyframes: {
                shimmer: {
                    '0%': { backgroundPosition: '-100%' },
                    '100%': { backgroundPosition: '100%' },
                },
                ping: {
                    '75%, 100%': { transform: 'scale(1.5)' },
                },
            },
            backgroundImage: {
                'gradient-custom':
                    'linear-gradient(to right, #D9D9D9 0%, #EDEEF1 50%, #D9D9D9 100%)',
            },
        },
        important: true,
    },
    darkMode: 'class',
    plugins: [],
};
