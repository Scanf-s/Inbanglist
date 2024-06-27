import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore'; // zustand 스토어를 가져옵니다.

const Activate = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const { activateAccount, showModal, modalMessage, clearError } = useAuthStore();

  useEffect(() => {
    if (token) {
      activateAccount(token);
    }
  }, [token, activateAccount]);

  useEffect(() => {
    if (showModal) {
      setTimeout(() => {
        clearError();
        navigate('/login');
      }, 3000);
    }
  }, [showModal, clearError, navigate]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-2xl font-bold">이메일 인증 중...</h1>
      {showModal && modalMessage && (
        <div className="fixed top-5 right-5 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded shadow-md z-50">
          <div className="flex flex-col items-center">
            <p>{modalMessage}</p>
            <div className="w-full bg-red-300 h-1 mt-2">
              <div
                className="bg-red-600 h-full"
                style={{ width: '100%' }}
              ></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Activate;
