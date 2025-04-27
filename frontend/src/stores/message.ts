import { defineStore } from "pinia";
import { Message } from "../types";

export const useMessageStore = defineStore("friendship", {
  state: (): {message: Message} => ({
    
    message: {} as Message // Holds the currently selected message

  }),
 
  actions: {
    // Save the list of messageS
    saveMessages(message: Message) {
      this.message = message;
    },


    // Fetch a single message by ID from the backend
    async fetchMessage(messageId: number) {
      try {
        const response = await fetch(`https://thebookstack-2.onrender.com/message/${messageId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch message data");
        }
        const messageData = await response.json();
        this.message = messageData; // Update the state with the fetched message data
      
      } catch (error) {
        console.error("Error fetching message data:", error);
      }
    },

   
  },
});