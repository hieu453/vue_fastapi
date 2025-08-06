<script setup>
</script>

<template>
    <v-container>
        <v-row justify="center" class="ga-2">
            <router-link :to="{ name: 'login' }">
                <v-btn>
                    Login
                </v-btn>
            </router-link>
            <router-link :to="{ name: 'register' }">
                <v-btn>
                    Register
                </v-btn>
            </router-link>
        </v-row>
    </v-container>
</template>