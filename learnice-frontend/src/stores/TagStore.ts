import { PoSTag } from "@/types/PoSTag";
import { defineStore } from "pinia";

export const useTagStore = defineStore('tagStore', {
    state: () => ({
        tempCount: 0 as number,
        taggedSentence: [] as PoSTag[],
        isLoading: false as boolean,
    }),
    getters: {
        // getTempCount(state) {
        //     return state.tempCount;
        // }
    },
    actions: {
        async tagSentence(sentenceToTag: string) {
            this.isLoading = true;
            this.taggedSentence = [];
            const url = `http://127.0.0.1:8000/tag/${encodeURIComponent(sentenceToTag)}`;

            try {
                const response = await fetch(url);

                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }

                // parse response
                const data = await response.json();

                for (const item of data) {
                    console.log(item);
                    this.taggedSentence.push({
                        'word': item[0],
                        'tag': item[1],
                        'translation': item[2],
                    })
                }
                this.isLoading = false;
            } catch (error) {
                this.isLoading = false;
                console.error("Error tagging sentence: ", error);
            }
        }
    }
})