import './App.css';
import { Route, Routes } from 'react-router-dom';
import Layout from './components/common/Layout';
import HomePage from './pages/HomePage';

function App() {

  return (
    <Routes>
      <Route path='/' element={<Layout />}>
        <Route index element={<HomePage />} />
      </Route>
    </Routes>
  );
}

export default App;
