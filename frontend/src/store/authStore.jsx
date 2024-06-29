import { create } from 'zustand';
import axios from '../api/axios';

const useAuthStore = create((set) => ({
    user: null,
    accessToken: localStorage.getItem('accessToken'),
    refreshToken: localStorage.getItem('refreshToken'),
    isAuthenticated: false,
    error: null,
    showModal: false,
    modalMessage: '',
    setUser: (user) => set({ user }),
    setIsAuthenticated: (isAuthenticated) => set({ isAuthenticated }),

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

    logout: () => {
        console.log('Logging out'); // 디버깅 로깅
        useAuthStore.getState().clearTokens();
        useAuthStore.getState().setUser(null); // 로그아웃 시 유저 정보 삭제
        set({ error: null });
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

    login: async (email, password, onSuccess) => {
        try {
            console.log('Attempting login'); // 디버깅 로깅
            // useAuthStore.getState().requestToken(email, password);
            const response = await axios.post('/api/users/login', {
                email,
                password,
            });
            console.log('Login successful'); // 디버깅 로깅
            useAuthStore.getState().setIsAuthenticated(true)    
            const { access, refresh } = response.data.jwt_tokens;
            useAuthStore.getState().saveTokens(access, refresh);
            useAuthStore.getState().setUser({ email: response.data.email, name:response.data.name})
            onSuccess();
        } catch (error) {
            console.error('Login error:', error);
            const errorMessage = '로그인에 실패하였습니다. 이메일과 비밀번호를 확인하세요.';
            useAuthStore.getState().setError(errorMessage);
        }
    },

    signUp: async (name, email, password, onSuccess, onError) => {
        try {
            console.log('Attempting sign up'); // 디버깅 로깅
            await axios.post('/api/users/register', {
                username: name,
                email,
                password,
            });
            console.log('Sign up successful'); // 디버깅 로깅
            onSuccess();
        } catch (error) {
            console.error('Sign up error:', error);
            if(error.response.status === 400) {
                useAuthStore.getState().setError('이미 가입된 메일입니다.');
            } else {
                useAuthStore.getState().setError('회원가입에 실패하였습니다.');
            }
            onError(errorMessage);
        }
    },

}));

export default useAuthStore;
