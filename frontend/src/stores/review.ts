import { defineStore } from "pinia";
import { Review } from "../types";

export const useReviewStore = defineStore("review", {
  state: (): {review: Review} => ({
    
    review: {} as Review, // Holds the currently selected review
  }),

  actions: {
    // Save the list of reviews
    saveReviews(review: Review) {
      this.review = review;
    },


    // Fetch a single review by ID from the backend
    async fetchReview(reviewId: number) {
      try {
        const response = await fetch(`http://localhost:8000/review/${reviewId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch review data");
        }
        const reviewData = await response.json();
        this.review = reviewData; // Update the state with the fetched review data
      
      } catch (error) {
        console.error("Error fetching review data:", error);
      }
    },

    async fetchReviewReturn(reviewId: number) {
      try {
        const response = await fetch(`http://localhost:8000/review/${reviewId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch review data");
        }
        const reviewData = await response.json();
        this.review = reviewData; // Update the state with the fetched review data
        return this.review
      } catch (error) {
        console.error("Error fetching review data:", error);
      }
    },
  },
});