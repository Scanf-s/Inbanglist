import NavBar from './NavBar';
import { Outlet } from 'react-router-dom';

const Layout = ({ darkMode, toggleDarkMode }) => {
    return (
        <div className={`w-full max-h-screen min-w-screen ${darkMode ? 'dark' : ''} `}>
            <NavBar toggleDarkMode={toggleDarkMode} darkMode={darkMode} />
            <div
                className={`w-full max-h-[calc(100vh-68px)] ${
                    darkMode ? 'bg-slate-700' : 'bg-white'
                }`}>
                <Outlet />
            </div>
        </div>
    );
};

export default Layout;
