import { defineStore } from 'pinia'
import { Comment } from '../types'

export const useCommentsStore = defineStore('comments', {
    state: () => ({ 
        comments: [] as Comment[],
    }),
    actions: {
        saveComments(comments: Comment[]) {
            this.comments = comments
        },
        removeComment(commentId: number) {
            this.comments = this.comments.filter((r) => r.id !== commentId);
        },
    }
})