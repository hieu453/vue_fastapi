<script setup>
import { resetObject } from '@/utils/resetObject';
import { reactive } from 'vue';

defineProps({
    errors: Object
})

const model = defineModel()
const inputs = reactive({
    name: null,
    price: null,
})
const emit = defineEmits(['create'])

const createProduct = () => {
    emit('create', inputs)
    resetObject(inputs)
}
</script>

<template>
    <v-dialog v-model="model" max-width="600">
        <v-card prepend-icon="mdi-account" title="Product Information">
            <v-card-text>
                <v-row dense>
                    <v-col cols="12" md="4" sm="6">
                        <v-text-field :error-messages="errors?.name" label="Name" v-model="inputs.name"></v-text-field>
                    </v-col>

                    <v-col cols="12" md="4" sm="6">
                        <v-text-field :error-messages="errors?.price" label="Price" type="number" v-model="inputs.price"></v-text-field>
                    </v-col>
                </v-row>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn text="Cancel" variant="plain" @click="model = false"></v-btn>

                <v-btn color="primary" text="Create" variant="tonal" @click="createProduct"></v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>