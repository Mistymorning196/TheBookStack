import { defineStore } from 'pinia'
import { Reader } from '../types'

export const useReadersStore = defineStore('readers', {
    state: () => ({ 
        readers: [] as Reader[],
    }),
    actions: {
        saveReaders(readers: Reader[]) {
            this.readers = readers
        }
    }
})