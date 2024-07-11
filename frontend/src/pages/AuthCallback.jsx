import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';

const AuthCallbackPage = () => {
    const navigate = useNavigate();
    const { saveTokens } = useAuthStore();

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const access = urlParams.get('access_token');
        const refresh = urlParams.get('refresh_token');

        if (access && refresh) {
            saveTokens(access, refresh);
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
