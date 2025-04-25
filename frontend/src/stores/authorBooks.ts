import { defineStore } from 'pinia'
import { AuthorBook } from '../types'

export const useAuthorBooksStore = defineStore('authorBooks', {
    state: () => ({ 
        authorBooks: [] as AuthorBook[],
    }),
    actions: {
        saveAuthorBooks(authorBooks: AuthorBook[]) {
            this.authorBooks = authorBooks
        }
    }
})