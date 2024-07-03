import axios from 'axios';

const instance = axios.create({
    baseURL: 'https://www.inbanglist.com/',
    headers: {
        'Content-Type': 'application/json',
    },
});

export default instance;
