import { PoSTag } from "@/types/PoSTag";
import { defineStore } from "pinia";

export const useTagStore = defineStore('tagStore', {
    state: () => ({
        tempCount: 0 as number,
        taggedSentence: [
            {
                'word': 'Klettir',
                'tag': 'n'
            },
            {
                'word': 'geta',
                'tag': 'v',
            },
            {
                'word': 'verið',
                'tag': 'v',
            },
            {
                'word': 'hætulegir',
                'tag': 'a',
            },
            {
                'word': '.',
                'tag': 'pl',
            }   
        ] as PoSTag[]
    }),
    getters: {
        getTempCount(state) {
            return state.tempCount;
        }
    },
    actions: {
        increaseTempCount() {
            this.tempCount += 1;
        },
        decreaseTempCount() {
            this.tempCount -= 1;
        }
    }
})