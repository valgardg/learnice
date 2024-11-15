<template>
    <div class="d-flex justify-content-center align-items-center">
        <div class="d-flex flex-column">    
            <div class="d-flex flex-column">
                <input 
                    class="input-frame" 
                    placeholder="Enter an Icelandic sentence to PoS tag!"
                    v-model="typed"/>
                <div class="d-flex justify-content-end mt-2">
                    <button class="btn btn-primary" @click="tagInput">PoS Tag</button>
                </div>
            </div>
            <!-- tagged words -->
            <div v-if="taggedSentence.length > 0" class="tagged-frame d-flex flex-wrap">
                <div v-for="(word, index) in taggedSentence" :key="index" :style="{ marginRight: index !== taggedSentence.length - 1 && taggedSentence[index+1].word != '.' ? '5px' : '0px'}">
                    <WordTooltip :posTag="word">
                        <div :class="['tag-class', !isPunctuation(word.word[0]) ? 'white-text' : '', getTagClass(word.tag)]">
                            {{ word.word }}
                        </div>
                    </WordTooltip>
                </div>
            </div>
        </div>
        <LoadingModal v-if="isLoading" />
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import LoadingModal from '@/components/loading/LoadingModal.vue';
import { useTagStore } from '@/stores/TagStore';
import { storeToRefs } from 'pinia';
import { isPunctuation } from '@/utils/punctuation';
import WordTooltip from '@/components/WordTooltip.vue';

const { tagSentence } = useTagStore();
const { taggedSentence, isLoading } = storeToRefs(useTagStore());
const typed = ref('')

const tagInput = () => {
    tagSentence(typed.value);
}

const getTagClass = (tag: string) => {
    switch (tag[0]) {
        case 'c':
            return 'conjunction';
        case 'n':
            return 'noun';
        case 'l':
            return 'adjective';
        case 's':
            return 'verb';
        case 'a':
            return 'adverb';
        case 'f':
            return 'pronoun';
        case 'g':
            return 'article';
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
.conjunction {
    background-color: #39d37c;
}
.noun {
    background-color: rgb(208, 177, 38);
}
.verb {
    background-color: rgb(255, 116, 116);
}
.adverb {
    background-color: #0A2342;
}
.adjective {
    background-color: rgb(116, 137, 255);
}
.pronoun {
    background-color: #f890de;
}
.article {
    background-color: rgb(98, 229, 229)
}
</style>