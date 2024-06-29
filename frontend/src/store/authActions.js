import axios from '../api/axios';
import Cookies from 'js-cookie';

export const authActions = (set, get) => ({
    setUser: (user) =>
        set((state) => {
            state.user = user;
        }),
    setIsAuthenticated: (isAuthenticated) =>
        set((state) => {
            state.isAuthenticated = isAuthenticated;
        }),

    setError: (error) => {
        console.log('Setting error:', error); // 디버깅 로깅
        set((state) => {
            state.error = error;
            state.showModal = true;
            state.modalMessage = error;
        });
    },
    clearError: () =>
        set((state) => {
            state.error = null;
            state.showModal = false;
            state.modalMessage = '';
        }),

    saveTokens: (access, refresh) => {
        console.log('Saving tokens'); // 디버깅 로깅
        Cookies.set('accessToken', access); // 액세스 토큰을 쿠키에 저장
        Cookies.set('refreshToken', refresh); // 리프레시 토큰을 쿠키에 저장
        set((state) => {
            state.accessToken = access;
            state.refreshToken = refresh;
            state.isAuthenticated = true;
        });
    },

    clearTokens: () => {
        console.log('Clearing tokens'); // 디버깅 로깅
        Cookies.remove('accessToken'); // 액세스 토큰을 쿠키에서 삭제
        Cookies.remove('refreshToken'); // 리프레시 토큰을 쿠키에서 삭제
        set((state) => {
            state.accessToken = null;
            state.refreshToken = null;
            state.isAuthenticated = false;
        });
    },

    logout: () => {
        console.log('Logging out'); // 디버깅 로깅
        get().clearTokens();
        set((state) => {
            state.user = null; // 로그아웃 시 유저 정보 삭제
            state.error = null;
        });
    },

    deleteUser: async (email, password, onSuccess, onError) => {
        try {
            console.log('Attempting delete account.');
            let access = get().accessToken;
            const refresh = get().refreshToken;

            const makeDeleteRequest = async (token) => {
                return await axios.delete('/api/users/delete', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                    data: {
                        email: email,
                        password: password,
                        refresh_token: refresh,
                    },
                });
            };
            try {
                const response = await makeDeleteRequest(access);
                get().clearError();
                console.log('Successful deletion account:', response);
                onSuccess();
            } catch (error) {
                if (error.response && error.response.data && error.response.data.code === 'token_not_valid') {
                    // 토큰이 유효하지 않거나 만료된 경우
                    console.log('Access token is invalid or expired. Refreshing token...');
                    access = await get().refreshAccessToken();
                    // 재발급 받은 토큰으로 다시 시도
                    const response = await makeDeleteRequest(access);
                    set((state) => {
                        state.clearTokens();
                        state.clearError();
                    });
                    console.log('Successful deletion account:', response);
                    onSuccess();
                } else {
                    console.log('Delete account error:', error);
                    get().setError('계정 삭제에 실패했습니다. 다시 시도하세요.');
                }
            }
        } catch (error) {
            console.log('Delete account error:', error);
            set((state) => state.setError('계정 삭제에 실패했습니다. 다시 시도하세요.'));
            onError();
        }
    },

    login: async (email, password, onSuccess) => {
        try {
            console.log('Attempting login'); // 디버깅 로깅
            const response = await axios.post('/api/users/login', {
                email,
                password,
            });
            console.log('Login successful'); // 디버깅 로깅
            const { access, refresh } = response.data.jwt_tokens;
            get().saveTokens(access, refresh);
            set((state) => {
                state.isAuthenticated = true;
                state.user = response.data.user;
            });
            onSuccess();
        } catch (error) {
            console.error('Login error:', error);
            const errorMessage = '로그인에 실패하였습니다. 이메일과 비밀번호를 확인하세요.';
            get().setError(errorMessage);
        }
    },
    // login: async (email, password, onSuccess) => {
    //     try {
    //         const response = await axios.post(
    //             '/api/users/login',
    //             new URLSearchParams({
    //                 username: email,
    //                 password: password,
    //             }),
    //             {
    //                 headers: {
    //                     'Content-Type': 'application/x-www-form-urlencoded', // Django 기본 로그인 폼 형식
    //                 },
    //                 withCredentials: true, // 쿠키 포함
    //             },
    //         );
    //         onSuccess();
    //     } catch (error) {
    //         console.error('Error during login:', error);
    //     }
    // },

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
            if (error.response.status === 400) {
                get().setError('이미 가입된 메일입니다.');
            } else {
                get().setError('회원가입에 실패하였습니다.');
            }
            onError(errorMessage);
        }
    },

    navigateToAdminDocs: () => {
        const token = get().accessToken;
        if (token) {
            const url = '/api/v1/docs';
            window.open(url, '_self', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
        } else {
            console.error('Access token is missing.');
        }
    },
    refreshAccessToken: async () => {
        const refresh = get().refreshToken;
        try {
            console.log('Refreshing access token'); // 디버깅 로깅
            const response = await axios.post('/api/token/refresh', {
                refresh: refresh,
            });
            console.log('Access Token refresh successful:', response.data); // 디버깅 로깅
            const { access } = response.data;
            set(() => get().saveTokens(access, refresh));
            return access; // 새로 발급된 액세스 토큰을 반환
        } catch (error) {
            console.error('Token refresh error:', error);
            set(() => get().setError('토큰 갱신에 실패하였습니다. 다시 로그인하세요.'));
            set(() => get().clearTokens());
            throw error;
        }
    },
    fetchUser: async () => {
        const accessToken = get().accessToken;

        try {
            console.log('Attempting fetch user'); // 디버깅 로그
            const response = await axios.get('/api/users/info', {
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                },
            });
            get().setUser(response.data.user);
            console.log('Fetched user data successful:', response);
        } catch (error) {
            console.error('Fetch user error:', error);
            set((state) => state.setError('사용자의 정보를 불러오지 못했습니다.'));
        }
    },
    initializeAuth: async () => {
        const accessToken = Cookies.get('accessToken');
        const refreshToken = Cookies.get('refreshToken');
        if (accessToken && refreshToken) {
            set((state) => {
                state.accessToken = accessToken;
                state.refreshToken = refreshToken;
                state.isAuthenticated = true;
            });
            get().fetchUser();
            console.log('initializeAuth Successful.');
        } else {
            set((state) => {
                state.accessToken = null;
                state.refreshToken = null;
                state.isAuthenticated = false;
            });
            console.log('회원정보가 존재하지 않습니다.');
        }
    },
});
