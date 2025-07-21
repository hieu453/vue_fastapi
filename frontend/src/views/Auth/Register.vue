<script setup>
import { api } from '@/plugins/axios';
import { useAuthStore } from '@/stores/useAuthStore';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

const form = ref()
const router = useRouter()
const authStore = useAuthStore()

const inputs = reactive({
    username: null,
    full_name: null,
    email: null,
    password: null,
})

const errors = ref()

const loading = ref(false)

const rules = {
    required: value => !!value || 'Required.',
    email: value => {
        const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        return pattern.test(value) || 'Invalid e-mail.'
    },
}

const register = async () => {
    const { valid } = await form.value.validate()

    if (valid) {
        loading.value = true

        try {
            await api.post("/register", inputs)
            await authStore.login(inputs)
            router.push({ name: 'products' })
            loading.value = false;
        } catch (error) {
            errors.value = error.response.data.detail
            loading.value = false;
        }
    }
}
</script>

<template>
    <v-card class="mx-auto mt-4" max-width="344" title="User Registration">
        <v-form ref="form">
            <v-container>
                <v-text-field v-model="inputs.username" :rules="[rules.required]" color="primary" label="Username"
                    variant="underlined">
                </v-text-field>
                <v-text-field v-model="inputs.full_name" :rules="[rules.required]" color="primary" label="Fullname"
                    variant="underlined"></v-text-field>
                <v-text-field :error-messages="errors" v-model="inputs.email" :rules="[rules.required, rules.email]" color="primary"
                    label="Email" variant="underlined"></v-text-field>
                <v-text-field v-model="inputs.password" :rules="[rules.required]" type="password" color="primary"
                    label="Password" placeholder="Enter your password" variant="underlined"></v-text-field>
            </v-container>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="success" @click="register" :loading="loading">
                    Complete Registration
                    <v-icon icon="mdi-chevron-right" end></v-icon>
                </v-btn>
            </v-card-actions>
        </v-form>
    </v-card>
</template>