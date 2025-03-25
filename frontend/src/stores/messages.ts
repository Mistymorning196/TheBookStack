import { defineStore } from 'pinia'
import { Message } from '../types'

export const useMessagesStore = defineStore('messages', {
    state: () => ({ 
        messages: [] as Message[],
    }),
    actions: {
        saveMessages(messages: Message[]) {
            this.messages = messages
        },
        // Add a new chosen hobby
        addMessage(message: Message) {
            this.messages.push(message);
        },
        removeMessage(messageId: number) {
            this.messages = this.messages.filter((m) => m.id !==messageId);
        },
    }
})