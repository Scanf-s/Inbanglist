import StreamList from '../components/StreamList';

const HomePage = () => {
    return (
        <div className='grid grid-cols-1 md:grid-cols-3 gap-4 lg:gap-6 py-4 px-14 md:px-8 w-full max-h-[calc(100vh-68px)]'>
            <StreamList platform='youtube' />
            <StreamList platform='chzzk' />
            <StreamList platform='afreecatv' />
        </div>
    );
};

export default HomePage;
