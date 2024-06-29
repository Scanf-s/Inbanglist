import NavBar from './NavBar';
import { Outlet } from 'react-router-dom';

const Layout = () => {
    return (
        <div className='min-w-screen min-h-screen bg-[#f5f7fa] dark:bg-slate-900'>
            <NavBar />
            <div className='w-full max-h-[calc(100vh-68px)] bg-[#f5f7fa] dark:bg-slate-900'>
                <Outlet />
            </div>
        </div>
    );
};

export default Layout;
