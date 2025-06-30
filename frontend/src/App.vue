<script setup>
import { RouterView } from 'vue-router'
import Snackbar from './components/Snackbar.vue';
import { provide, ref } from 'vue';

const text = ref('')
const visible = ref(false)
const color = ref('')

const showSnackbar = (message, colorValue) => {
  text.value = message
  color.value = colorValue
  visible.value = true
}

provide('showSnackbar', showSnackbar)
</script>

<template>
  <snackbar v-model="visible" :text="text" :color="color" />
  <RouterView />
</template>
