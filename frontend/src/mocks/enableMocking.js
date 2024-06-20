export const enableMocking = async () => {
    if (!import.meta.env.DEV) return;

    const { worker } = await import('./browser');
    return worker.start({
        serviceWorker: {
            url: '/mockServiceWorker.js',
        },
        quiet: true,
    });
};
