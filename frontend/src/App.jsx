import './App.css';
import { Route, Routes } from 'react-router-dom';
import Layout from './components/common/Layout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import { useDarkModeStore } from './store/darkMode';
import { useEffect } from 'react';
import Activate from './pages/Activate';
import GlobalModal from './components/common/GlobalModal';

function App() {
  const { initializeDarkMode } = useDarkModeStore();

  useEffect(() => {
    initializeDarkMode();
  }, [initializeDarkMode]);

  return (
    <>
      <Routes>
        <Route path='/' element={<Layout />}>
          <Route index element={<HomePage />} />
        </Route>
        <Route path='login' element={<LoginPage />} />
        <Route path='signUp' element={<SignUpPage />} />
        <Route path='activate/:token' element={<Activate />} />
      </Routes>
      <GlobalModal />
    </>
  );
}

export default App;
