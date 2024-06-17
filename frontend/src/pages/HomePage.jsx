import StreamList from '../components/StreamList';

const HomePage = ({ darkMode }) => {
    return (
        <div className='grid grid-cols-1 md:grid-cols-3 gap-10 p-4 w-full'>
            <StreamList platform='youtube' />
            <StreamList platform='chzzk' />
            <StreamList platform='afreecatv' />
        </div>
    );
};

export default HomePage;
