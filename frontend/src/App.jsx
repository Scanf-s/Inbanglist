import './App.css';
import { Route, Routes } from 'react-router-dom';
import Layout from './components/common/Layout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import { useDarkModeStore } from './store/darkMode';
import { useEffect } from 'react';
import GlobalModal from './components/common/GlobalModal';
import UserInfo from './pages/UserInfo';
import useAuthStore from './store/authStore';
import AuthCallbackPage from './pages/AuthCallback';

function App() {
    const { initializeDarkMode } = useDarkModeStore();
    const initializeAuth = useAuthStore((state) => state.initializeAuth);

    useEffect(() => {
        initializeDarkMode();
    }, [initializeDarkMode]);

    useEffect(() => {
        const initialize = async () => {
            await initializeAuth();
        };
        initialize();
    }, [initializeAuth]);

    return (
        <>
            <Routes>
                <Route path='/' element={<Layout />}>
                    <Route index element={<HomePage />} />
                    <Route path='user' element={<UserInfo />} />
                </Route>
                <Route path='login' element={<LoginPage />} />
                <Route path='signUp' element={<SignUpPage />} />
                <Route path='auth/callback' element={<AuthCallbackPage />} />
            </Routes>
            <GlobalModal />
        </>
    );
}

export default App;
