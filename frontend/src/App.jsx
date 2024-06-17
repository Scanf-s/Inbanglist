import './App.css';
import { Route, Routes } from 'react-router-dom';
import Layout from './components/common/Layout';
import HomePage from './pages/HomePage';
import { useState } from 'react';

function App() {
  const [darkMode, setDarkMode] = useState(false);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    console.log(darkMode)
  }

  return (
    <Routes>
      <Route path='/' element={<Layout toggleDarkMode={toggleDarkMode} darkMode={darkMode} />}>
        <Route index element={<HomePage darkMode={darkMode} />} />
      </Route>
    </Routes>
  );
}

export default App;
