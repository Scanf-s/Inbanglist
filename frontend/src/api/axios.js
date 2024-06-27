import axios from 'axios';

const instance = axios.create({
    // baseURL: 'https://www.inbanglist.com/',
    baseURL: 'http://localhost:8000/',
    headers: {
        'Content-Type': 'application/json',
    },
});

// 요청 인터셉터 추가하여 JWT 토큰을 헤더에 포함
instance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default instance;
