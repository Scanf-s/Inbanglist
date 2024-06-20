import './index.css';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App.jsx';
import { enableMocking } from './mocks/enableMocking.js';

async function startApp() {
    await enableMocking();
    ReactDOM.createRoot(document.getElementById('root')).render(
        <BrowserRouter>
            <App />
        </BrowserRouter>
    );
}

startApp();
