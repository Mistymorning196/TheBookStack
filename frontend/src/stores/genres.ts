import { defineStore } from 'pinia'
import { Genre } from '../types'

export const useGenresStore = defineStore('genres', {
    state: () => ({ 
        genres: [] as Genre[],
    }),
    actions: {
        saveGenres(genres: Genre[]) {
            this.genres = genres
        }
    }
})