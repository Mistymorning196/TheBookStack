import { defineStore } from 'pinia'
import { UserBook } from '../types'

export const useUserBooksStore = defineStore('userBooks', {
    state: () => ({ 
        userBooks: [] as UserBook[],
    }),
    actions: {
        saveUserBooks(userBooks: UserBook[]) {
            this.userBooks = userBooks
        }
    }
})