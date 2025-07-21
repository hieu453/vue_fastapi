<script setup>
import { api } from '@/plugins/axios';
import { useAuthStore } from '@/stores/useAuthStore';
import { inject, onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import Edit from './Edit.vue';
import Delete from './Delete.vue';
import Create from './Create.vue';
import { resetObject } from '@/utils/resetObject';

const products = ref()
const error = ref('')
const validationErrors = reactive({})
const openEditModal = ref(false)
const openDeleteModal = ref(false)
const openCreateModal = ref(false)
const selectedProduct = ref()
const checkedProductIds = ref([])

const showSnackbar = inject('showSnackbar')

const authStore = useAuthStore();
const router = useRouter()

const showEditModal = (product) => {
    openEditModal.value = true
    selectedProduct.value = { ...product }
    resetObject(validationErrors)
}

const showDeleteModal = (product) => {
    openDeleteModal.value = true
    selectedProduct.value = { ...product }
}

const showCreateModal = () => {
    openCreateModal.value = true
    resetObject(validationErrors)
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
    try {
        await api.post('products', inputs)
        openCreateModal.value = false
        showSnackbar('Product Created!')
        await fetchProducts()
    } catch (error) {
        const details = error.response.data.detail
        details.forEach(detail => {
            const field = detail.loc[detail.loc.length - 1]
            validationErrors[field] = detail.msg
        });
    }
}

const updateProduct = async (inputs) => {
    try {
        await api.patch(`products/${inputs.id}`, inputs)
        openEditModal.value = false
        showSnackbar('Product Updated!', 'success')
        await fetchProducts()
    } catch (error) {
        const details = error.response.data.detail
        if (Array.isArray(details)) {
            details.forEach(detail => {
                const field = detail.loc[detail.loc.length - 1]
                validationErrors[field] = detail.msg
            });
        } else {
            validationErrors['auth'] = details
        }
    }
}

const deleteProduct = async (product) => {
    await api.delete(`products/${product.id}/delete`)
    openDeleteModal.value = false
    showSnackbar('Product Deleted!')
    await fetchProducts()
}

const logout = () => {
    authStore.logout()
}

onMounted(fetchProducts)

const logIds = () => {
    console.log(checkedProductIds.value)
}
</script>

<template>
    <edit 
        v-model="openEditModal" 
        :product="selectedProduct"
        @update="updateProduct"
        :errors="validationErrors"
    />
    <delete
        v-model="openDeleteModal"
        :product="selectedProduct"
        @delete="deleteProduct"
    />
    <create 
        v-model="openCreateModal"
        @create="createProduct"
        :errors="validationErrors"
    />
    <v-container>
        <v-row justify="center" class="ga-2">
            <v-btn color="blue" rounded="lg" @click="showCreateModal">
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
                        <th>
                            <input type="checkbox">
                        </th>
                        <th class="text-left font-weight-bold">
                            Name
                        </th>
                        <th class="text-left font-weight-bold">
                            Price
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
                                <td>
                                    <input type="checkbox" v-model="checkedProductIds" :value="product.id" @change="logIds">
                                </td>
                                <td>{{ product.name }}</td>
                                <td>${{ product.price }}</td>
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