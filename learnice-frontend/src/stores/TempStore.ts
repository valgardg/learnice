import { defineStore } from "pinia";

export const useTempStore = defineStore('temporary', {
    state: () => ({
        tempCount: 0 as number,
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