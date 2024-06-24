import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useDarkModeStore = create(
    persist(
        (set, get) => ({
            darkMode: false,
            toggleDarkMode: () =>
                set((state) => {
                    const newDarkMode = !state.darkMode;
                    if (newDarkMode) {
                        document.documentElement.classList.add('dark');
                    } else {
                        document.documentElement.classList.remove('dark');
                    }

                    return { darkMode: newDarkMode };
                }),
            initializeDarkMode: () => {
                const { darkMode } = get();
                if (darkMode) {
                    document.documentElement.classList.add('dark');
                } else {
                    document.documentElement.classList.remove('dark');
                }
            },
        }),
        {
            name: 'theme',
        }
    )
);
