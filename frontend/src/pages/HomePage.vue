<template>
  <ReaderNavBarComponent />
  <div class="body">
    <h1>Homepage</h1>
  </div>

  <h2>Recommended Books:</h2>
  <section class="display">
    <div v-for="(book, index) in recommendedBooks" :key="index">
      <router-link :to="`/book/${book.id}`" class="book-link">
        <div v-if="book.cover_image">
          <img :src="`http://localhost:8000/${book.cover_image}`" alt="Book Cover" class="book-cover"/>
        </div>
        <p v-else>No cover image available</p>
        <p>Title: {{ book.title }}</p>
        <p>Author: {{ book.author }}</p>
      </router-link>
    </div>
  </section>

  <button @click="goToAllBooks" class="go-to-all-books-button">See All Books</button>

  <h2>Recommended Readers:</h2>
  <section class="display">
    <div v-for="(reader, index) in recommendedReaders" :key="index">
      <router-link :to="`/user/${reader.id}`" class="user-link">
        <p>Username: {{ reader.username }}</p>
      </router-link>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import ReaderNavBarComponent from "../components/ReaderNav.vue";

import { useReadersStore } from "../stores/readers";
import { useBooksStore } from "../stores/books";
import { Book, Reader, Friendship, ReaderGenre, UserBook, Genre } from "../types/index";


export default defineComponent({
  data() {
    return {
      reader_id: null as number | null,
      recommendedBooks: [] as Book[],
      recommendedReaders: [] as Reader[],
    };
  },
  async mounted() {
    const sessionCookie = document.cookie.split(';');
    let currentSessionid = '';
    for (let cookie of sessionCookie) {
      cookie = cookie.trim();
      if (cookie.startsWith("sessionid=")) {
        currentSessionid = cookie.substring("sessionid=".length);
      }
    }

    const previousSessionid = window.sessionStorage.getItem("session_id");
    if (currentSessionid === previousSessionid) {
      this.reader_id = Number(window.sessionStorage.getItem("reader_id"));
    } else {
      const params = new URLSearchParams(window.location.search);
      this.reader_id = parseInt(params.get("u") || "0");
      sessionStorage.setItem("reader_id", this.reader_id.toString());
      sessionStorage.setItem("session_id", currentSessionid);
    }

    await this.fetchDataAndRecommend();
  },
  components: {
    ReaderNavBarComponent,
  },
  methods: {
    async fetchDataAndRecommend() {
      const [
        bookRes,
        readerRes,
        bookGenreRes,
        readerGenreRes,
        userBooksRes,
        friendshipRes
      ] = await Promise.all([
        fetch("http://localhost:8000/books/"),
        fetch("http://localhost:8000/readers/"),
        fetch("http://localhost:8000/book_genres/"),
        fetch("http://localhost:8000/reader_genres/"),
        fetch("http://localhost:8000/user_books/"),
        fetch("http://localhost:8000/friendships/") // Fetch friendships
      ]);

      const books = (await bookRes.json()).books as Book[];
      const readers = (await readerRes.json()).readers as Reader[];
      const bookGenres = (await bookGenreRes.json()).book_genre || [];
      const readerGenres = (await readerGenreRes.json()).reader_genre || [];
      const userBooks = (await userBooksRes.json()).user_books || [];
      const friendships = (await friendshipRes.json()).friendships || []; // Friendships data

      useBooksStore().saveBooks(books);
      useReadersStore().saveReaders(readers);

      const currentReaderVector: Record<number, number> = {};
      for (const rg of readerGenres) {
        if (rg.user === this.reader_id) {
          currentReaderVector[rg.genre] = rg.count;
        }
      }

      // --- BOOK RECOMMENDATION (filtered by books user does NOT have) ---
      const userBookIds = new Set(
        userBooks.filter((ub: UserBook) => ub.user === this.reader_id).map((ub: UserBook) => ub.book)
      );

      const bookScores: { book: Book; score: number }[] = [];
      for (const book of books) {
        if (userBookIds.has(book.id)) continue; // Skip already owned books

        const genreVector: Record<number, number> = {};
        for (const bg of bookGenres) {
          if (bg.book === book.id) {
            genreVector[bg.genre] = (genreVector[bg.genre] || 0) + 1;
          }
        }

        // Dot product similarity
        let score = 0;
        for (const genre in genreVector) {
          score += (currentReaderVector[+genre] || 0) * genreVector[+genre];
        }

        bookScores.push({ book, score });
      }

      // --- READER RECOMMENDATION (excluding friendships where user == reader_id) ---
      // Extract users who have a friendship where user === reader_id
      const excludedReaderIds = new Set(
        friendships.filter((f: Friendship) => f.user === this.reader_id).map((f: Friendship) => f.friend)
      );

      const readerScores: { reader: Reader; score: number }[] = [];
      for (const reader of readers) {
        if (reader.id === this.reader_id || excludedReaderIds.has(reader.id)) continue;

        const readerVector: Record<number, number> = {};
        for (const rg of readerGenres) {
          if (rg.user === reader.id) {
            readerVector[rg.genre] = rg.count;
          }
        }

        let score = 0;
        for (const genre in readerVector) {
          score += (currentReaderVector[+genre] || 0) * readerVector[+genre];
        }

        readerScores.push({ reader, score });
      }

      // --- Apply Recommendation ---
      const currentReaderHasPrefs = Object.keys(currentReaderVector).length > 0;

      if (currentReaderHasPrefs) {
        this.recommendedBooks = bookScores
          .sort((a, b) => b.score - a.score)
          .slice(0, 5)
          .map(item => item.book);

        this.recommendedReaders = readerScores
          .sort((a, b) => b.score - a.score)
          .slice(0, 5)
          .map(item => item.reader);
      } else {
        // Fallback: recommend most popular books
        const bookCounts: Record<number, number> = {};
        for (const bg of bookGenres) {
          bookCounts[bg.book] = (bookCounts[bg.book] || 0) + 1;
        }

        this.recommendedBooks = books
          .map(book => ({ book, count: bookCounts[book.id] || 0 }))
          .sort((a, b) => b.count - a.count)
          .slice(0, 5)
          .map(item => item.book);

        // Fallback: readers with the most diverse genre interests
        const readerDiversity = readers
          .filter(r => r.id !== this.reader_id && !excludedReaderIds.has(r.id))
          .map(reader => {
            const genres = readerGenres.filter((rg: ReaderGenre) => rg.user === reader.id);
            const uniqueGenres = new Set(genres.map((g: Genre) => g.genre));
            return { reader, diversity: uniqueGenres.size };
          })
          .sort((a, b) => b.diversity - a.diversity)
          .slice(0, 5)
          .map(item => item.reader);

        this.recommendedReaders = readerDiversity;
      }
    },

    // Method to handle the "See All Books" button click
    goToAllBooks() {
      this.$router.push('/allBooks'); // Navigates to /allBooks page
    }
  },
});
</script>

