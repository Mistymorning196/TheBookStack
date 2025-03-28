<template>
    <div class="body">
      <h1>Blog Posts:</h1>
      <section class="scrollable-container">
        <div v-for="(blog, index) in blogs" :key="index" class="blog-card">
          <router-link :to="`/post/${blog.id}`" class="blog-link">
            <p class="blog-title">Title: {{ blog.title }}</p>
          </router-link>
        </div>
      </section>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import { useBlogsStore } from "../stores/blogs";
  import { Blog } from "../types/index";
  
  export default defineComponent({
    data() {
      return {
        reader_id: null as number | null, // Initially null, will be populated after mounted
      };
    },
    async mounted() {
      // Fetch blogs
      const responseBlog = await fetch("http://localhost:8000/blogs/");
      const dataBlog = await responseBlog.json();
      const blogs = dataBlog.blogs as Blog[];
      const storeBlog = useBlogsStore();
      storeBlog.saveBlogs(blogs);
    },
    computed: {
      blogs() {
        const storeBlog = useBlogsStore();
        return storeBlog.blogs;
      },
    },
    setup() {
      const storeBlog = useBlogsStore();
      return { storeBlog };
    },
  });
  </script>
  
  <style scoped>
  /* General Styling */
  .body {
    font-family: "Arial", sans-serif;
    background-color: #efe0cb; /* Light background */
    min-height: 100vh;
    padding: 1rem;
    margin: 0;
    text-align: center;
  }
  
  /* Scrollable Section */
  .scrollable-container {
    max-height: 500px; /* Limit height for scrolling */
    overflow-y: auto;
    background-color: #2f4a54;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  /* Individual Blog Card */
  .blog-card {
    background-color: #71929f;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease-in-out;
    width: 90%;
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
  }
  
  .blog-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
  }
  
  /* Blog Title */
  .blog-title {
    color: white;
    font-size: 1.2rem;
    font-weight: bold;
    margin: 0;
    padding: 0.5rem;
    border-radius: 5px;
    background-color: #542f2f;
  }
  
  /* Blog Link */
  .blog-link {
    text-decoration: none;
    color: white;
    transition: all 0.3s ease;
  }
  
  .blog-link:hover {
    color: #f0b400;
    transform: scale(1.05);
  }
  
  /* Responsive Design */
  @media (max-width: 768px) {
    .scrollable-container {
      max-height: 400px; /* Adjust for mobile */
    }
  
    .blog-card {
      width: 95%;
    }
  }
  </style>
  
  