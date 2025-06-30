import { api } from '@/plugins/axios';
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
    const errors = ref()

    const login = async (credentials) => {
        const credentialsFormData = new FormData();
        credentialsFormData.append('username', credentials.email)
        credentialsFormData.append('password', credentials.password)

        try {
            const response = await api.post('/token', credentialsFormData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            })
            localStorage.setItem('auth-token', response.data.access_token)

            return true
        } catch (error) {
            errors.value = error.response.data.detail
            
            return false
        }

    }

    const logout = () => {
        localStorage.removeItem('auth-token')
    }

    const getAuthUser = async () => {
        try {
            const response = await api.get("/me")
            return response.data
        } catch (error) {
            return null
        }

    }

    return { login, errors, logout, getAuthUser }
})