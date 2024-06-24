import NavBar from './NavBar';
import { Outlet } from 'react-router-dom';

const Layout = () => {
    return (
        <div className='min-w-screen min-h-screen'>
            <NavBar />
            <div className='w-full max-h-[calc(100vh-68px)] dark:bg-slate-700 bg-white'>
                <Outlet />
            </div>
        </div>
    );
};

export default Layout;
