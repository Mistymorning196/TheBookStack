import { defineStore } from "pinia";
import { Discussion } from "../types";

export const useDiscussionStore = defineStore("discussion", {
  state: (): {discussion: Discussion} => ({
    
    discussion: {} as Discussion, // Holds the currently selected discussion
  }),

  actions: {
    // Save the list of discussions
    saveDiscussions(discussion: Discussion) {
      this.discussion = discussion;
    },


    // Fetch a single discussion by ID from the backend
    async fetchDiscussion(discussionId: number) {
      try {
        const response = await fetch(`http://localhost:8000/discussion/${discussionId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch discussion data");
        }
        const discussionData = await response.json();
        this.discussion = discussionData; // Update the state with the fetched discussion data
      
      } catch (error) {
        console.error("Error fetching discussion data:", error);
      }
    },

    async fetchDiscussionReturn(discussionId: number) {
      try {
        const response = await fetch(`http://localhost:8000/discussion/${discussionId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch discussion data");
        }
        const discussionData = await response.json();
        this.discussion = discussionData; // Update the state with the fetched discussion data
        return this.discussion
      } catch (error) {
        console.error("Error fetching discussion data:", error);
      }
    },
  },
});