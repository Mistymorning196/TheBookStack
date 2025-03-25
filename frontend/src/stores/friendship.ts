import { defineStore } from "pinia";
import { Friendship } from "../types";

export const useFriendshipStore = defineStore("friendship", {
  state: (): {friendship: Friendship} => ({
    
    friendship: {} as Friendship // Holds the currently selected friendship

  }),
 
  actions: {
    // Save the list of friendships
    savefriendships(friendship: Friendship) {
      this.friendship = friendship;
    },


    // Fetch a single friendship by ID from the backend
    async fetchFriendship(friendshipId: number) {
      try {
        const response = await fetch(`http://localhost:8000/friendship/${friendshipId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch friendship data");
        }
        const friendshipData = await response.json();
        this.friendship = friendshipData; // Update the state with the fetched friendship data
      
      } catch (error) {
        console.error("Error fetching friendship data:", error);
      }
    },

   
  },
});