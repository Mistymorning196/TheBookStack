import { defineStore } from "pinia";
import { Comment } from "../types";

export const useCommentStore = defineStore("comment", {
  state: (): {comment: Comment} => ({
    
    comment: {} as Comment, // Holds the currently selected comment
  }),

  actions: {
    // Save the list of comments
    saveComments(comment: Comment) {
      this.comment = comment;
    },


    // Fetch a single comment by ID from the backend
    async fetchComment(commentId: number) {
      try {
        const response = await fetch(`https://thebookstack-2.onrender.com/comment/${commentId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch comment data");
        }
        const commentData = await response.json();
        this.comment = commentData; // Update the state with the fetched comment data
      
      } catch (error) {
        console.error("Error fetching comment data:", error);
      }
    },

    async fetchCommentReturn(commentId: number) {
      try {
        const response = await fetch(`https://thebookstack-2.onrender.com/comment/${commentId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch comment data");
        }
        const commentData = await response.json();
        this.comment = commentData; // Update the state with the fetched comment data
        return this.comment
      } catch (error) {
        console.error("Error fetching comment data:", error);
      }
    },
  },
});