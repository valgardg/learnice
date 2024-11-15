<template>
    <div class="tooltip-container" @mouseenter="show = true" @mouseleave="show = false">
        <slot></slot>
        <div v-if="show" class="tooltip">
            <div class="fs-5">{{ posTag.word }}</div>
        </div>
    </div>
</template>
  
<script setup lang="ts">
import { PoSTag } from '@/types/PoSTag';
import { ref, defineProps, computed } from 'vue';

const props = defineProps<{
    posTag: PoSTag;
}>();

const show = ref(false);

const wordInfo = computed(() => {
    const info: {[key: string]: string}[] = [];
    if(props.posTag.tag[0] == 'n') {
        for(const char of props.posTag.tag) {
            info.push({[char]: char});
        }
    }
});
</script>

<style scoped>
.tooltip-container {
    position: relative;
    display: inline-block;
}

.tooltip {
    position: absolute;
    background-color: #f0f0f0;
    color: #000000;
    padding: 8px;
    border: solid;
    border-width: 0.1rem;
    border-radius: 0.4rem;
    white-space: nowrap;
    z-index: 1000;
    opacity: 1.0;
    
    transform: translate(-50%, -50%);
    top: 100%;
    left: 25%;
    margin-top: 8px;
}
</style>