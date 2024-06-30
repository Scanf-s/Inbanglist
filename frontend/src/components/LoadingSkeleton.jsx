const LoadingSkeleton = () => {
    return (
        <div className='flex flex-col 2xl:flex-row 2xl:gap-2 skeleton'>
            <div className='h-48 w-full bg-gray-300 rounded-md'></div>
            <div className='flex flex-col w-full gap-2 p-2'>
                <div className='h-6 bg-gray-300 rounded-md'></div>
                <div className='h-4 bg-gray-300 rounded-md'></div>
                <div className='h-4 bg-gray-300 rounded-md'></div>
            </div>
        </div>
    );
};

export default LoadingSkeleton;
