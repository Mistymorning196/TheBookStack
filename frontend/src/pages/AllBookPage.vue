<template>
  <ReaderNavBarComponent />
  <div class="body">
    <h1>Every Book</h1>
       <!--Filter to filter the books by genre-->
    <div class="filter">
      <label for="genre-select">Filter by Genre:</label>
      <select id="genre-select" v-model="selectedGenre">
        <option value="">All Genres</option>
        <option v-for="genre in genreList" :key="genre.id" :value="genre.id">
          {{ genre.type }}
        </option>
      </select>
    </div>

       <!--Display all books with links-->
    <section class="display">
      <div v-for="book in filteredBooks" :key="book.id" class="book-card">
        <router-link :to="`/book/${book.id}`" class="book-link">
          <div v-if="book.cover_image">
            <img :src="`http://localhost:8000/${book.cover_image}`" alt="Book Cover" class="book-cover"/>
          </div>
          <p v-else>No cover image available</p>
          <p><strong>{{ book.title }}</strong></p>
          <p>Author: {{ book.author }}</p>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import ReaderNavBarComponent from "../components/ReaderNav.vue";
import { useBooksStore } from "../stores/books";
import { Book } from "../types";

export default defineComponent({
  components: {
    ReaderNavBarComponent,
  },
  data() {
    return {
      books: [] as Book[],
      genres: [] as any[],
      bookGenres: [] as any[],
      userBooks: [] as any[],
      selectedGenre: "" as string | number,
      bookUserCounts: {} as Record<number, number>,
    };
  },
  computed: {
    //get list of genres
    genreList() {
      return this.genres
        .filter(genre => genre && genre.type)  // Ensure genre has the 'type' field
        .sort((a, b) => a.type.localeCompare(b.type));  // Sort by genre type
    },
    //filters the book by using bookGenre
    filteredBooks() {
      let filtered = this.books;

      if (this.selectedGenre !== "") {
        const validBookIds = new Set(
          this.bookGenres
            .filter(bg => bg.genre === Number(this.selectedGenre))
            .map(bg => bg.book)
        );
        filtered = filtered.filter(book => validBookIds.has(book.id));
      }

      return filtered.sort((a, b) => {
        return (this.bookUserCounts[b.id] || 0) - (this.bookUserCounts[a.id] || 0);
      });
    },
  },
  async mounted() {
    await this.fetchAllData();
  },
  methods: {
    //fetches books, genres, userbooks, bookgenres
    async fetchAllData() {
      const [bookRes, genreRes, bookGenreRes, userBookRes] = await Promise.all([
        fetch("http://localhost:8000/books/"),
        fetch("http://localhost:8000/genres/"),
        fetch("http://localhost:8000/book_genres/"),
        fetch("http://localhost:8000/user_books/"),
      ]);

      const bookData = await bookRes.json();
      const genreData = await genreRes.json();
      const bookGenreData = await bookGenreRes.json();
      const userBookData = await userBookRes.json();

      this.books = bookData.books || [];
      this.genres = genreData.genres || []; // Ensure this contains an array of genre objects
      this.bookGenres = bookGenreData.book_genre || [];
      this.userBooks = userBookData.user_books || [];

      this.bookUserCounts = {};
      for (const ub of this.userBooks) {
        this.bookUserCounts[ub.book] = (this.bookUserCounts[ub.book] || 0) + 1;
      }

      useBooksStore().saveBooks(this.books);
    },
  },
});
</script>

<style scoped>
/*general styling*/
.body {
  font-family: Arial, Helvetica, sans-serif;
  padding: 0.5rem 1rem; 
  background-color: #EFE0CB;
}

h1 {
  background-color: #2f4a54;
  color: white;
  text-align: center;
  padding: 0.6rem 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  font-size: 1.6rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Filter Section */
.filter {
  margin: 0.5rem 0 1.5rem;
  text-align: center;
}

.filter label {
  font-weight: bold;
  margin-right: 0.5rem;
  color: #2f4a54;
}

.filter select {
  padding: 0.3rem 0.5rem;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 0.9rem;
}

/* Display Grid */
.display {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem;
  justify-content: center;
}

/* Book Card */
.book-card {
  background-color: #2f4a54;
  color: white;
  padding: 0.8rem;
  border-radius: 10px;
  width: 220px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

/* Book Link Styling */
.book-link {
  text-decoration: none;
  color: inherit;
}

.book-link p {
  background-color: #71929f;
  padding: 0.4rem;
  margin: 0.4rem 0;
  border-radius: 6px;
  text-align: center;
  font-size: 0.85rem;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.book-cover {
  width: 60px;         
  height: 60px;          
  object-fit: cover;
  border-radius: 4px;
  box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
  margin-bottom: 0.3rem;
}

.book-cover:hover {
  transform: scale(1.03);
}


/* Responsive Styles */
@media (max-width: 768px) {
  .display {
    flex-direction: column;
    align-items: center;
  }

  .book-card {
    width: 90%;
  }

  .filter select {
    width: 80%;
    margin-top: 0.5rem;
  }
}

</style>

