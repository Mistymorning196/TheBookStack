import { defineStore } from 'pinia'
import { Discussion } from '../types'

export const useDiscussionsStore = defineStore('discussions', {
    state: () => ({ 
        discussions: [] as Discussion[],
    }),
    actions: {
        saveDiscussions(discussions: Discussion[]) {
            this.discussions = discussions
        },
        removeDiscussion(discussionId: number) {
            this.discussions = this.discussions.filter((r) => r.id !== discussionId);
        },
    }
})