<script setup>
import { useAuthStore } from '@/stores/useAuthStore';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

const visible = ref(false)
const form = ref()
const inputs = reactive({
    email: null,
    password: null,
})
const router = useRouter()
const authStore = useAuthStore()

const rules = {
    required: value => !!value || 'Required.',
    email: value => {
        const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        return pattern.test(value) || 'Invalid e-mail.'
    },
}

const login = async () => {
    const { valid } = await form.value.validate()

    if (valid) {
        const success = await authStore.login(inputs)

        if (success) {
            router.push({ name: 'products' })
        }
    }
}
</script>

<template>
    <div>
        <v-img class="mx-auto my-6" max-width="228"
            src="https://cdn.vuetifyjs.com/docs/images/logos/vuetify-logo-v3-slim-text-light.svg"></v-img>
        
        <v-card class="mx-auto pa-12 pb-8" elevation="8" max-width="448" rounded="lg">
            <v-form @submit.prevent="login" ref="form">
                <div class="text-subtitle-1 text-medium-emphasis">Email</div>
                <v-text-field v-model="inputs.email" :rules="[rules.email, rules.required]" density="compact" placeholder="Email address" prepend-inner-icon="mdi-email-outline"
                    variant="outlined" :error-messages="authStore.errors"></v-text-field>
                <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                    Password
                    <a class="text-caption text-decoration-none text-blue" href="#" rel="noopener noreferrer"
                        target="_blank">
                        Forgot login password?</a>
                </div>
                <v-text-field v-model="inputs.password" :rules="[rules.required]" :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'" :type="visible ? 'text' : 'password'"
                    density="compact" placeholder="Enter your password" prepend-inner-icon="mdi-lock-outline"
                    variant="outlined" @click:append-inner="visible = !visible"></v-text-field>
                <v-btn type="submit" class="mb-8" color="blue" size="large" variant="tonal" block>
                    Log In
                </v-btn>
                <!-- <v-card-text class="text-center">
                    <a class="text-blue text-decoration-none" href="#" rel="noopener noreferrer" target="_blank">
                        Sign up now <v-icon icon="mdi-chevron-right"></v-icon>
                    </a>
                </v-card-text> -->
            </v-form>
        </v-card>
    </div>
</template>