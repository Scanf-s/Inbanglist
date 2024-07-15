import { useEffect, useState } from 'react';
import useAuthStore from '../../store/authStore';

const GlobalModal = () => {
  const { showModal, modalMessage, clearError } = useAuthStore();
  const [secondsLeft, setSecondsLeft] = useState(3);

  useEffect(() => {
    if (showModal) {
      setSecondsLeft(3);
      const startTime = Date.now();
      const interval = setInterval(() => {
        const elapsedTime = (Date.now() - startTime) / 1000;
        const remainingTime = 3 - elapsedTime;

        if (remainingTime <= 0) {
          clearError();
          clearInterval(interval);
          setSecondsLeft(0);
        } else {
          setSecondsLeft(remainingTime);
        }
      }, 100);

      return () => clearInterval(interval);
    }
  }, [showModal, clearError]);

  if (!showModal) return null;

  return (
    <div className="fixed top-5 right-5 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded shadow-md z-50">
      <div className="flex flex-col items-center">
        <p>{modalMessage}</p>
        <div className="w-full bg-red-300 h-1 mt-2">
          <div
            className="bg-red-600 h-full transition-all duration-[100ms]"
            style={{ width: `${(secondsLeft / 3) * 100}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default GlobalModal;
