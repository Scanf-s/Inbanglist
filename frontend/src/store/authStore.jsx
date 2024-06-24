import create from 'zustand';
import axios from '../api/axios';

const useAuthStore = create((set) => ({
    auth: {},
    login: async (email, password) => {
        try {
            const response = await axios.post('/login', { email, password });
            const { accessToken, refreshToken } = response.data;

            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('refreshToken', refreshToken);
            axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

            set({ auth: { token: accessToken } });
        } catch (error) {
            console.error('로그인 실패:', error);
            alert('로그인에 실패했습니다. 다시 시도해주세요.');
        }
    },
    logout: () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        delete axios.defaults.headers.common['Authorization'];
        set({ auth: {} });
    },
    initializeAuth: () => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            set({ auth: { token } });
        }
    },
    register: async (name, email, password) => {
        try {
            const response = await axios.post('/register', { name, email, password });
            alert('회원가입에 성공했습니다. 로그인 페이지로 이동합니다.');
        } catch (error) {
            console.error('회원가입 실패:', error);
            alert('회원가입에 실패했습니다. 다시 시도해주세요.');
        }
    }
}));

export default useAuthStore;
