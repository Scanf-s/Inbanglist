import './App.css';
import { Route, Routes } from 'react-router-dom';
import Layout from './components/common/Layout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import { useDarkModeStore } from './store/darkMode';
import { useEffect } from 'react';
import GlobalModal from './components/common/GlobalModal';
<<<<<<< HEAD
import useAuthStore from './store/authStore';
=======
import UserInfo from './pages/UserInfo';
>>>>>>> 730cb9b (회원정보 페이지 생성 및 라우터 설정)

function App() {
  const { initializeDarkMode } = useDarkModeStore();
  const initializeAuth = useAuthStore((state) => state.initializeAuth);

  useEffect(() => {
    initializeDarkMode();
  }, [initializeDarkMode]);

  return (
    <>
      <Routes>
        <Route path='/' element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path='user' element={<UserInfo />} />
        </Route>
        <Route path='login' element={<LoginPage />} />
        <Route path='signUp' element={<SignUpPage />} />
<<<<<<< HEAD
=======
        <Route path='activate/:token' element={<Activate />} />
        <Route path='user' element={<UserInfo />} />
>>>>>>> 730cb9b (회원정보 페이지 생성 및 라우터 설정)
      </Routes>
      <GlobalModal />
    </>
  );
}

export default App;
