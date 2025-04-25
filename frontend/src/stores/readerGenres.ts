import { defineStore } from 'pinia'
import { ReaderGenre } from '../types'

export const useReaderGenresStore = defineStore('readerGenres', {
    state: () => ({ 
        readerGenres: [] as ReaderGenre[],
    }),
    actions: {
        saveReaderGenres(readerGenres: ReaderGenre[]) {
            this.readerGenres = readerGenres
        }
    }
})