<style scoped>
/* Body Styling */
.body {
    font-family: Arial, Helvetica, sans-serif;
    background-color: #EFE0CB; /* Light background */
    margin: 0;
    padding: 0.8rem; /* Padding around the body */
    max-height: 75vh; /* Reduce max height to 75% of the viewport height */
    overflow-y: auto; /* Enable scrolling if content overflows */
}

/* Heading Styling */
h1, h2 {
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

h1 {
    font-size: 1.8rem; /* Slightly smaller font for h1 */
    margin-top: 1rem; /* Reduced top margin */
}

h2 {
    font-size: 1.4rem; /* Slightly smaller for h2 */
    margin-top: 0.3rem; /* Smaller top margin for h2 */
}

/* Display Section (Book and User Lists) */
.display {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem; /* Further reduced gap between items */
    justify-content: center; /* Center the items */
    margin-top: 1rem;
    padding: 0 1rem; /* Add padding to prevent stretching on edges */
}

/* General Card Styling for Book and User Items */
.display > div {
    background-color: #2f4a54;
    padding: 0.5rem; /* Reduced padding for compactness */
    margin: 0.3rem; /* Reduced margin */
    border-radius: 8px;
    flex-basis: 30%; /* Adjust card width */
    max-width: 250px; /* Further reduce max-width to 250px */
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.display > div:hover {
    transform: translateY(-4px); /* Slightly smaller hover effect */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* Slightly elevated shadow on hover */
}

/* Link Styling */
.book-link, .user-link {
    text-decoration: none;
    color: white;
    font-size: 0.9rem; /* Smaller font size for links */
    font-weight: bold;
    transition: color 0.3s ease, transform 0.3s ease;
}

/* Hover Effect for Links */
.book-link:hover, .user-link:hover {
    color: #f0b400; /* Golden color on hover */
    transform: scale(1.03); /* Slight zoom effect */
}

/* Paragraph Styling (inside links) */
.book-link > p, .user-link > p {
    margin: 0.2rem 0;
    padding: 0.3rem;
    background-color: #71929f; /* Light background for content */
    border-radius: 5px;
    color: white;
    text-align: center;
    font-size: 0.8rem; /* Smaller text size for paragraph */
}

.all-books-button {
    background-color: #2f4a54; /* Matching dark background */
    color: white;
    border: none;
    padding: 0.6rem 1.2rem; /* Slightly larger padding */
    font-size: 1rem;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
    margin: 1rem auto 0;
    display: block;
}

.all-books-button:hover {
    background-color: #f0b400; /* Golden hover effect */
    color: #2f4a54; /* Contrast text color on hover */
    transform: scale(1.03);
}

.book-cover {
  width: 60px;           /* Smaller width */
  height: 60px;          /* Smaller height */
  object-fit: cover;
  border-radius: 4px;
  box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
  margin-bottom: 0.3rem;
}

.book-cover:hover {
  transform: scale(1.03);
}



/* Additional Responsive Styling */
@media (max-width: 768px) {
    .display {
        flex-direction: column;
        align-items: center;
    }

    .display > div {
        flex-basis: 80%; /* Increase card width on smaller screens */
        max-width: 100%; /* Allow full width on mobile */
    }

    h1, h2 {
        font-size: 1.4rem; /* Even smaller font for mobile */
    }

    .book-link, .user-link {
        font-size: 0.8rem; /* Smaller font size for mobile */
    }

    .book-link > p, .user-link > p {
        font-size: 0.7rem; /* Even smaller text for mobile */
    }
}
</style>

