import { defineStore } from "pinia";
import { Genre } from "../types";

export const useGenreStore = defineStore("genre", {
  state: (): {genre: Genre, csrf:string} => ({
    
    genre: {} as Genre, // Holds the currently selected Genre
    csrf: ''
  }),

  actions: {
    // Save the list of genres
    saveGenres(genre: Genre) {
      this.genre = genre;
    },

    setCsrfToken(csrf: string){
      this.csrf = csrf;
    },
    // Fetch a single Genre by ID from the backend
    async fetchGenre(genreId: number) {
      try {
        const response = await fetch(`https://thebookstack-2.onrender.com/genre/${genreId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch genre data");
        }
        const genreData = await response.json();
        this.genre = genreData; // Update the state with the fetched Genre data
      
      } catch (error) {
        console.error("Error fetching genre data:", error);
      }
    },

    async fetchGenreReturn(genreId: number) {
      try {
        const response = await fetch(`https://thebookstack-2.onrender.com/genre/${genreId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch Genre data");
        }
        const genreData = await response.json();
        this.genre = genreData; // Update the state with the fetched Genre data
        return this.genre
      } catch (error) {
        console.error("Error fetching Genre data:", error);
      }
    },
  },
});