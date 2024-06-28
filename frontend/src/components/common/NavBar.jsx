import { Link } from 'react-router-dom';
import { useDarkModeStore } from '../../store/darkMode';
import useAuthStore from '../../store/authStore';
import { useEffect, useState } from 'react';

const NavBar = () => {
    const { toggleDarkMode } = useDarkModeStore();
    const [isLogin, setIsLogin] = useState(true);
    const { user, logout } = useAuthStore();

    useEffect(() => {
        if (user) {
            setIsLogin(true);
        }

    },[])

    return (
        <div className='flex justify-between items-center dark:bg-slate-800 bg-slate-200 p-4 h-[68px]'>
            <h1 className='text-3xl dark:text-white text-black'>StreamView</h1>
            <div className='flex items-center gap-2'>
                {user ? (
                    <div className='text-center cursor-pointer tracking-wide dark:text-white text-black'>
                        <Link to='/login' className='inline-block' onClick={logout}>
                            로그아웃
                        </Link>
                    </div>
                ) : (
                    <>
                        <div className='text-center cursor-pointer tracking-wide dark:text-white text-black'>
                            <Link to='/login' className='inline-block'>
                                로그인
                            </Link>
                        </div>
                        <p className='dark:text-white text-black'>/</p>
                        <div className='text-center cursor-pointer tracking-wide dark:text-white text-black'>
                            <Link to='/signUp' className='inline-block'>
                                회원가입
                            </Link>
                        </div>
                    </>
                )}
                <div
                    className='w-12 h-7 p-2 bg-slate-400 dark:bg-slate-900 cursor-pointer rounded-full relative transition-all'
                    onClick={toggleDarkMode}>
                    <div className='w-5 h-5 bg-white absolute top-1 left-1 rounded-full transition-all dark:translate-x-5'>
                        <div className='w-full h-full bg-black dark:bg-white rounded-full' />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default NavBar;
