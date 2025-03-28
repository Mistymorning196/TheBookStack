import { defineStore } from 'pinia'
import { Blog } from '../types'

export const useBlogsStore = defineStore('blogs', {
    state: () => ({ 
        blogs: [] as Blog[],
    }),
    actions: {
        saveBlogs(blogs: Blog[]) {
            this.blogs = blogs
        }
    }
})