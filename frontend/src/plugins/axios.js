import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000/api",
    headers: {
        'Content-Type': 'application/json',
    }
})

api.interceptors.request.use(function (config) {
    const token = localStorage.getItem('auth-token') || null
    config.headers.Authorization = token ? `Bearer ${token}` : ''
    
    return config
}, function (error) {
    return Promise.reject(error);
});

export { 
    api
}