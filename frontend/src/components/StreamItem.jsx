const StreamItem = ({ stream }) => {
  return (
    <div className='relative'>
      <div>
        <img src={stream.thumbnail} alt={stream.title} className='block w-full h-auto rounded-md' />
      </div>
      <div className='absolute top-0 left-0 w-full h-full flex flex-col justify-center'>
        <div className='flex flex-row justify-between p-2'>
          <div className='py-0.5 px-1.5 bg-red-600 text-white rounded-md'>LIVE</div>
          <div className='py-0.5 px-1.5 bg-slate-600/75 text-white rounded-md'> {stream.live_viewer}명 시청중</div>
        </div>
        <div className='self-center justify-self-start flex-grow'>PLAY</div>
        <div className='flex flex-row justify-between w-full'>
          <div className='px-3 py-2'>Img</div>
          <div className='flex-grow overflow-hidden px-3 py-2'>
            {/* <span>{stream.channel_name}</span> */}
            <p className='truncate'>{stream.title}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StreamItem;