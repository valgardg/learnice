<template>
    <div class="tooltip-container" @mouseenter="show = true" @mouseleave="show = false">
        <slot></slot>
        <div v-if="show" class="tooltip">
            <div class="fs-5">{{ posTag.word }} - {{ posTag.translation }}</div>
            <!-- Iterate through posTag keys -->
            <div v-for="(value, key) in parseDynamicPosTag(posTag.tag)" :key="key">
                {{ value }}
            </div>
            {{ parsedTag.length }}
        </div>
    </div>
</template>
  
<script setup lang="ts">
import { PoSTag } from '@/types/PoSTag';
import { ref, defineProps, computed, onMounted } from 'vue';
import { parseDynamicPosTag } from '@/utils/generateWordInfo'

const props = defineProps<{
    posTag: PoSTag;
}>();

const show = ref(false);
const parsedTag = ref({});
</script>

<style scoped>
.tooltip-container {
    position: relative;
    display: inline-block;
}

.tooltip {
    position: absolute;
    background-color: #ffffff;
    color: #000000;
    padding: 8px;
    border: solid;
    border-width: 0.1rem;
    border-radius: 0.2rem;
    white-space: nowrap;
    z-index: 1000;
    opacity: 1.0;
    
    transform: translate(-50%, -50%);
    top: 220%;
    left: 75%;
    margin-top: 8px;
}
</style>