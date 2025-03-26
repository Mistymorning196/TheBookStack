<template>
    <div>
      <!-- Search bar input -->
      <input 
        v-model="query" 
        placeholder="Search by title, author, or username..." 
        @input="search" 
        class="search-input" 
      />
    
      <!-- Button group to toggle between searching books and readers -->
      <div class="button-group">
        <button @click="toggleSearchType('books')" :class="{ active: searchType === 'books' }">Search Books</button>
        <button @click="toggleSearchType('readers')" :class="{ active: searchType === 'readers' }">Search Readers</button>
      </div>
    
      <!-- Grid display for results -->
      <div class="grid-container">
        <div v-for="item in filteredResults" :key="item.id" class="grid-item">
          <!-- For books -->
          <div v-if="searchType === 'books'">
            <router-link :to="`/book/${item.id}`" class="book-link">
                <strong class="book-title">{{ item.title }}</strong>
                <p><em>{{ item.author }}</em></p>
            </router-link>
          </div>
          
          <!-- For readers -->
          <div v-if="searchType === 'readers'">
            <router-link :to="`/user/${item.id}`" class="user-link">
                <strong class="reader-username">{{ item.username }}</strong>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted, computed } from "vue";
  
  export default defineComponent({
    setup() {
      const query = ref("");
      const searchType = ref("books"); // Default search type is 'books'
      const results = ref<any[]>([]);
      const reader_id = ref(Number(window.sessionStorage.getItem("reader_id"))); // Use ref for reader_id
  
      // Fetch all books
      const fetchBooks = async () => {
        try {
          const response = await fetch("http://localhost:8000/books/");
          const data = await response.json();
          results.value = data.books; // Access the "books" key from the response
        } catch (error) {
          console.error("Error fetching books:", error);
        }
      };
  
      // Fetch all readers
      const fetchReaders = async () => {
        try {
          const response = await fetch("http://localhost:8000/readers/");
          const data = await response.json();
          results.value = data.readers; // Access the "readers" key from the response
        } catch (error) {
          console.error("Error fetching readers:", error);
        }
      };
  
      // Search function to call either books or readers
      const search = async () => {
        if (searchType.value === 'books') {
          try {
            const response = await fetch(`http://localhost:8000/books/?search=${query.value}`);
            const data = await response.json();
            results.value = data.books; // Access the "books" key from the response
          } catch (error) {
            console.error("Error searching books:", error);
          }
        } else if (searchType.value === 'readers') {
          try {
            const response = await fetch(`http://localhost:8000/readers/?search=${query.value}`);
            const data = await response.json();
            results.value = data.readers; // Access the "readers" key from the response
          } catch (error) {
            console.error("Error searching readers:", error);
          }
        }
      };
  
      // Toggle between searching books or readers
      const toggleSearchType = (type: string) => {
        searchType.value = type;
        query.value = ''; // Clear search input when toggling search type
        results.value = []; // Clear previous search results
        if (type === 'books') {
          fetchBooks();
        } else {
          fetchReaders();
        }
      };
  
      // Filter results to exclude the logged-in user when searching for readers
      const filteredResults = computed(() => {
        // Ensure reader_id exists before filtering
        if (searchType.value === "readers" && reader_id.value) {
          return results.value.filter((item) => item.id !== reader_id.value);
        }
        return results.value;
      });
  
      // Fetch books on page load by default
      onMounted(fetchBooks);
  
      return { query, searchType, results, filteredResults, search, toggleSearchType };
    },
  });
  </script>
  
  <style scoped>
  /* Search bar styling */
  .search-input {
    width: 100%;
    padding: 8px;
    margin-top: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  /* Button group styling */
  .button-group {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }
  
  .button-group button {
    padding: 8px 12px; /* Smaller padding for the button */
    background-color: #2f4a54;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    width: 45%; /* Smaller width for buttons */
  }
  
  .button-group button.active {
    background-color: #3a5f6f; /* Highlight active button */
  }
  
  /* Grid container styling */
  .grid-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-top: 20px;
    max-height: 500px; /* Set a max-height for the container */
    overflow-y: auto; /* Enable vertical scrolling */
    background-color: #71929f; /* Background color for the grid */
    padding: 20px;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow for grid */
  }
  
  /* Grid item styling */
  .grid-item {
    background-color: #2f4a54;
    color: white;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease, background-color 0.3s ease;
    min-height: 80px; /* Reduced height for the output boxes */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  
  /* Hover effect for grid items */
  .grid-item:hover {
    transform: scale(1.05);
    background-color: #3a5f6f;
  }
  
  /* Book title styling */
  .book-title {
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 0.5em;
  }
  
  /* Reader username styling */
  .reader-username {
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 0.5em;
  }
  
  /* Ensures content inside grid items remains aligned */
  .grid-item p {
    font-size: 1rem;
    margin-bottom: 0.5em;
    flex-grow: 1;
  }
  
  /* Styling for links (router-link) */
  .book-link,
  .user-link {
    text-decoration: none;
    color: inherit;
    display: block; /* Makes the whole area clickable */
    padding: 10px;
  }
  
  .book-link:hover,
  .user-link:hover {
    background-color: #3a5f6f;
    border-radius: 5px;
  }
  
  /* Media query for responsive grid */
  @media (max-width: 768px) {
    .grid-container {
      grid-template-columns: repeat(2, 1fr); /* 2 items per row on smaller screens */
    }
  }
  
  @media (max-width: 480px) {
    .grid-container {
      grid-template-columns: 1fr; /* 1 item per row on extra small screens */
    }
  }
  </style>
  
  
  