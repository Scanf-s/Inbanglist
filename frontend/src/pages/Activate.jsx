import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';
import Modal from '../components/common/GlobalModal';

const Activate = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const { activateAccount, showModal, error, clearError } = useAuthStore();

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
      {showModal && error && <Modal message={error} onClose={clearError}/>}
    </div>
  );
};

export default Activate;
