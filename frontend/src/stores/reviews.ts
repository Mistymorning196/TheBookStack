import { defineStore } from 'pinia'
import { Review } from '../types'

export const useReviewsStore = defineStore('reviews', {
    state: () => ({ 
        reviews: [] as Review[],
    }),
    actions: {
        saveReviews(reviews: Review[]) {
            this.reviews = reviews
        },
        // Add a new review
        addReview(review: Review) {
            this.reviews.push(review);
        },
        removeReview(reviewId: number) {
            this.reviews = this.reviews.filter((r) => r.id !== reviewId);
        },
    }
})