import { create } from 'zustand';
import axios from '../api/axios';

const useAuthStore = create((set) => ({
    user: null,
    accessToken: localStorage.getItem('accessToken'),
    refreshToken: localStorage.getItem('refreshToken'),
    isAuthenticated: !!localStorage.getItem('accessToken'),
    error: null,
    showModal: false,
    modalMessage: '',

    setError: (error) => {
        console.log('Setting error:', error); // 디버깅 로깅
        set({ error, showModal: true, modalMessage: error });
    },

    clearError: () => set({ error: null, showModal: false, modalMessage: '' }),

    saveTokens: (access, refresh) => {
        console.log('Saving tokens'); // 디버깅 로깅
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);
        set({
            accessToken: access,
            refreshToken: refresh,
            isAuthenticated: true,
        });
    },

    clearTokens: () => {
        console.log('Clearing tokens'); // 디버깅 로깅
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        set({
            accessToken: null,
            refreshToken: null,
            isAuthenticated: false,
        });
    },

    setUser: (user) => set({ user }),

    login: async (email, password, onSuccess, onError) => {
        try {
            console.log('Attempting login'); // 디버깅 로깅
            const response = await axios.post('/api/users/login/', {
                email,
                password,
            });
            console.log('Login successful'); // 디버깅 로깅
            // const { access, refresh } = response.data;
            // useAuthStore.getState().saveTokens(access, refresh);
            onSuccess();
        } catch (error) {
            console.error('Login error:', error);
            const errorMessage = '로그인에 실패하였습니다. 이메일과 비밀번호를 확인하세요.';
            useAuthStore.getState().setError(errorMessage);
            onError(errorMessage);
        }
    },

    activateAccount: async (token) => {
        try {
            console.log('Activating account'); // 디버깅 로깅
            const response = await axios.get(`/api/users/activate/${token}`);
            console.log('Activation successful:', response.data); // 디버깅 로깅
            const {
                jwt_tokens: { access, refresh },
            } = response.data;
            set((state) => state.saveTokens(access, refresh));
            set((state) => state.setError('이메일 인증에 성공하였습니다! 로그인 페이지로 이동합니다...'));
        } catch (error) {
            console.error('Activation error:', error);
            set((state) => state.setError('이메일 인증에 실패하였습니다. 다시 시도하세요.'));
        }
    },

    signUp: async (email, password, passwordVerify, onSuccess, onError) => {
        try {
            console.log('Attempting sign up'); // 디버깅 로깅
            await axios.post('/api/users/register/', {
                email,
                password,
                password_verify: passwordVerify,
            });
            console.log('Sign up successful'); // 디버깅 로깅
            onSuccess();
        } catch (error) {
            console.error('Sign up error:', error);
            const errorMessage = '회원가입에 실패하였습니다.';
            useAuthStore.getState().setError(errorMessage);
            onError(errorMessage);
        }
    },
    // refreshAccessToken: async () => {},
    // deleteAccount: async (token) => {},
}));

export default useAuthStore;
