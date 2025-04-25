import { defineStore } from 'pinia'
import { AuthorBlog } from '../types'

export const useAuthorBlogsStore = defineStore('authorBlogs', {
    state: () => ({ 
        authorBlogs: [] as AuthorBlog[],
    }),
    actions: {
        saveAuthorBlogs(authorBlogs: AuthorBlog[]) {
            this.authorBlogs = authorBlogs
        }
    }
})