<script setup>
import { api } from '@/plugins/axios';
import { useAuthStore } from '@/stores/useAuthStore';
import { inject, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import Edit from './Edit.vue';
import Delete from './Delete.vue';
import Create from './Create.vue';

const products = ref()
const error = ref('')
const openEditModal = ref(false)
const openDeleteModal = ref(false)
const openCreateModal = ref(false)
const selectedProduct = ref()

const showSnackbar = inject('showSnackbar')
console.log(showSnackbar)

const authStore = useAuthStore();
const router = useRouter()

const showEditModal = (product) => {
    openEditModal.value = true
    selectedProduct.value = { ...product }
}

const showDeleteModal = (product) => {
    openDeleteModal.value = true
    selectedProduct.value = { ...product }
}

const fetchProducts = async () => {
    try {
        const response = await api.get("/products")
        products.value = response.data
    } catch (err) {
        error.value = 'You are not logged in!'
    }
}

const createProduct = async (inputs) => {
    await api.post('products', inputs)
    openCreateModal.value = false
    showSnackbar('Product Created!')
    fetchProducts()
}

const updateProduct = async (inputs) => {
    await api.patch(`products/${inputs.id}`, inputs)
    openEditModal.value = false
    showSnackbar('Product Updated!')
    fetchProducts()
}

const deleteProduct = async (product) => {
    await api.delete(`products/${product.id}/delete`)
    openDeleteModal.value = false
    showSnackbar('Product Deleted!')
    fetchProducts()
}

const logout = () => {
    authStore.logout()
    router.push({ name: 'home' })
}

onMounted(fetchProducts)
</script>

<template>
    <edit 
        v-model="openEditModal" 
        :product="selectedProduct"
        @update="updateProduct"
    />
    <delete
        v-model="openDeleteModal"
        :product="selectedProduct"
        @delete="deleteProduct"
    />
    <create 
        v-model="openCreateModal"
        @create="createProduct"
    />
    <v-container>
        <v-row justify="center" class="ga-2">
            <v-btn color="blue" rounded="lg" @click="openCreateModal = true">
                Create product
            </v-btn>
            <v-btn rounded="lg" @click="logout">
                Logout
            </v-btn>
        </v-row>
        <v-row justify="center">
            <v-table>
                <thead>
                    <tr>
                        <th class="text-left font-weight-bold">
                            Name
                        </th>
                        <th class="text-left font-weight-bold">
                            Calories
                        </th>
                        <th class="text-left font-weight-bold">
                            Options
                        </th>
                    </tr>
                </thead>
                <template v-if="products">
                    <template v-if="products.length > 0">
                        <tbody>
                            <tr v-for="product in products" :key="product.name">
                                <td>{{ product.name }}</td>
                                <td>{{ product.price }}</td>
                                <td class="d-flex ga-2 align-center">
                                    <v-btn class="rounded-xl bg-green" @click="showEditModal(product)">
                                        Edit
                                    </v-btn>
                                    <v-btn class="rounded-xl bg-red" @click="showDeleteModal(product)">
                                        Delete
                                    </v-btn>
                                </td>
                            </tr>
                        </tbody>
                    </template>
                    <template v-else>
                        <p>No products in db</p>
                    </template>
                </template>
                <template v-else>
                    Fetching products...
                </template>
            </v-table>
            <template v-if="error">
                <p style="color: red;">{{ error }}</p>
            </template>
        </v-row>
    </v-container>
</template>