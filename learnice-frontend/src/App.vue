<template>
  <div class="d-flex flex-column main-container">
    <AppHeader />
    <RouterView class="router-view"/>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import AppHeader from './components/header/AppHeader.vue';
</script>

<style scoped>
.main-container {
    min-height: 100vh;
}
.router-view {
    flex: 1;
}
</style>
