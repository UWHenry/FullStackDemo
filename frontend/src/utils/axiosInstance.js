import axios from "axios";

const axiosInstance = axios.create({
    baseURL: "https://localhost:8000",
    withCredentials: true
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
