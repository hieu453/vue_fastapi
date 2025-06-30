<script setup>
import { ref } from 'vue'

const props = defineProps({
    product: Object
})
const model = defineModel()
defineEmits(['delete'])
</script>

<template>
    <v-dialog v-model="model" max-width="400" persistent>
        <!-- <template v-slot:activator="{props: activatorProps}">
                <v-btn v-bind="activatorProps">
                    Open Dialog
                </v-btn>
            </template> -->

        <v-card 
            prepend-icon="mdi-map-marker" 
            :text="`Are you sure you want to delete ${product.name}?`"
            :title="`Delete ${product.name}?`"
        >
            <template v-slot:actions>
                <v-spacer></v-spacer>

                <v-btn @click="model = false">
                    Disagree
                </v-btn>

                <v-btn color="red" @click="$emit('delete', product)">
                    Agree
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>