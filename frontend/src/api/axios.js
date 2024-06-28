import axios from 'axios';

const instance = axios.create({
    baseURL: 'https://www.inbanglist.com/',
    // baseURL: 'http://localhost:8000/',
    headers: {
        'Content-Type': 'application/json',
    },
});

// 요청 인터셉터 추가하여 JWT 토큰을 헤더에 포함
// instance.interceptors.request.use(
//     (config) => {
//         // 로그인 요청에서는 Authorization 헤더를 추가하지 않음
//         if (!config.url.includes('/api/users/login/')) {
//             const token = localStorage.getItem('accessToken');
//             if (token) {
//                 config.headers['Authorization'] = `Bearer ${token}`;
//             }
//         }
//         return config;
//     },
//     (error) => {
//         return Promise.reject(error);
//     },
// );

// 응답 인터셉터 추가하여 토큰 갱신
// instance.interceptors.response.use(
//     (response) => {
//         return response;
//     },
//     async (error) => {
//         const originalRequest = error.config;
//         if (error.response.status === 401 && !originalRequest._retry) {
//             originalRequest._retry = true;
//             try {
//                 await useAuthStore.getState().refreshAccessToken();
//                 originalRequest.headers['Authorization'] = `Bearer ${localStorage.getItem('accessToken')}`;
//                 return instance(originalRequest);
//             } catch (err) {
//                 return Promise.reject(err);
//             }
//         }
//         return Promise.reject(error);
//     },
// );

export default instance;
