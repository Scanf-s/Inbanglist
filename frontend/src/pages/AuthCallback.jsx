import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';

const AuthCallbackPage = () => {
    const navigate = useNavigate();
    const { saveTokens } = useAuthStore();

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        console.log(urlParams);
        const access = urlParams.get('access_token');
        const refresh = urlParams.get('refresh_token');

        console.log('토큰 확인중');
        if (access && refresh) {
            console.log('토큰 확인');
            saveTokens(access, refresh);

            //URL에서 토큰 제거
            //window.history.replaceState({}, document.title, window.location.pathname);

            navigate('/');
        } else {
            console.error('토큰을 가져오지 못했습니다');
        }
    }, [saveTokens, navigate]);

    return (
        <div>
            <h2>로그인 처리 중...</h2>
        </div>
    );
};

export default AuthCallbackPage;
