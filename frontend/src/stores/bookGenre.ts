import { defineStore } from "pinia";
import { BookGenre } from "../types";

export const useBookGenreStore = defineStore("bookGenre", {
  state: (): {bookGenre: BookGenre, csrf:string} => ({
    
    bookGenre: {} as BookGenre, // Holds the currently selected bookGenre
    csrf: ''
  }),

  actions: {
    // Save the list of bookGenres
    saveBookGenres(bookGenre: BookGenre) {
      this.bookGenre = bookGenre;
    },

    setCsrfToken(csrf: string){
      this.csrf = csrf;
    },
    // Fetch a single bookGenre by ID from the backend
    async fetchBookGenre(bookGenreId: number) {
      try {
        const response = await fetch(`http://localhost:8000/book_genre/${bookGenreId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch bookGenre data");
        }
        const bookGenreData = await response.json();
        this.bookGenre = bookGenreData; // Update the state with the fetched bookGenre data
      
      } catch (error) {
        console.error("Error fetching bookGenre data:", error);
      }
    },

    async fetchBookGenreReturn(bookGenreId: number) {
      try {
        const response = await fetch(`http://localhost:8000/book_genre/${bookGenreId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch bookGenre data");
        }
        const bookGenreData = await response.json();
        this.bookGenre = bookGenreData; // Update the state with the fetched bookGenre data
        return this.bookGenre
      } catch (error) {
        console.error("Error fetching bookGenre data:", error);
      }
    },
  },
});