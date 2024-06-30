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
                className='bg-[#f5f7fa] dark:bg-slate-700 p-[40px] lg:w-3/5 lg:h-4/5 w-3/4 h-3/4 shadow-md rounded-lg relative flex gap-1 md:gap-2 flex-col items-center'
                ref={modalRef}>
                <div className='group/item md:w-4/5 w-full relative'>
                    <img
                        src={stream.thumbnail}
                        alt={stream.title}
                        className='w-full h-fit rounded-md'
                    />
                    <div className='group/edit absolute top-0 left-0 justify-between w-full h-full group-hover/item:backdrop-brightness-75 duration-500 ease-in-out'>
                        <div className='flex flex-col justify-between'>
                            <div className='self-end px-1 bg-black opacity-70 text-white rounded-md text-sm md:text-base lg:text-lg m-2'>
                                {stream.concurrent_viewers > 1000
                                    ? `${(stream.concurrent_viewers / 1000).toFixed(1)}천`
                                    : stream.concurrent_viewers}
                                명 시청 중
                            </div>
                            <StreamLink
                                url={stream.streaming_link}
                                className='min-w-8 min-h-8 md:min-w-10 md:min-h-10 flex-grow self-center justify-self-center absolute inset-x-2/4 inset-y-2/4'>
                                <img
                                    className='w-8 h-8 md:w-10 md:h-10 motion-safe:animate-bounce group-hover/item:animate-ping-slow'
                                    src='/inbanglist-logo.svg'
                                />
                            </StreamLink>
                        </div>
                    </div>
                </div>
                <button
                    onClick={onClose}
                    className='px-3 py-1 m-2 border dark:border-slate-700 bg-white text-black dark:bg-black/50 dark:text-white text-sm rounded-lg absolute top-0 right-0'>
                    X
                </button>
                <div className='md:w-4/5 w-full dark:text-[#f5f7fa]'>
                    <div className='my-3 lg:my-5 w-full '>
                        <div className='flex gap-2 lg:gap-3 my-1 w-full'>
                            <img
                                src={stream.channel_profile_image}
                                alt={stream.channel_name}
                                className='w-9 h-9 lg:w-10 lg:h-10 mx-0.5 mt-1 rounded-full border dark:border-slate-400'
                            />
                            <div className='flex flex-col flex-grow overflow-hidden'>
                                <StreamLink
                                    url={stream.streaming_link}
                                    className='text-base lg:text-xl font-semibold my-0 lg:my-0.5 hover:opacity-65 dark:hover:opacity-80 text-justify'>
                                    {stream.title}
                                </StreamLink>
                                <span className='text-slate-600 dark:text-[#c3cfe2]'>
                                    {stream.channel_name}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div className='my-2 flex gap-1 lg:gap-2'></div>
                </div>
            </main>
        </div>
    );
};

export default DetailModal;
