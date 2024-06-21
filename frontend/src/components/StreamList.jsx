import { useEffect, useRef, useState } from 'react';
import StreamItem from './StreamItem';
import axios from '../api/axios';

const StreamList = ({ platform }) => {
    const [streams, setStreams] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const perPage = 10;
    const ref = useRef();

    // 더미데이터 fetch -> 추후 api를 통해 불러온 데이터로 변경하여 관리
    useEffect(() => {
        fetchData();
    }, [platform]);

    const fetchData = async () => {
        try {
            const response = await axios.get(`${platform}`);

            if (response.status < 200 || response.status >= 300) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = response.data;
            const sortedData = data.sort((a, b) => b.concurrent_viewers - a.concurrent_viewers);
            const startIndex = (currentPage - 1) * perPage;
            const selectData = sortedData.slice(startIndex, startIndex + perPage);
            setStreams((prevStreams) => [...prevStreams, ...selectData]);
            // setCurrentPage((prevPage) => prevPage + 1);
        } catch (error) {
            console.log('Error fetching data :', error);
        }
    };
    console.log(streams);

    // 무한 스크롤 구현
    const handleScroll = () => {
        const { scrollTop, clientHeight, scrollHeight } = ref.current;
        if (scrollTop + clientHeight >= scrollHeight - 50) {
            fetchData();
        }
    };

    useEffect(() => {
        ref.current && ref.current.addEventListener('scroll', handleScroll);
        return () => {
            ref.current && ref.current.removeEventListener('scroll', handleScroll);
        };
    }, []);

    return (
        <div className='max-h-[calc(100vh-116px)]'>
            <h1 className='text-2xl p-3'>{platform}</h1>
            <div
                className='flex flex-col gap-6 max-h-[calc(100vh-172px)] scroll-smooth scroll_custom'
                ref={ref}>
                {streams.map((stream) => (
                    <StreamItem key={stream.id} stream={stream} />
                ))}

            </div>
        </div>
    );
};

export default StreamList;
