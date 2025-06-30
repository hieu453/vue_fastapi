<script setup>
defineProps({
    text: String,
    color: String
})

const model = defineModel()

</script>

<template>
    <div class="text-center ma-2">
        <v-snackbar v-model="model" timeout="1000" :color="color">
            {{ text }}

            <template v-slot:actions>
                <v-btn color="white" variant="text" @click="model = false">
                    Close
                </v-btn>
            </template>
        </v-snackbar>
    </div>
</template>