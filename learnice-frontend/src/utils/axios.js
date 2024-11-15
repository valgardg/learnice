import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'https://api.example.com', // REPLACE WITH ACTUAL URL
    timeout: 1000,
    headers: { 'X-Custom-Header': 'foobar' }
});

// optional interceptor
axiosInstance.interceptors.request.use(
    config => {
        // do something before request is sent
        return config;
    },
    error => {
        // do something with request error
        return Promise.reject(error);
    }
);

axiosInstance.interceptors.response.use(
    response => {
        // any status code that lie within the range of 2xx cause this function to trigger
        return response;
    },
    error => {
        // any status code that falls outside the range of 2xx cause this function to trigger
        return Promise.reject(error);
    }
);

export default axiosInstance;