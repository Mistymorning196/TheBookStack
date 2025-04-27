<template>
  <ReaderNavBarComponent />
  <div class="body">
    <h1>Blog Posts:</h1>

    <!-- Search bar input -->
    <input 
      v-model="query" 
      placeholder="Search by title or author..." 
      @input="search" 
      class="search-input" 
    />

    <!-- Scrollable section to show blogs -->
    <section class="scrollable-container">
      <div v-for="(blog, index) in filteredBlogs" :key="index" class="blog-card">
        <router-link :to="`/post/${blog.id}`" class="blog-link">
          <div class="blog-title">
            <p>Title: {{ blog.title }}</p>
            <p>Author: {{ blog.author }}</p>
          </div>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import ReaderNavBarComponent from "../components/ReaderNav.vue";
import { defineComponent} from "vue";
import { useBlogsStore } from "../stores/blogs";
import { Blog } from "../types/index";

export default defineComponent({
  data() {
    return {
      query: "",  // The search query
      reader_id: null as number | null, // Initially null, will be populated after mounted
    };
  },
  async mounted() {
    // Fetch all blogs initially
    await this.fetchBlogs();
  },
  computed: {
    // Filter blogs based on the search query
    filteredBlogs() {
      return this.blogs.filter((blog) => {
        const query = this.query.toLowerCase();
        return (
          blog.title.toLowerCase().includes(query) ||
          blog.author.toLowerCase().includes(query)
        );
      });
    },
    // Fetch blogs from the store
    blogs() {
      const storeBlog = useBlogsStore();
      return storeBlog.blogs;
    },
  },
  methods: {
    // Fetch blogs from the API and store them
    async fetchBlogs() {
      try {
        const response = await fetch("https://thebookstack-2.onrender.com/blogs/");
        const data = await response.json();
        const blogs = data.blogs as Blog[];
        const storeBlog = useBlogsStore();
        storeBlog.saveBlogs(blogs);
      } catch (error) {
        console.error("Error fetching blogs:", error);
      }
    },

    // Search function called when user types in the search bar
    async search() {
      if (this.query.trim()) {
        await this.fetchBlogsByQuery();
      } else {
        await this.fetchBlogs();  // Fetch all blogs if the search query is empty
      }
    },

    // Fetch blogs filtered by search query (by title or author)
    async fetchBlogsByQuery() {
      try {
        const response = await fetch(`https://thebookstack-2.onrender.com/blogs/?search=${this.query}`);
        const data = await response.json();
        const blogs = data.blogs as Blog[];
        const storeBlog = useBlogsStore();
        storeBlog.saveBlogs(blogs);
      } catch (error) {
        console.error("Error fetching blogs by query:", error);
      }
    },
  },
  components: {
    ReaderNavBarComponent,
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

/* Heading Styling */
h1 {
    color: white;
    background-color: #2f4a54; /* Dark background for headers */
    padding: 0.3rem 1rem; /* Reduced padding for better space usage */
    margin: 0.3rem 0; /* Reduced margin between titles */
    border-radius: 5px;
    font-size: 1.6rem; /* Reduced font size for smaller headings */
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Search input styling */
.search-input {
  width: 100%;
  padding: 8px;
  margin-top: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 20px;
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
