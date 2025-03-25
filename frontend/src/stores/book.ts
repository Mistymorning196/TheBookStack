import { defineStore } from "pinia";
import { Book } from "../types";

export const useBookStore = defineStore("book", {
  state: (): {book: Book} => ({
    
    book: {} as Book, // Holds the currently selected book
  }),

  actions: {
    // Save the list of books
    saveBooks(book: Book) {
      this.book = book;
    },


    // Fetch a single book by ID from the backend
    async fetchBook(bookId: number) {
      try {
        const response = await fetch(`http://localhost:8000/book/${bookId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch book data");
        }
        const bookData = await response.json();
        this.book = bookData; // Update the state with the fetched book data
      
      } catch (error) {
        console.error("Error fetching book data:", error);
      }
    },

    async fetchBookReturn(bookId: number) {
      try {
        const response = await fetch(`http://localhost:8000/book/${bookId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch book data");
        }
        const bookData = await response.json();
        this.book = bookData; // Update the state with the fetched book data
        return this.book
      } catch (error) {
        console.error("Error fetching book data:", error);
      }
    },
  },
});