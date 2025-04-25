import { defineStore } from "pinia";
import { Reader } from "../types";

export const useReaderStore = defineStore("reader", {
  state: (): {reader: Reader, csrf:string} => ({
    
    reader: {} as Reader, // Holds the currently selected reader
    csrf: ''
  }),

  actions: {
    // Save the list of readers
    saveReaders(reader: Reader) {
      this.reader = reader;
    },

    setCsrfToken(csrf: string){
      this.csrf = csrf;
    },
    // Fetch a single reader by ID from the backend
    async fetchReader(readerId: number) {
      try {
        const response = await fetch(`http://localhost:8000/reader/${readerId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch reader data");
        }
        const readerData = await response.json();
        this.reader = readerData; // Update the state with the fetched reader data
      
      } catch (error) {
        console.error("Error fetching reader data:", error);
      }
    },

    async fetchReaderReturn(readerId: number) {
      try {
        const response = await fetch(`http://localhost:8000/reader/${readerId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch reader data");
        }
        const readerData = await response.json();
        this.reader = readerData; // Update the state with the fetched reader data
        return this.reader
      } catch (error) {
        console.error("Error fetching reader data:", error);
      }
    },
  },
});