import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';
import Modal from '../components/common/GlobalModal';

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    // 로그인 버튼 클릭 이벤트 함수
    const { login, error, setError, showModal, clearError } = useAuthStore();
    const handleLogin = async (e) => {
        e.preventDefault();

        // 이메일 형식 검증
        let regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!regex.test(email)) {
            setError('이메일 형식이 올바르지 않습니다.');
            return;
        }

        // 로그인 함수 호출
        await login(email, password, () => navigate('/'));
    };

    useEffect(() => {
        if (showModal) {
            setTimeout(() => {
                clearError();
            }, 3000);
        }
    }, [showModal, clearError]);

    const handleNaverLogin = () => {
        window.open('/api/users/oauth2/naver/login', '_blank', 'noopener,noreferrer,width=600,height=600');
    };

    const openGoogleLogin = () => {
        const googleLoginUrl = '/api/users/oauth2/google/login';
        window.open(googleLoginUrl, 'googleLogin', 'noopener,noreferrer,width=600,height=600');
    };

    return (
        <div className='h-screen w-screen bg-gradient-to-br from-[#f5f7fa] to-[#c3cfe2] dark:from-[#537895] dark:to-[#09203f]'>
            <div className='fixed h-full w-full'>
                <div className='h-full flex justify-center items-center'>
                    <div className='flex flex-col gap-8 w-[calc(100%-40px)] max-w-[440px] p-[50px] bg-white dark:bg-[#09203f] border dark:border-[#09203f] rounded-xl shadow-md'>
                        <form className='flex flex-col gap-4' onSubmit={handleLogin}>
                            <input
                                className='h-12 p-2 w-full border border-solid border-slate-300 rounded-md text-sm dark:bg-[#09203f] dark:text-[#f5f7fa]'
                                type='text'
                                name='email'
                                id='email'
                                required
                                placeholder='이메일'
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                            <input
                                className='h-12 p-2 w-full border border-solid border-slate-300 rounded-md text-sm dark:bg-[#09203f] dark:text-[#f5f7fa]'
                                type='password'
                                name='password'
                                id='password'
                                required
                                placeholder='비밀번호'
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                            <button
                                className='w-full h-12 text-lg bg-[#929EAD] text-white dark:text-black rounded-md hover:bg-[#BCC5CE]'
                                type='submit'>
                                로그인
                            </button>
                        </form>
                        <form className='flex flex-col gap-4 border-t-[1px] border-t-slate-300 dark:text-[#c3cfe2]'>
                            <p className='mt-8 mb-2 text-center'>소셜로 간편하게 로그인하세요</p>
                            <button
                                onClick={openGoogleLogin}
                                className='relative flex justify-center items-center gap-4 w-full h-12 pl-3 text-lg rounded-md border border-[#166ae5] text-[#166ae5] hover:bg-[#e7f0fd]'
                                type='submit'>
                                <img className='w-[25px] absolute left-6' src='/Google__G__logo.svg.png' />
                                구글 로그인
                            </button>
                            <button
                                onClick={handleNaverLogin}
                                className='relative flex justify-center items-center gap-4 w-full h-12 pl-3 text-lg rounded-md border border-[#65A23F] text-[#65A23F] hover:bg-[#deecdd]'
                                type='submit'>
                                <img className='w-[25px] absolute left-6' src='/Naver_logo_initial.svg.png' />
                                네이버 로그인
                            </button>
                        </form>
                        <div className='flex justify-center gap-1 text-sm dark:text-[#c3cfe2]'>
                            <p>아직 회원이 아니신가요?</p>
                            <Link to='/signUp' className='text-[#929EAD] font-bold underline'>
                                지금 가입하세요.
                            </Link>
                        </div>
                        {showModal && error && <Modal message={error} onClose={clearError} />}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
