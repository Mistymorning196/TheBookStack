import { defineStore } from 'pinia'
import { BookGenre } from '../types'

export const useBookGenresStore = defineStore('bookGenres', {
    state: () => ({ 
        bookGenres: [] as BookGenre[],
    }),
    actions: {
        saveBookGenres(bookGenres: BookGenre[]) {
            this.bookGenres = bookGenres
        }
    }
})