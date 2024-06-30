import { IoInformationCircleOutline } from 'react-icons/io5';
import DetailModal from './common/DetailModal';
import { useState } from 'react';
import { Link } from 'react-router-dom';

const StreamItem = ({ stream }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);
    const [imgSrc, setImgSrc] = useState(
        stream.thumbnail ? stream.thumbnail : 'https://via.placeholder.com/400x220'
    );

    const handleError = () => {
        setImgSrc('https://via.placeholder.com/400x220');
    };

    const timeSinceStart = (StartedAt) => {
        const startedTime = new Date(StartedAt);
        const currentTime = new Date();

        const diffMs = currentTime - startedTime;

        const diffHours = Math.floor(diffMs / (1000 * 60 * 60)) % 24;
        const diffMinutes = Math.floor(diffMs / (1000 * 60)) % 60;
        const diffSeconds = Math.floor(diffMs / 1000) % 60;

        return {
            hours: diffHours,
            minutes: diffMinutes,
            seconds: diffSeconds,
        };
    };

    const timeDiff = timeSinceStart(stream.created_at);

    return (
        <div className='flex flex-col 2xl:flex-row 2xl:gap-2'>
            <div className='group/item relative 2xl:w-2/6'>
                <div>
                    <img
                        src={imgSrc}
                        alt={stream.title}
                        className='block w-full h-auto rounded-md'
                        onError={handleError}
                    />
                </div>
                <div
                    id='card__container'
                    className='group/edit absolute top-0 left-0 w-full h-full flex flex-col justify-between backdrop-brightness-75 opacity-0 group-hover/item:opacity-100 transition-opacity duration-500 ease-in-out'>
                    <div id='card__live' className='flex flex-row justify-between items-center p-2'>
                        <div className='w-3 h-3 lg:w-4 lg:h-4 2xl:w-2 2xl:h-2 bg-[#F33232] rounded-full ml-1 animate-ping-slow'></div>
                        <div className='px-1 bg-black opacity-70 text-white rounded-md text-sm lg:text-base 2xl:text-xs'>
                            {stream.concurrent_viewers > 1000
                                ? `${(stream.concurrent_viewers / 1000).toFixed(1)}천`
                                : stream.concurrent_viewers}
                            명
                        </div>
                    </div>
                    <div className='absolute right-0 bottom-0 text-xl lg:text-2xl 2xl:text-base'>
                        <button
                            onClick={openModal}
                            className='text-white bg-black opacity-70 rounded-full p-0.5 mx-1 lg:mx-2 my-1'>
                            <IoInformationCircleOutline />
                        </button>
                    </div>
                </div>
            </div>
            <div
                id='card__info'
                className='flex gap-2 lg:gap-3 w-full my-1 2xl:w-4/6 2xl:flex-col 2xl:gap-0 2xl:my-0'>
                <div className='min-w-7 min-h-7 lg:min-w-9 lg:min-h-9 2xl:hidden'>
                    <img
                        src={stream.channel_profile_image}
                        alt={stream.channel_name}
                        className='w-7 h-7 lg:w-9 lg:h-9 rounded-full mt-1.5 ml-0.5 2xl:hidden'
                    />
                </div>
                <div className='flex flex-col flex-grow overflow-hidden'>
                    <Link
                        to={stream.streaming_link}
                        className='truncate py-1 font-semibold text-base lg:text-lg dark:text-[#f5f7fa] hover:opacity-65 dark:hover:opacity-80'>
                        {stream.title}
                    </Link>
                    <div className='text-xs lg:text-sm text-slate-600 dark:text-[#c3cfe2]'>
                        {stream.channel_name}
                    </div>
                    <div className='text-xs lg:text-sm text-slate-600 dark:text-[#c3cfe2]'>
                        {timeDiff.hours > 0
                            ? `${timeDiff.hours}시간 ${timeDiff.minutes}분 ${timeDiff.seconds}초 전`
                            : `${timeDiff.minutes}분 ${timeDiff.seconds}초 전`}
                    </div>
                </div>
            </div>
            {isModalOpen && (
                <DetailModal isOpen={isModalOpen} onClose={closeModal} stream={stream} />
            )}
        </div>
    );
};

export default StreamItem;
