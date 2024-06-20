import { http, HttpResponse } from 'msw';
import youtubeData from './data/youtube.json';
import chzzkData from './data/chzzk.json';
import afreecatvData from './data/afreecatv.json';

export const handlers = [
    // Intercept "GET https://example.com/user" requests...
    http.get('http://localhost:8000/api/v1/youtube', () => {
        return HttpResponse.json(youtubeData);
    }),

    http.get('http://localhost:8000/api/v1/chzzk', () => {
        return HttpResponse.json(chzzkData);
    }),

    http.get('http://localhost:8000/api/v1/afreecatv', () => {
        return HttpResponse.json(afreecatvData);
    }),
];
