import { defineStore } from 'pinia'
import { Author } from '../types'

export const useAuthorsStore = defineStore('authors', {
    state: () => ({ 
        authors: [] as Author[],
    }),
    actions: {
        saveAuthors(authors: Author[]) {
            this.authors = authors
        }
    }
})