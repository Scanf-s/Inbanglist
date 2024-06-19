import { IoInformationCircleOutline } from 'react-icons/io5';
import { FaPlay } from 'react-icons/fa';
import DetailModal from './common/DetailModal';
import { useState } from 'react';
import { Link } from 'react-router-dom';

const StreamItem = ({ stream }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);
  return (
    <div className='relative'>
      <div>
        <img src={stream.thumbnail} alt={stream.title} className='block w-full h-auto rounded-md' />
      </div>
      <div id='card__container' className='absolute top-0 left-0 w-full h-full flex flex-col justify-center'>
        <div id='card__live' className='flex flex-row justify-between p-2'>
          <div className='w-3 lg:w-11 h-3 lg:h-7  lg:py-0.5 lg:px-1.5 bg-red-600 text-white rounded-full md:rounded-md'>
            <span className='hidden lg:inline'>LIVE</span>
          </div>
          <div className='py-0.5 px-1.5 bg-slate-600/75 text-white rounded-md'> {stream.live_viewer}명 시청중</div>
        </div>
        <div id='card__play' className=' flex-grow w-full h-full flex'>
          <Link to='' className='m-auto'>
            <FaPlay className=' w-10 h-8 text-white' />
          </Link>
        </div>
        <div id='card__info' className='flex flex-row justify-between w-full items-center md:invisible lg:visible'>
          <div className='px-2 text-xl w-14 h-14 flex ml-1'>
            <img src='/logo_100.png' alt={stream.channel_name} className='min-w-10 h-10 rounded-full m-auto' />
          </div>
          <div className='flex-grow overflow-hidden px-1 py-2'>
            <span className='text-md md:text-sm text-slate-600'>{stream.channel_name}</span>
            <p className='truncate text-sm md:text-base lg:text-xl'>{stream.title}</p>
          </div>
          <div className='px-3 py-2 text-xl'>
            <button onClick={openModal} className='flex items-center'>
              <IoInformationCircleOutline />
            </button>
            <DetailModal isOpen={isModalOpen} onClose={closeModal} stream={stream} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default StreamItem;
