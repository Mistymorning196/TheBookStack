import { defineStore } from "pinia";
import { AuthorBook } from "../types";

export const useAuthorBookStore = defineStore("authorBook", {
  state: (): {authorBook: AuthorBook} => ({
    
    authorBook: {} as AuthorBook, // Holds the currently selected author book
  }),

  actions: {
    // Save the list of author books
    saveAuthorBooks(authorBook: AuthorBook) {
      this.authorBook = authorBook;
    },

    // Fetch a single author book by ID from the backend
    async fetchAuthorBook(authorBookId: number) {
      try {
        const response = await fetch(`https://thebookstack-2.onrender.com/author_book/${authorBookId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch author book data");
        }
        const authorBookData = await response.json();
        this.authorBook = authorBookData; // Update the state with the fetched authorBook data
      
      } catch (error) {
        console.error("Error fetching author book data:", error);
      }
    },

    async fetchAuthorBookReturn(authorBookId: number) {
      try {
        const response = await fetch(`https://thebookstack-2.onrender.com/author_book/${authorBookId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch author book data");
        }
        const authorBookData = await response.json();
        this.authorBook = authorBookData; // Update the state with the fetched author book data
        return this.authorBook
      } catch (error) {
        console.error("Error fetching author book data:", error);
      }
    },
  },
});