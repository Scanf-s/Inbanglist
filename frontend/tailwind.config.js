/** @type {import('tailwindcss').Config} */
export default {
    content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
    theme: {
        container: {
            padding: 0,
            margin: 0,
        },
        extend: {
            animation: {
                'ping-slow': 'ping 1.5s linear infinite',
                'spin-slow': 'spin 2s linear infinite',
            },
            fontFamily: {
                sans: ['Poppins', 'ui-sans-serif', 'system-ui'],
            },
        },
        important: true,
    },
    darkMode: 'class',
    plugins: [],
};
