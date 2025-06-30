<script setup>
import { RouterView } from 'vue-router'
import Snackbar from './components/Snackbar.vue';
import { provide, ref } from 'vue';

const text = ref('')
const visible = ref(false)

const showSnackbar = (message) => {
  text.value = message
  visible.value = true
}

provide('showSnackbar', showSnackbar)
</script>

<template>
  <snackbar v-model="visible" :text="text" />
  <RouterView />
</template>
