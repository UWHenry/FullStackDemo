import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'https://localhost:8000',
});

axiosInstance.interceptors.request.use(
    (config) => {
        const token = sessionStorage.getItem('jwtToken');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        console.log("axios error:")
        console.log(error)
        return Promise.reject(error);
    }
);

export default axiosInstance;
