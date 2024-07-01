import { create } from 'zustand';
import { createJSONStorage, devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';
import { authActions } from './authActions';

const initialState = {
    user: null,
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false,
    error: null,
    showModal: false,
    modalMessage: '',
};

const useAuthStore = create(
    devtools(
        immer(
            persist(
                (set, get) => ({
                    ...initialState,
                    ...authActions(set, get),
                }),
                {
                    name: 'auth-storage', // 스토리지에 저장될 이름
                    storage: createJSONStorage(() => localStorage), // 스토리지 설정
                },
            ),
        ),
    ),
);

export default useAuthStore;
