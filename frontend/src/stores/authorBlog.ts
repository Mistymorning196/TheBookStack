import { defineStore } from "pinia";
import { AuthorBlog } from "../types";

export const useAuthorBlogStore = defineStore("authorBlog", {
  state: (): {authorBlog: AuthorBlog} => ({
    
    authorBlog: {} as AuthorBlog, // Holds the currently selected author Blog
  }),

  actions: {
    // Save the list of author Blogs
    saveAuthorBlogs(authorBlog: AuthorBlog) {
      this.authorBlog = authorBlog;
    },

    // Fetch a single author Blog by ID from the backend
    async fetchAuthorBlog(authorBlogId: number) {
      try {
        const response = await fetch(`http://localhost:8000/author_blog/${authorBlogId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch author Blog data");
        }
        const authorBlogData = await response.json();
        this.authorBlog = authorBlogData; // Update the state with the fetched authorBlog data
      
      } catch (error) {
        console.error("Error fetching author Blog data:", error);
      }
    },

    async fetchAuthorBlogReturn(authorBlogId: number) {
      try {
        const response = await fetch(`http://localhost:8000/author_blog/${authorBlogId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch author Blog data");
        }
        const authorBlogData = await response.json();
        this.authorBlog = authorBlogData; // Update the state with the fetched author Blog data
        return this.authorBlog
      } catch (error) {
        console.error("Error fetching author Blog data:", error);
      }
    },
  },
});