import { defineStore } from 'pinia'
import { Friendship } from '../types'

export const useFriendshipsStore = defineStore('friendships', {
    state: () => ({ 
        friendships: [] as Friendship[],
    }),
    actions: {
        saveFriendships(friendships: Friendship[]) {
            this.friendships = friendships
        },
        // Add a new chosen hobby
        addFriendship(friendship: Friendship) {
            this.friendships.push(friendship);
        },
        removeFriendship(friendshipId: number) {
            this.friendships = this.friendships.filter((f) => f.id !== friendshipId);
        },
    }
})