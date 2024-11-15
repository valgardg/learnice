<template>
    <div class="d-flex justify-content-center align-items-center">
        <div class="d-flex flex-column">    
            <div class="d-flex flex-column">
                <input 
                    class="input-frame" 
                    placeholder="Enter an Icelanndic sentence to PoS tag!"
                    v-model="typed"/>
                <div class="d-flex justify-content-end mt-2">
                    <button class="btn btn-primary" @click="tagInput">PoS Tag</button>
                </div>
            </div>
            <!-- tagged words -->
            <div v-if="tagged.length > 0" class="tagged-frame d-flex flex-wrap">
                <div v-for="(word, index) in taggedSentence" :key="index" :style="{ marginRight: index !== taggedSentence.length - 1 && taggedSentence[index+1].word != '.' ? '5px' : '0px'}">
                    <div :class="['tag-class', word.word != '.' ? 'white-text' : '', getTagClass(word.tag)]">
                        {{ word.word }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useTagStore } from '@/stores/TagStore';
import { storeToRefs } from 'pinia';

const { taggedSentence } = storeToRefs(useTagStore());
const typed = ref('')
const tagged = ref('');

const tagInput = () => {
    tagged.value = typed.value;
    console.log('Tagged value is now: ' + tagged.value);
}

const getTagClass = (tag: string) => {
    switch (tag[0]) {
        case 'n':
            return 'noun';
        case 'a':
            return 'adjective';
        case 'v':
            return 'verb';
        default:
            return '';
    }
}

</script>

<style scoped>
.input-frame {
    border: solid;
    border-radius: 0.8rem;
    border-width: 0.1px;
    padding: 1rem;
    width: 60rem;
    font-size: x-large;
}
.tagged-frame {
    padding: 1rem;
    width: 60rem;
    font-size: x-large;
}
.tag-class {
    padding: 6px;
    border-radius: 0.6rem;
}

.white-text {
    color: white;
}

.noun {
    background-color: rgb(208, 177, 38);
}
.verb {
    background-color: rgb(255, 116, 116);
}
.adjective {
    background-color: rgb(116, 137, 255);
}
</style>