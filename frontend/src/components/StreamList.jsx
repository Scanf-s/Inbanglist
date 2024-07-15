import { useCallback, useEffect, useRef, useState } from 'react';
import StreamItem from './StreamItem';
import axios from '../api/axios';
import LoadingSkeleton from './LoadingSkeleton';

const StreamList = ({ platform }) => {
    const [streams, setStreams] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [isLoading, setIsLoading] = useState(false);
    const perPage = 20;
    const maxPage = 5;
    const ref = useRef();

    useEffect(() => {
        fetchData();
    }, [platform]);

    const fetchData = useCallback(async () => {
        if (isLoading || currentPage > maxPage) return;
        setIsLoading(true);

        try {
            const offset = (currentPage - 1) * perPage;
            const response = await axios.get(
                `/api/v1/${platform}/?limit=${perPage}&offset=${offset}`
            );

            if (response.status < 200 || response.status >= 300) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const newStreams = response.data.results.sort(
                (a, b) => b.concurrent_viewers - a.concurrent_viewers
            );
            setStreams((prevStreams) => [...prevStreams, ...newStreams]);
            setCurrentPage((prevPage) => prevPage + 1);
        } catch (error) {
            console.log('Error fetching data :', error);
        } finally {
            setIsLoading(false);
        }
    }, [platform, isLoading]);

    // 무한 스크롤 구현
    const handleScroll = useCallback(() => {
        if (isLoading) return;

        const { scrollTop, clientHeight, scrollHeight } = ref.current;
        if (scrollTop + clientHeight >= scrollHeight) {
            fetchData();
        }
    }, [fetchData]);

    useEffect(() => {
        ref.current && ref.current.addEventListener('scroll', handleScroll);
        return () => {
            ref.current && ref.current.removeEventListener('scroll', handleScroll);
        };
    }, [handleScroll]);

    return (
        <div className='max-h-[calc(100vh-100px)] border dark:border-slate-700 rounded-xl px-4 bg-white dark:bg-slate-800 shadow-md'>
            <div className='flex items-center gap-2 max-h-[56px] p-3'>
                <img src={`/${platform}_logo.svg`} className='w-20 h-[32px]' />
            </div>
            <div
                className='flex flex-col gap-6 max-h-[calc(100vh-157px)] scroll-smooth scroll_custom'
                ref={ref}>
                {streams.length === 0 && isLoading
                    ? Array.from({ length: perPage }).map((_, index) => (
                          <LoadingSkeleton key={index} />
                      ))
                    : streams.map((stream) => <StreamItem key={stream.id} stream={stream} />)}
            </div>
        </div>
    );
};

export default StreamList;
