import { useEffect, useState } from 'react';
import StreamItem from './StreamItem';

const StreamList = ({ platform }) => {
    const [streams, setStreams] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const perPage = 20;

    // 더미데이터 fetch -> 추후 api를 통해 불러온 데이터로 변경하여 관리
    useEffect(() => {
        fetchData();
    }, [platform, currentPage]);

    // /api/v1/youtube
    // /api/v1/chzzk
    // /api/v1/afreecatv/
    const fetchData = async () => {
        try {
            const response = await fetch('/data/data.json');

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const filteredData = data
                .filter((item) => item.kind === platform)
                .sort((a, b) => b.live_viewer - a.live_viewer);
            const startIndex = (currentPage - 1) * perPage;
            const selectData = filteredData.slice(startIndex, startIndex + perPage);
            setStreams(selectData);
        } catch (error) {
            console.log('Error fetching data :', error);
        }
    };
    console.log(streams);

    return (
        <div>
            <h1 className='text-2xl p-3'>{platform}</h1>
            {streams.map((stream) => (
                <StreamItem key={stream.index} stream={stream} />
            ))}
        </div>
    );
};

export default StreamList;
