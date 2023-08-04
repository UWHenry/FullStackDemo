import axios from "axios";

const axiosInstance = axios.create({
    baseURL: "https://localhost:8000",
    withCredentials: true
});

axiosInstance.interceptors.request.use(
    async (config) => {
        // configure JSON Web Token
        const token = sessionStorage.getItem("jwtToken");
        if (token) {
            config.headers["Authorization"] = `Bearer ${token}`;
        }
        // configuer csrf token
        if (['post', 'put', 'patch', 'delete'].includes(config.method.toLowerCase()) && !config.headers['X-CSRFToken']) {
            try {
                const response = await axios.get(
                    `${axiosInstance.defaults.baseURL}/api/get_csrf_token`,
                    { withCredentials: true }
                );
                config.headers['X-CSRFToken'] = response.data.csrf_token;
            } catch (error) {
                console.error('Error fetching CSRF token:', error);
            }
        }
        return config;
    },
    (error) => {
        console.log("axios error:");
        console.log(error);
        return Promise.reject(error);
    }
);

export default axiosInstance;
