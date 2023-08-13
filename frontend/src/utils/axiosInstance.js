import axios from "axios";
import axiosRetry from "axios-retry";

const axiosInstance = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
    withCredentials: true
});
axiosRetry(axiosInstance, {
    retries: 3,
    retryDelay: (retryCount) => {
        return retryCount * 1000;
    },
    retryCondition: (error) => {
        const isOptimisticLockConflict = (
            error.response &&
            error.response.status === 409 &&
            error.response.data === "Optimistic Lock Conflict"
        );
        return isOptimisticLockConflict;
    }
});

function getCookie(name) {
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

axiosInstance.interceptors.request.use(
    async (config) => {
        // configuer csrf token
        let csrfToken = getCookie("csrf_access_token");
        if (csrfToken) config.headers["X-CSRF-TOKEN"] = csrfToken;
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

axiosInstance.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 422) {
            window.location.href = '/logout';
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;
