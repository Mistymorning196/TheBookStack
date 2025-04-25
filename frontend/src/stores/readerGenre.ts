import { defineStore } from "pinia";
import { ReaderGenre } from "../types";

export const useReaderGenreStore = defineStore("readerGenre", {
  state: (): {readerGenre: ReaderGenre, csrf:string} => ({
    
    readerGenre: {} as ReaderGenre, // Holds the currently selected readerGenre
    csrf: ''
  }),

  actions: {
    // Save the list of readerGenres
    saveReaderGenres(readerGenre: ReaderGenre) {
      this.readerGenre = readerGenre;
    },

    setCsrfToken(csrf: string){
      this.csrf = csrf;
    },
    // Fetch a single readerGenre by ID from the backend
    async fetchReaderGenre(readerGenreId: number) {
      try {
        const response = await fetch(`http://localhost:8000/reader_genre/${readerGenreId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch readerGenre data");
        }
        const readerGenreData = await response.json();
        this.readerGenre = readerGenreData; // Update the state with the fetched readerGenre data
      
      } catch (error) {
        console.error("Error fetching readerGenre data:", error);
      }
    },

    async fetchReaderGenreReturn(readerGenreId: number) {
      try {
        const response = await fetch(`http://localhost:8000/reader_genre/${readerGenreId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch readerGenre data");
        }
        const readerGenreData = await response.json();
        this.readerGenre = readerGenreData; // Update the state with the fetched readerGenre data
        return this.readerGenre
      } catch (error) {
        console.error("Error fetching readerGenre data:", error);
      }
    },
  },
});