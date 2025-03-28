import { defineStore } from "pinia";
import { Blog } from "../types";

export const useBlogStore = defineStore("blog", {
  state: (): {blog: Blog} => ({
    
    blog: {} as Blog, // Holds the currently selected blog
  }),

  actions: {
    // Save the list of blogs
    saveBlogs(blog: Blog) {
      this.blog = blog;
    },


    // Fetch a single blog by ID from the backend
    async fetchBlog(blogId: number) {
      try {
        const response = await fetch(`http://localhost:8000/blog/${blogId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch blog data");
        }
        const blogData = await response.json();
        this.blog = blogData; // Update the state with the fetched blog data
      
      } catch (error) {
        console.error("Error fetching blog data:", error);
      }
    },

    async fetchBlogReturn(blogId: number) {
      try {
        const response = await fetch(`http://localhost:8000/blog/${blogId}/`);
  
        if (!response.ok) {
          throw new Error("Failed to fetch blog data");
        }
        const blogData = await response.json();
        this.blog = blogData; // Update the state with the fetched blog data
        return this.blog
      } catch (error) {
        console.error("Error fetching blog data:", error);
      }
    },
  },
});