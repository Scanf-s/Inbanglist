import './App.css';
import { Route, Routes } from 'react-router-dom';
import Layout from './components/common/Layout';
import HomePage from './pages/HomePage';
import { useState } from 'react';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';

function App() {
    const [darkMode, setDarkMode] = useState(false);

    const toggleDarkMode = () => {
        setDarkMode(!darkMode);
        console.log(darkMode);
    };

    return (
        <Routes>
            <Route
                path='/'
                element={<Layout toggleDarkMode={toggleDarkMode} darkMode={darkMode} />}>
                <Route index element={<HomePage darkMode={darkMode} />} />
            </Route>
            <Route path='login' element={<LoginPage />} />
            <Route path='signUp' element={<SignUpPage />} />
        </Routes>
    );
}

export default App;
