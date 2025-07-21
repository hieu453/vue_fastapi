<script setup>
import { ref, shallowRef, watch } from 'vue';

const model = defineModel()
defineEmits(['update'])
const props = defineProps({
    product: Object,
    errors: Object
})

const inputs = ref()

watch(() => props.product, () => {
    inputs.value = props.product
})
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
                    <v-col cols="12">
                        <p class="text-red">{{ errors?.auth }}</p>
                    </v-col>
                </v-row>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn text="Close" variant="plain" @click="model = false"></v-btn>

                <v-btn color="blue" text="Save" @click="$emit('update', inputs)"></v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>