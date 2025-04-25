import { defineStore } from "pinia";
import { Author } from "../types";

export const useAuthorStore = defineStore("author", {
  state: (): {author: Author, csrf:string} => ({
    
    author: {} as Author, // Holds the currently selected author
    csrf: ''
  }),

  actions: {
    // Save the list of authors
    saveAuthors(author: Author) {
      this.author = author;
    },

    setCsrfToken(csrf: string){
      this.csrf = csrf;
    },
    // Fetch a single author by ID from the backend
    async fetchAuthor(authorId: number) {
      try {
        const response = await fetch(`http://localhost:8000/author/${authorId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch author data");
        }
        const authorData = await response.json();
        this.author = authorData; // Update the state with the fetched author data
      
      } catch (error) {
        console.error("Error fetching author data:", error);
      }
    },

    async fetchAuthorReturn(authorId: number) {
      try {
        const response = await fetch(`http://localhost:8000/author/${authorId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch author data");
        }
        const authorData = await response.json();
        this.author = authorData; // Update the state with the fetched author data
        return this.author
      } catch (error) {
        console.error("Error fetching author data:", error);
      }
    },
  },
});