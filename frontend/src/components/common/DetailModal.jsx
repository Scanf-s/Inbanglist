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
                onClose(); // 모달 외부 클릭 시 onClose 함수 호출
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [onClose]);

    return (
        <div className='fixed top-0 left-0 right-0 bottom-0 bg-black/70 flex justify-center items-center z-50 backdrop-blur-sm'>
            <main
                className='bg-[#f5f7fa] dark:bg-slate-700 p-[40px] w-5/6 h-4/6 shadow-md rounded-lg relative flex gap-1 md:gap-4 lg:gap-8 flex-col md:flex-row'
                ref={modalRef}>
                <div className='md:w-1/2 w-full'>
                    <img src={stream.thumbnail} alt={stream.title} className='w-full rounded-md' />
                    <button
                        onClick={onClose}
                        className='px-3 py-1 m-2 border dark:border-slate-700 bg-white text-black dark:bg-black/50 dark:text-white text-sm rounded-lg absolute top-0 right-0'>
                        X
                    </button>
                </div>
                <div className='md:w-1/2 w-full dark:text-[#f5f7fa]'>
                    <div className='my-3 lg:my-5'>
                        <div className='flex items-center gap-1 lg:gap-2'>
                            <img
                                src={stream.channel_profile_image}
                                alt={stream.channel_name}
                                className='max-w-9 max-h-9 lg:max-w-10 lg:max-h-10 mx-0.5 rounded-full border dark:border-slate-400'
                            />
                            <span className='flex-grow'>{stream.channel_name}</span>
                        </div>
                    </div>
                    <div className='my-2 flex gap-1 lg:gap-2'>
                        <StreamLink url={stream.streaming_link}>
                            <img
                                className='max-w-10 max-h-10 lg:max-w-11 lg:max-h-11 motion-safe:animate-bounce'
                                src='/inbanglist-logo.svg'
                            />
                        </StreamLink>
                        <div className='flex flex-col gap-1'>
                            <StreamLink
                                url={stream.streaming_link}
                                className='block text-base lg:text-xl font-semibold my-0 lg:my-0.5 underline'>
                                {stream.title}
                            </StreamLink>
                            <div className='block text-gray-400 text-sm lg:text-base ml-0.5'>
                                {stream.concurrent_viewers > 1000
                                    ? `${(stream.concurrent_viewers / 1000).toFixed(1)}천`
                                    : stream.concurrent_viewers}
                                명 시청 중
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default DetailModal;
