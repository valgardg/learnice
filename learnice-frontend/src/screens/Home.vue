<template>
    <div class="d-flex justify-content-center align-items-start">
        <div class="d-flex flex-column">  
              <!-- input section -->
            <div class="d-flex flex-column input-section">
                <p class="fs-2">The Learnice Sentence Analyzer</p>
                <p>Simply input an Icelandic or English sentence; English sentences will be automatically translated to Icelandic. Each word is then analyzed with PoS tagging, showing details like word class, gender, number, case, and declension. You'll also see a direct translation of each word. If there are any grammar or spelling mistakes, we’ll provide suggestions to help you improve. Perfect for learning and mastering Icelandic!</p>
                <input
                    class="input-frame" 
                    placeholder="Enter an Icelandic or English sentence to analyze!"
                    v-model="typed"/>
                <div class="d-flex justify-content-end mt-2">
                    <button class="btn btn-primary" @click="tagInput">Analyze sentence</button>
                </div>
            </div>
            <!-- predicted language -->
            <div class="d-flex justify-content-end pred-langauge-text" v-if="predictedLangauge">
                <div>Predicted input language: {{ predictedLangauge }}</div>
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
            <!-- grammar suggestins -->
            <div v-if="grammarSuggestions.length > 0" class="mt-2 suggestion-frame">
                <div class="fs-4 suggestion-title fw-bold">Grammar and spelling suggestions</div>
                <div v-for="(suggestion, index) in grammarSuggestions" :key="index">
                    <div class="d-flex flex-row align-items-center mt-1">
                        <div class="incorrect">{{ suggestion.incorrect }}</div>
                        <div>-></div>
                        <div class="correct">{{ suggestion.corrected }}</div>
                    </div>
                </div>
            </div>
        </div>
        <LoadingModal v-if="isLoading" />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import LoadingModal from '@/components/loading/LoadingModal.vue';
import { useTagStore } from '@/stores/TagStore';
import { storeToRefs } from 'pinia';
import { isPunctuation } from '@/utils/punctuation';
import WordTooltip from '@/components/WordTooltip.vue';

const { tagSentence } = useTagStore();
const { taggedSentence, grammarSuggestions, predictedLangauge, isLoading } = storeToRefs(useTagStore());
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
        case 't':
            return 'numeral';
        default:
            return '';
    }
}
</script>

<style scoped>
.input-section {
    width: 60rem;
    margin-top: 7rem;
}
.input-frame {
    border: solid;
    border-radius: 0.8rem;
    border-width: 0.1px;
    padding: 1rem;
    width: 60rem;
    font-size: x-large;
    margin-top: 1rem;
}
.tagged-frame {
    padding: 1rem;
    width: 60rem;
    font-size: x-large;
}
.suggestion-frame {
    padding: 1rem;
}
.tag-class {
    padding: 6px;
    border-radius: 0.6rem;
}

.white-text {
    color: white;
}
.conjunction {
    background-color: #20f17a;
}
.noun {
    background-color: rgb(255, 210, 7);
}
.verb {
    background-color: rgb(255, 76, 76);
}
.adverb {
    background-color: #0A2342;
}
.adjective {
    background-color: rgb(78, 105, 255);
}
.pronoun {
    background-color: #ff48ce;
}
.article {
    background-color: rgb(93, 246, 246)
}
.numeral {
    background-color: #80fd27;
}
.pred-langauge-text {
    font-size: small;
    margin-top: 0.5rem;
}
.incorrect {
    padding: 0.5rem;
    margin-right: 0.5rem;
    background-color: rgb(255, 76, 76);
    border-radius: 0.8rem;
    color: white;
}
.correct {
    padding: 0.5rem;
    margin-left: 0.5rem;
    background-color: #20f17a;
    border-radius: 0.8rem;
    color: white;
}
</style>