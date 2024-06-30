import React, { useEffect, useState } from 'react';
import useAuthStore from '../store/authStore';
import { useNavigate } from 'react-router-dom';

const UserInfo = () => {
    const user = useAuthStore((state) => state.user);
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
    const deleteUser = useAuthStore((state) => state.deleteUser);
    const [password, setPassword] = useState('');
    const [isDeletion, setIsDeletion] = useState(false);
    const fetchUser = useAuthStore((state) => state.fetchUser);

    const navigate = useNavigate();

    const handleDeleteAccount = () => {
        if (password.trim() === '') {
            alert('비밀번호를 입력해주세요.');
            return;
        }
        const email = user.email; // user.email

        deleteUser(email, password, () => navigate('/'), setIsDeletion(false));
    };

    useEffect(() => {
        if (!isAuthenticated) {
            console.log('로그인 된 회원만 접근 할 수 있습니다.');
            navigate('/login');
        } else {
            const loadUser = async () => {
                await fetchUser();
            };
            loadUser();
        }
    }, [isAuthenticated, fetchUser, navigate]);

    if (!user) return <p>회원정보를 불러오는 중...</p>;

    const titleLayout = 'mt-10 mb-10 flex';
    const innerTitle = 'w-40';

    const linked = 'text-sm px-2 y-0.5 mr-3 ';
    const unLink = 'text-sm px-2 y-0.5 mr-3 text-slate-500';
    const linkingBtn = 'text-sm px-2 y-0.5 bg-white border solid border-slate-500 rounded-md text-black';
    const unlinkBtn = 'text-sm px-2 y-0.5 bg-white border solid border-slate-500 rounded-md text-slate-500';

    return (
        <div className='relative w-full h-[calc(100vh-68px)] p-8'>
            <div className='mb-5'>
                <h1 className='text-2xl'>회원정보</h1>
            </div>
            <hr />
            <div>
                <div className='flex flex-col items-center text-center'>
                    <p className='mb-5'>
                        {user.user_profile_image ? (
                            <img src='/logo_100.png' className='w-40 h-40 rounded-3xl' />
                        ) : (
                            <img src='/logo_100.png' />
                        )}
                        {/* {user.user_profile_image ? <img src={user.user_profile_image} /> : <img src='/logo_100.png'/>} */}
                    </p>
                    <p className={innerTitle}>아바타</p>
                </div>
                <div className={titleLayout}>
                    <p className={innerTitle}>이름</p>
                    <p>{user.username ? user.username : '이름없음'}</p>
                </div>
                <div className={titleLayout}>
                    <p className={innerTitle}>메일</p>
                    <p>{user?.email}</p>
                </div>
                <div className={titleLayout}>
                    <p className={innerTitle}>연동계정</p>
                    <div>
                        <p className='mb-3'>
                            <span className={unLink}>naver</span>
                            <button className={linkingBtn}>연동하기</button>
                            {/* {naverOauth ? <p className=''>naver</p> : <p>naver</p>} */}
                        </p>
                        <p className='mb-3'>
                            <span className={linked}>google</span>
                            <button className={unlinkBtn}>연동해제</button>
                        </p>
                    </div>
                </div>
            </div>
            <div>
                <button onClick={() => setIsDeletion(true)} className='text-red-500'>
                    회원탈퇴
                </button>
            </div>

            {isDeletion ? (
                <div className='absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] w-[400px] h-[200px] bg-slate-100 rounded-lg border border-1 solid border-black p-8'>
                    <h1 className='text-2xl text-red-600 mb-5'>계정을 삭제하시겠습니까?</h1>
                    <p className='text-slate-700 mb-4'>
                        계정을 삭제하시려면 <i>비밀번호</i> 를 입력하세요.
                    </p>
                    <input
                        type='password'
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className='px-3 py-0.5 outline-none rounded-md bg-slate-300 w-[150px]'
                    />
                    <button onClick={handleDeleteAccount} className='text-red-700 bg-slate-300 ml-5 rounded-md px-3 py-0.5'>
                        계정 삭제
                    </button>
                    <button
                        onClick={() => {
                            setIsDeletion(false);
                            setPassword('');
                        }}
                        className='text-slate-900 bg-slate-300 ml-5 rounded-md px-3 py-0.5'>
                        취소
                    </button>
                </div>
            ) : null}
        </div>
    );
};

export default UserInfo;
