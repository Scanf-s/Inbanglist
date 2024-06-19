import { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';

const StreamLink = ({ url, children, className }) => (
  <Link to={url} className={className}>
    {children}
  </Link>
);

const DetailModal = ({ isOpen, onClose, stream }) => {
  if (!isOpen) return null;
  const modalRef = useRef();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (modalRef.current && !modalRef.current.contains(event.target)) {
        onClose();  // 모달 외부 클릭 시 onClose 함수 호출
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [onClose]);

  return (
    <div className='fixed top-0 left-0 right-0 bottom-0 bg-black/70 flex justify-center items-center z-50 backdrop-blur-sm'>
      <main className='bg-white p-[40px] w-5/6 h-4/6 shadow-md rounded-lg relative flex' ref={modalRef}>
        <div className='mr-10 w-1/2'>
          <img src={stream.thumbnail} alt={stream.title} className='w-full rounded-md' />
          <button onClick={onClose} className='px-3 py-1 bg-black/50 text-white rounded-full absolute top-0 right-[-50px]'>
            X
          </button>
        </div>
        <div className='w-1/2 pt-3'>
          <div className='mb-5'>
            <StreamLink url='' className='flex items-center'>
              <img src='/logo_100.png' alt={stream.channel_name} className='w-10 h-10 rounded-full border mr-3' />
              <span>{stream.channel_name}</span>
            </StreamLink>
          </div>
          <div>
            <StreamLink url='' className='block mb-3'>
              {stream.title}
            </StreamLink>
            <StreamLink url='' className='block text-gray-400 text-base'>
              시청자 {stream.live_viewer}명
            </StreamLink>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DetailModal;