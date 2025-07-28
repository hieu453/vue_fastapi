import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000/api",
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
})

api.interceptors.request.use(function (config) {
    const token = localStorage.getItem('access_token') || null
    config.headers.Authorization = token ? `Bearer ${token}` : ''

    return config
}, function (error) {
    return Promise.reject(error);
});

api.interceptors.response.use(function (response) {
    return response;
}, async function (error) {
    const originalRequest = error.config

    if ((error.status === 403 || error.status === 401) && !originalRequest._retry) {
        originalRequest._retry = true

        try {
            // const refreshToken = localStorage.getItem('refresh_token');
            const response = await axios.post("http://localhost:8000/api/refresh-token", {}, { withCredentials: true });
            const accessToken = response.data.access_token
            localStorage.setItem('access_token', accessToken)

            api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
            return api(originalRequest);
        } catch (err) {
            console.error('Token refresh failed:', err);
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            return Promise.reject(err);
        }
    }
    return Promise.reject(error);
});

export {
    api
};
