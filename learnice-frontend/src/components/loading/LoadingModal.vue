<template>
    <div class="modal-container">
        <div class="d-flex h-100 justify-content-center align-items-center">
            <div class="indicator-background">
                <LoadingIndicator />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import LoadingIndicator from './LoadingIndicator.vue';
</script>

<style scoped>
.modal-container {
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: rgba(114, 114, 114, 0.399);
}
.indicator-background {
    background-color: white;
    border: solid;
    border-color: rgb(181, 181, 181);
    border-width: 0.1rem;
    border-radius: 0.8rem;
}
</style>