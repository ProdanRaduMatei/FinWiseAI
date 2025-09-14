import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:9090/api', // adjust if needed
    headers: {
        'Content-Type': 'application/json',
    },
});

export default api;