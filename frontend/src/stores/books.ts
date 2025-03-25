import { defineStore } from 'pinia'
import { Book } from '../types'

export const useBooksStore = defineStore('books', {
    state: () => ({ 
        books: [] as Book[],
    }),
    actions: {
        saveBooks(books: Book[]) {
            this.books = books
        }
    }
})