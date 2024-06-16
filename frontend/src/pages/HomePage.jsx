import StreamList from '../components/StreamList';

const HomePage = () => {
  return (
    <div className='grid grid-cols-1 md:grid-cols-3 gap-4 p-4 w-full'>
      <StreamList platform="youtube"/>
      <StreamList platform="chzzk"/>
      <StreamList platform="afreecatv"/>
    </div>
  )
}

export default HomePage