import { Link } from 'react-router-dom';
import { useDarkModeStore } from '../../store/darkMode';
import useAuthStore from '../../store/authStore';

const NavBar = () => {
    const { toggleDarkMode } = useDarkModeStore();
    const user = useAuthStore((state) => state.user);
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
    const logout = useAuthStore((state) => state.logout);
    const navigateToAdminDocs = useAuthStore((state) => state.navigateToAdminDocs);

    return (
        <div className='flex justify-between items-center dark:bg-slate-700 bg-[#c3cfe2] p-4 h-[68px]'>
            <Link to='/' className='flex items-center gap-1 md:gap-2'>
                <img className='w-8 h-8 md:w-10 md:h-10' src='/inbanglist-logo.svg' />
                <h1 className='text-lg md:text-[22px] dark:text-[#f5f7fa] text-black'>INBANGLIST</h1>
            </Link>
            <div className='flex items-center gap-1 md:gap-2'>
                {isAuthenticated ? (
                    <div className='text-center cursor-pointer tracking-wide dark:text-[#f5f7fa] text-black'>
                        {user?.is_staff ? (
                            <button to='/api/v1/docs' className='inline-block mr-3 underline' onClick={navigateToAdminDocs}>
                                Admin Docs
                            </button>
                        ) : null}
                        <Link to='/user' className='inline-block mr-3'>
                            회원 정보
                        </Link>
                        <Link to='/login' className='inline-block' onClick={logout}>
                            로그아웃
                        </Link>
                    </div>
                ) : (
                    <>
                        <div className='text-center cursor-pointer tracking-wide dark:text-[#f5f7fa] text-black text-sm md:text-base'>
                            <Link to='/login' className='inline-block'>
                                로그인
                            </Link>
                        </div>
                        <p className='dark:text-[#c3cfe2] text-black'>/</p>
                        <div className='text-center cursor-pointer tracking-wide dark:text-[#f5f7fa] text-black text-sm md:text-base'>
                            <Link to='/signUp' className='inline-block'>
                                회원가입
                            </Link>
                        </div>
                    </>
                )}
                <div
                    className='md:w-12 md:h-6 w-10 h-5 p-2 mx-1 dark:bg-[#c3cfe2] bg-slate-900 cursor-pointer rounded-full relative transition-all'
                    onClick={toggleDarkMode}>
                    <div className='md:w-4 md:h-4 w-3 h-3 bg-white absolute top-1 md:left-1.5 left-1 rounded-full transition-all dark:translate-x-5'>
                        <div className='w-full h-full dark:bg-black bg-[#f5f7fa] rounded-full' />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default NavBar;
