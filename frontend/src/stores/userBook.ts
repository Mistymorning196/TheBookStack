import { defineStore } from "pinia";
import { UserBook } from "../types";

export const useUserBookStore = defineStore("userBook", {
  state: (): {userBook: UserBook} => ({
    
    userBook: {} as UserBook, // Holds the currently selected user book
  }),

  actions: {
    // Save the list of user books
    saveUserBooks(userBook: UserBook) {
      this.userBook = userBook;
    },

    // Fetch a single user book by ID from the backend
    async fetchUserBook(userBookId: number) {
      try {
        const response = await fetch(`http://localhost:8000/user_book/${userBookId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch user book data");
        }
        const userBookData = await response.json();
        this.userBook = userBookData; // Update the state with the fetched userBook data
      
      } catch (error) {
        console.error("Error fetching user book data:", error);
      }
    },

    async fetchUserBookReturn(userBookId: number) {
      try {
        const response = await fetch(`http://localhost:8000/user_book/${userBookId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch user book data");
        }
        const userBookData = await response.json();
        this.userBook = userBookData; // Update the state with the fetched user book data
        return this.userBook
      } catch (error) {
        console.error("Error fetching user book data:", error);
      }
    },
  },
});